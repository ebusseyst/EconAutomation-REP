from pathlib import Path

from PySide6.QtWidgets import QMainWindow, QFileDialog

from econ_automation.ea_scripts.case_setup_scripts.case_folder_setup_codebase import setup_new_case
from econ_automation.ea_scripts.gui_files.gui_core.current_ea_gui import Ui_ea_MainWindow

# Shael Private Claimant Dir- C:/Users/shaelwolfson/OneDrive - Stokes & Associates/Leone Deogracias's files - Econ
# Chris Private Claimant Dir - C:/Users/ChristopherJohnson/OneDrive - Stokes & Associates/Leone Deogracias's files - Econ
# Econ Public Claimant Dir - S:/Shared Folders/Shared Documents/Economics Claimant Folder
# Econ Templates Parent Dir - S:/Shared Folders/Shared Documents/Economics Claimant Folder/00-EconAutomation Templates
# Econ Excel Templates Dir - S:/Shared Folders/Shared Documents/Economics Claimant Folder/00-EconAutomation Templates/EconAutomation Excel Templates
# Econ Report Templates Dir - S:/Shared Folders/Shared Documents/Economics Claimant Folder/00-EconAutomation Templates/EconAutomation Report Templates

# DEBUG: REPLACE CONSTANTS WITH DYNAMIC INTEGRATED VARS
BASE_FILEPATHS = {
    "Private Directory": Path(f"{Path.home()}/OneDrive - Stokes & Associates/Leone Deogracias's files - Econ"),
    "Public Directory": Path(r"S:/Shared Folders/Shared Documents/Economics Claimant Folder")
}
WB_TEMPLATE_DIR = Path(r"S:/Shared Folders/Shared Documents/Economics Claimant Folder/00-EconAutomation Templates/EconAutomation Excel Templates")

def select_OFF_file_function(ui: Ui_ea_MainWindow, ea_main_window: QMainWindow):
    """
    Allows the user to select a file to load, and updates the display.

    Args:
        ui (Ui_ea_MainWindow): The UI of the main window.
        ea_main_window (QMainWindow): The main window.
    """
    file_path, _ = QFileDialog.getOpenFileName(
        parent=ea_main_window,
        caption="Select File",
        # DEBUG - NEED TO ADD CLAIMANT FOLDER FILEPATH
        # dir=r"S:/Shared Folders/Shared Documents/Claimant Folder",
        dir="",
        filter="Word Files (*.docx)",
    )
    if file_path:
        path_obj = Path(file_path)
        parent_dir = path_obj.parent
        claimant_dir_name = parent_dir.stem
        claimant_name_last, claimant_name_first = claimant_dir_name.split(",")
        claimant_name = claimant_name_first.strip() + " " + claimant_name_last.strip()
        
        ui.ea_setupcase_selectedOFF_label.setText(claimant_name)
        ui.ea_setupcase_selectedOFF_label.setToolTip(file_path)

def create_case_function(
    OFF_filepath: str, 
    base_filepaths: dict[str, Path] = BASE_FILEPATHS, 
    wb_template_dir: Path = WB_TEMPLATE_DIR
    ) -> None:
    """
    Handles the request to create a new case - adds new folder structure and saves Excel templates for the case.

    Args:
        OFF_filepath (str): The absolute filepath of the OFF file.
        base_filepaths (dict): The Econ department claimant folders' base filepaths with named keys.
        wb_template_dir (Path): The Econ department workbook templates' parent directory filepath.
    """
    setup_new_case(sel_OFF_filepath=Path(OFF_filepath), base_filepaths=base_filepaths, wb_template_dir=wb_template_dir)
    
# def 