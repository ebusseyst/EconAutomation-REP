import logging
import sys
import tempfile
from pathlib import Path

import yaml

# Module's logger instance
logger = logging.getLogger(__name__)


# Load Project Root Directory
def obtain_project_root(marker_filename: str = "pyproject.toml") -> Path:
    """
    Resolve path to the project root directory.
    """
    current = Path(__file__).resolve()

    for parent in current.parents:
        if (parent / marker_filename).exists():
            return parent

    return current.parent


# Assigns Project Root Directory to constant
PROJECT_ROOT = obtain_project_root()


# Resource path function
def obtain_resource_path(relative_path: str, src_bool: bool = True) -> Path:
    """
    Resolve path to a bundled resource; works in dev and PyInstaller exe.
    """
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / relative_path

    if src_bool:
        return Path(PROJECT_ROOT / "src" / relative_path)

    return Path(PROJECT_ROOT / relative_path)


class FileSystemCore:
    def __init__(self):
        # Load ea_config.yaml
        self.main_filepaths_dict = self.load_ea_config()

        # Create Temporary Directory
        self.temp_dir, self.temp_dir_filepath = self.create_temp_directory(
            self.main_filepaths_dict["temp_dir_filepaths"]["TEMP_DIR"]
        )

    def create_temp_directory(
        self, temp_dir_filepath: Path
    ) -> tuple[tempfile.TemporaryDirectory, Path]:
        """
        Creates a temporary directory for storing tables and charts prior to report merge.
        """
        temp_directory = tempfile.TemporaryDirectory(
            dir=temp_dir_filepath, ignore_cleanup_errors=True
        )
        temp_dir_path = Path(temp_directory.name)
        return temp_directory, temp_dir_path

    def cleanup_temp_directory(self):
        """
        Deletes the temporary directory and its contents.
        """
        self.temp_dir.cleanup()

    def load_ea_config(self) -> dict[str, dict[str, Path]]:
        """
        Loads ea_config.yaml and resolves paths to resources.
        """
        filepaths_dict = {}
        with open(obtain_resource_path("supporting_docs/ea_config.yaml"), "r") as f:
            ea_config_data = yaml.safe_load(f)

        for filepath_key, filepath_dict in ea_config_data.items():
            if filepath_key == "output_filepaths":
                filepaths_dict[filepath_key] = self._resolve_file_paths(
                    filepath_dict, src_bool=False
                )

            elif filepath_key == "temp_dir_filepaths":
                filepaths_dict[filepath_key] = self._resolve_file_paths(
                    filepath_dict, src_bool=False
                )

            else:
                filepaths_dict[filepath_key] = self._resolve_file_paths(
                    filepath_dict, src_bool=True
                )

        return filepaths_dict

    def _resolve_file_paths(
        self, filepath_dict: dict[str, str], src_bool: bool = True
    ) -> dict[str, Path]:
        """
        Resolves paths to resources, including nested dictionaries.
        """
        resolved_filepaths = {}
        for name, filepath in filepath_dict.items():
            resolved_filepaths[name] = obtain_resource_path(filepath, src_bool=src_bool)
        return resolved_filepaths
