import logging
import subprocess
import sys
import tempfile
from importlib.metadata import version
from pathlib import Path
import platform

import requests
from packaging.version import Version

logger = logging.getLogger(__name__)

CURRENT_VERSION = version("econ_automation")
VERSION_URL = "https://github.com/ebusseyst/EconAutomation-REP/releases/latest/download/version.json"
REQUEST_TIMEOUT = 5


def fetch_remote_version() -> dict | None:
    """Fetch version.json from the latest GitHub release."""
    try:
        response = requests.get(VERSION_URL, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        logger.error(f"HTTP error checking for updates: {e}")
        return None
    except requests.ConnectionError as e:
        logger.error(f"Connection error checking for updates: {e}")
        return None
    except requests.Timeout as e:
        logger.error(f"Timeout checking for updates: {e}")
        return None
    except requests.exceptions.JSONDecodeError as e:
        logger.error(f"Invalid JSON in version response: {e}")
        return None


def is_update_available(remote_version: dict) -> bool:
    """Return True if the remote version is newer than the installed version."""
    try:
        return Version(remote_version["version"]) > Version(CURRENT_VERSION)
    except Exception:
        return False


def download_installer(download_url: str, dest_dir: Path) -> Path | None:
    """Stream the installer binary into dest_dir, return its path or None on failure."""
    filename = download_url.split("/")[-1]
    download_path = dest_dir / filename
    try:
        with requests.get(download_url, stream=True, timeout=30) as response:
            response.raise_for_status()
            with open(download_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        return download_path
    except Exception as e:
        logger.error(f"Installer download failed: {e}")
        return None


def launch_installer(installer_path: Path) -> None:
    """
    Launch the installer as a detached process, then exit the app.
    The installer runs independently — the app does not wait for it.
    """
    if platform.system() == "Windows":
        DETACHED_PROCESS = 0x00000008
        subprocess.Popen(
            [str(installer_path)],
            creationflags=DETACHED_PROCESS,
            close_fds=True,
        )
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", str(installer_path)])
    else:
        installer_path.chmod(installer_path.stat().st_mode | 0o111)
        subprocess.Popen([str(installer_path)])

    sys.exit(0)


def check_and_apply_update(prompt_fn=None) -> None:
    """
    Full update flow called at app launch.

    prompt_fn is an optional callable that receives a message string and returns
    True if the user confirms the update. Pass a QMessageBox wrapper in the GUI.
    If prompt_fn is None, the update is applied without prompting.
    """
    remote = fetch_remote_version()
    if remote is None or not is_update_available(remote):
        return

    new_version = remote["version"]
    download_url = remote["download_url"]

    if prompt_fn is not None:
        confirmed = prompt_fn(f"Version {new_version} is available. Install now?")
        if not confirmed:
            return

    with tempfile.TemporaryDirectory() as tmp_dir:
        installer_path = download_installer(download_url, Path(tmp_dir))

        if installer_path is None:
            logger.error("Update download failed.")
            return

        # Move out of the temp dir before it is cleaned up so the detached
        # installer process can still access the file after this context exits.
        stable_path = Path(tempfile.gettempdir()) / installer_path.name
        installer_path.replace(stable_path)

    launch_installer(stable_path)
