import logging
import os
import platform
import sys
import tempfile
from pathlib import Path

import yaml

logger = logging.getLogger(__name__)

EA_CONFIG_PATH = Path(
    r"S:/Shared Folders/Shared Documents/Economics Claimant Folder"
    r"/00-EconAutomation Reference Files/ea_config.yaml"
)


def obtain_project_root(marker_filename: str = "pyproject.toml") -> Path:
    """
    Resolve path to the project root directory.
    """
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / marker_filename).exists():
            return parent
    return current.parent


PROJECT_ROOT = obtain_project_root()


def obtain_resource_path(relative_path: str, src_bool: bool = True) -> Path:
    """
    Resolve path to a bundled resource; works in dev and PyInstaller exe.

    src_bool=True  → bundled read-only asset (templates, config): resolves
                     into sys._MEIPASS when frozen.
    src_bool=False → user-writable output/temp path: resolves into a
                     per-user app-data directory when frozen so the app can
                     write files even when installed under Program Files.
    """
    if hasattr(sys, "_MEIPASS"):
        if src_bool:
            return Path(sys._MEIPASS) / relative_path
        if platform.system() == "Windows":
            base = Path(os.environ.get("LOCALAPPDATA", Path.home())) / "EconAutomation"
        else:
            base = Path.home() / "Library" / "Application Support" / "EconAutomation"
        base.mkdir(parents=True, exist_ok=True)
        return base / relative_path

    if src_bool:
        return Path(PROJECT_ROOT / "src" / relative_path)

    return Path(PROJECT_ROOT / relative_path)


class FileSystemCore:
    def __init__(self):
        self.main_filepaths_dict = self.load_ea_config()
        self.temp_dir, self.temp_dir_filepath = self.create_temp_directory()

    def create_temp_directory(self) -> tuple[tempfile.TemporaryDirectory, Path]:
        """
        Creates a temporary directory in the OS default temp location for
        storing charts and tables prior to report merge.
        """
        temp_directory = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        return temp_directory, Path(temp_directory.name)

    def cleanup_temp_directory(self) -> None:
        """
        Deletes the temporary directory and its contents.
        """
        self.temp_dir.cleanup()

    def load_ea_config(self) -> dict[str, dict[str, Path]]:
        """
        Loads ea_config.yaml and resolves all paths.
        """
        with open(EA_CONFIG_PATH, "r") as f:
            ea_config_data = yaml.safe_load(f)

        return {
            key: self._resolve_file_paths(filepath_dict)
            for key, filepath_dict in ea_config_data.items()
        }

    def _resolve_file_paths(
        self, filepath_dict: dict[str, str]
    ) -> dict[str, Path]:
        """
        Resolves each path string to a Path via obtain_resource_path.
        Absolute paths (e.g. S:/...) resolve correctly because Path joining
        replaces the base when the right-hand side is absolute.
        """
        return {
            name: obtain_resource_path(filepath)
            for name, filepath in filepath_dict.items()
        }
