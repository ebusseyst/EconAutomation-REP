import logging
import tempfile
from pathlib import Path
import platform

import yaml

logger = logging.getLogger(__name__)

if platform.system() == "Darwin":
    EA_CONFIG_PATH = (
        Path.home()
        / "Library/CloudStorage/ShareFile-ShareFile/Shared Folders/Shared Documents/Economics Claimant Folder/00-EconAutomation Reference Files/ea_config.yaml"
    )
else:
    EA_CONFIG_PATH = Path(
        r"S:/Economics Claimant Folder/00-EconAutomation Reference Files/ea_config.yaml"
    )

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
        return {name: Path(filepath).expanduser() for name, filepath in filepath_dict.items()}
