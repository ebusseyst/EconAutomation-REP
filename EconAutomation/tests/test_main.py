import logging
import logging.config
import subprocess
import sys
import tempfile
from packaging.version import Version
from pathlib import Path
import platform

import requests

# Setting up same logging config as main
logging.basicConfig(level=logging.INFO)

# Top-level test logger instance
logger = logging.getLogger(__name__)


# TEST CONSTANTS
CURRENT_VERSION = "0.0.1"
VERSION_URL = "https://github.com/ebusseyst/EconAutomation-REP/releases/tag/Test"
REQUEST_TIMEOUT = 5


def fetch_remote_version() -> dict | None:
    """Fetch remote version from Github"""
    try:
        response = requests.get(VERSION_URL, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as http_error:
        logger.error(f"HTTP error checking for updates: {http_error}")
        return None
    except requests.ConnectionError as connection_error:
        logger.error(f"Connection error checking for updates: {connection_error}")
        return None
    except requests.Timeout as timeout_error:
        logger.error(f"Timeout error checking for updates: {timeout_error}")
        return None
    except requests.JSONDecodeError as json_decode_error:
        logger.error(f"JSON decode error checking for updates: {json_decode_error}")
        return None


def is_update_available(remote_version: dict) -> bool:
    """Check if update is available"""
    try:
        return Version(remote_version["version"]) > Version(CURRENT_VERSION)
    except Exception:
        return False


def download_installer(download_url: str, dest_dir: Path) -> Path | None:
    """
    Stream the installer binary into dest_dir

    Args:
        download_url (str): _description_
        dest_dir (Path): _description_

    Returns:
        Path | None: Path to the downloaded file or None if download fails
    """
    filename = download_url.split("/")[-1]
    download_path = dest_dir / filename

    try:
        with requests.get(download_url, stream=True, timeout=30) as response:
            response.raise_for_status()
            with open(download_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        return download_path
    except Exception:
        return None


def launch_installer(installer_path: Path) -> None:
    """
    Launch the installer as a detached process, then exit the app.
    The installer runs independently — the app does not wait for it.
    """
    if platform.system() == "Windows":
        # DETACHED_PROCESS ensures the installer outlives the app process
        DETACHED_PROCESS = 0x00000008
        subprocess.Popen(
            [str(installer_path)],
            creationflags=DETACHED_PROCESS,
            close_fds=True,
        )
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", str(installer_path)])
    else:
        # Linux — assumes .AppImage or similar executable
        installer_path.chmod(installer_path.stat().st_mode | 0o111)  # ensure executable
        subprocess.Popen([str(installer_path)])

    sys.exit(0)  # close the running app so the installer can replace files


def check_and_apply_update(prompt_fn=None) -> None:
    """
    Full update flow. prompt_fn is an optional callable that receives an
    update message string and returns True if the user confirms.
    If prompt_fn is None, updates are applied without prompting.

    In a PySide6 app, pass a function that opens a QMessageBox.
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
            # surface this to the user however makes sense in your UI
            print("Update download failed. Try again later.")
            return

        # temp dir normally cleans up on exit, but we're launching an
        # external process — move the installer out before the context manager exits
        stable_path = Path(tempfile.gettempdir()) / installer_path.name
        installer_path.replace(stable_path)

    launch_installer(stable_path)


def test_fetch_remote_version():
    """
    Test fetching remote version
    """
    remote = fetch_remote_version()
    assert remote is not None


if __name__ == "__main__":
    test_fetch_remote_version()


# TEST autoupdate function
# def test_update_check():
#     """
#     Tests possible Github update check
#     """
