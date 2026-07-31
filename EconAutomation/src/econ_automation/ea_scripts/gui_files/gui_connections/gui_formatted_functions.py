from pathlib import Path
from typing import Callable
import platform

from PySide6.QtWidgets import QFileDialog, QMainWindow

from econ_automation.ea_scripts.case_setup_scripts.case_folder_setup_codebase import (
    setup_new_case,
)
from econ_automation.ea_scripts.file_system_scripts.file_system_codebase import (
    FileSystemCore,
)


def select_OFF_file_modal(ea_main_window: QMainWindow):
    """
    Allows the user to select a file to load, and updates the display.

    Args:
        ea_main_window (QMainWindow): The main window.
    """
    claimant_name = ""
    file_path = ""

    file_path, _ = QFileDialog.getOpenFileName(
        parent=ea_main_window,
        caption="Select File",
        dir=r"S:/Shared Folders/Shared Documents/Claimant Folder",
        filter="Word Files (*.docx)",
    )
    if file_path:
        path_obj = Path(file_path)
        parent_dir = path_obj.parent
        claimant_dir_name = parent_dir.stem
        parts = claimant_dir_name.split(",", 1)
        if len(parts) == 2:
            claimant_name = parts[1].strip() + " " + parts[0].strip()
        else:
            claimant_name = claimant_dir_name.strip()

    return claimant_name, file_path


def select_claimant_folder_modal(self, title: str) -> str:
    """Opens a modal folder selection dialog."""
    foldername = QFileDialog.getExistingDirectory(
        self,
        caption=title,
        dir=str(self.econ_cases_path),
    )

    if foldername:
        return str(Path(foldername).resolve())
    return ""


def create_case_function(
    OFF_filepath: str,
    admin_bool: bool = False,
    progress_callback: Callable[[str], None] | None = None,
) -> Path:
    """
    Handles the request to create a new case - adds new folder structure and saves Excel templates for the case.
    Returns the path to the created claimant directory.

    Args:
        OFF_filepath (str): The absolute filepath of the OFF file.
    """
    fs = FileSystemCore()
    base_filepaths = fs.main_filepaths_dict["base_filepaths"]
    platform_key = "Mac" if platform.system() == "Darwin" else "Windows"
    wb_template_dir = fs.main_filepaths_dict["wb_template_dir"][platform_key]
    return setup_new_case(
        sel_OFF_filepath=Path(OFF_filepath),
        base_filepaths=base_filepaths,
        wb_template_dir=wb_template_dir,
        admin_bool=admin_bool,
        progress_callback=progress_callback,
    )
