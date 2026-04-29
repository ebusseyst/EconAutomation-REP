import logging
import sys
from pathlib import Path
from typing import Any

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
        self.ea_config_data = self.load_ea_config()

        self.OFF_filepaths = self.ea_config_data["OFF_FILEPATHS"]
        self.workbook_filepaths = self.ea_config_data["WORKBOOKS"]
        self.template_filepaths = self.ea_config_data["TEMPLATES"]
        self.output_filepaths = self.ea_config_data["OUTPUTS"]

        self.main_filepaths_dict = {
            "WORKBOOKS": self.workbook_filepaths,
            "TEMPLATES": self.template_filepaths,
            "OUTPUTS": self.output_filepaths,
        }

    def load_ea_config(self) -> dict[str, dict[str, Any]]:
        """
        Loads ea_config.yaml and resolves paths to resources.
        """
        with open(obtain_resource_path("supporting_docs/ea_config.yaml"), "r") as f:
            ea_config_data = yaml.safe_load(f)

        OFF_filepaths = ea_config_data["OFF_filepaths"]
        workbook_filepaths = ea_config_data["workbook_filepaths"]
        template_filepaths = ea_config_data["template_filepaths"]
        output_filepaths = ea_config_data["output_filepaths"]

        for OFF_name, OFF_filepath in OFF_filepaths.items():
            OFF_filepaths[OFF_name] = obtain_resource_path(OFF_filepath, src_bool=True)

        for workbook_name, workbook_filepath in workbook_filepaths.items():
            workbook_filepaths[workbook_name] = obtain_resource_path(
                workbook_filepath, src_bool=True
            )

        for template_name, template_filepath in template_filepaths.items():
            template_filepaths[template_name] = obtain_resource_path(
                template_filepath, src_bool=True
            )

        for output_name, output_filepath in output_filepaths.items():
            output_filepaths[output_name] = obtain_resource_path(
                output_filepath, src_bool=False
            )

        return {
            "OFFs": OFF_filepaths,
            "WORKBOOKS": workbook_filepaths,
            "TEMPLATES": template_filepaths,
            "OUTPUTS": output_filepaths,
        }
