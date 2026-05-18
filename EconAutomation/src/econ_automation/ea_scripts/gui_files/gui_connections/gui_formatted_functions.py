from pathlib import Path

from PySide6.QtWidgets import QFileDialog

from econ_automation.ea_scripts.case_setup_scripts.case_folder_setup_codebase import (
    setup_new_case,
)
from econ_automation.ea_scripts.report_merge_scripts.report_merge_codebase import (
    merge_reports_core,
)

from econ_automation.ea_scripts.gui_files.gui_core.gui_core_codebase import (
    EAMainWindow,
)
from econ_automation.ea_scripts.gui_files.gui_connections.merge_config_codebase import (
    MergeConfig,
)

# Shael Private Claimant Dir- C:/Users/shaelwolfson/OneDrive - Stokes & Associates/Leone Deogracias's files - Econ
# Chris Private Claimant Dir - C:/Users/ChristopherJohnson/OneDrive - Stokes & Associates/Leone Deogracias's files - Econ
# Econ Public Claimant Dir - S:/Shared Folders/Shared Documents/Economics Claimant Folder
# Econ Templates Parent Dir - S:/Shared Folders/Shared Documents/Economics Claimant Folder/00-EconAutomation Templates
# Econ Excel Templates Dir - S:/Shared Folders/Shared Documents/Economics Claimant Folder/00-EconAutomation Templates/EconAutomation Excel Templates
# Econ Report Templates Dir - S:/Shared Folders/Shared Documents/Economics Claimant Folder/00-EconAutomation Templates/EconAutomation Report Templates

# DEBUG: REPLACE CONSTANTS WITH DYNAMIC INTEGRATED VARS
BASE_FILEPATHS = {
    "Private Directory": Path(
        f"{Path.home()}/OneDrive - Stokes & Associates/Leone Deogracias's files - Econ"
    ),
    "Public Directory": Path(
        r"S:/Shared Folders/Shared Documents/Economics Claimant Folder"
    ),
}
WB_TEMPLATE_DIR = Path(
    r"S:/Shared Folders/Shared Documents/Economics Claimant Folder/00-EconAutomation Templates/EconAutomation Excel Templates"
)


def select_OFF_file_function(ea_main_window: EAMainWindow):
    """
    Allows the user to select a file to load, and updates the display.

    Args:
        ea_main_window (EAMainWindow): The main window.
    """
    claimant_name = ""
    file_path = ""

    file_path, _ = QFileDialog.getOpenFileName(
        parent=ea_main_window,
        caption="Select File",
        # DEBUG - NEED TO ADD CLAIMANT FOLDER FILEPATH
        # dir=r"S:/Shared Folders/Shared Documents/Claimant Folder",
        dir="",
        filter="Word Files (*.docx)",
    )
    if file_path:
        path_obj = Path(file_path[0])
        parent_dir = path_obj.parent
        claimant_dir_name = parent_dir.stem
        claimant_name_last, claimant_name_first = claimant_dir_name.split(",")
        claimant_name = claimant_name_first.strip() + " " + claimant_name_last.strip()

    return claimant_name, file_path


def create_case_function(
    OFF_filepath: str,
    base_filepaths: dict[str, Path] = BASE_FILEPATHS,
    wb_template_dir: Path = WB_TEMPLATE_DIR,
) -> None:
    """
    Handles the request to create a new case - adds new folder structure and saves Excel templates for the case.

    Args:
        OFF_filepath (str): The absolute filepath of the OFF file.
        base_filepaths (dict): The Econ department claimant folders' base filepaths with named keys.
        wb_template_dir (Path): The Econ department workbook templates' parent directory filepath.
    """
    setup_new_case(
        sel_OFF_filepath=Path(OFF_filepath),
        base_filepaths=base_filepaths,
        wb_template_dir=wb_template_dir,
    )


def return_merge_config(ea_main_window: EAMainWindow) -> MergeConfig:
    """
    Extracts current merge configuration based on the GUI's checkboxes and comboboxes and returns it as a MergeConfig dataclass instance.

    Args:
        ea_main_window (EAMainWindow): The UI of the main window.
    """
    merge_config = MergeConfig()

    merge_config.earnings_projection_config = (
        ea_main_window.ui.ea_reportmerge_projectiontype_combobox.currentText()
    )

    merge_config.reference_type_config = (
        ea_main_window.ui.ea_reportmerge_referencetype_combobox.currentText()
    )

    merge_config.PVLCP_report_config = (
        ea_main_window.ui.ea_reportmerge_reporttypes_PVLCP_checkbox.isChecked()
    )
    merge_config.PVearnings_report_config = (
        ea_main_window.ui.ea_reportmerge_reporttypes_PVearnings_checkbox.isChecked()
    )

    merge_config.base1_config = (
        ea_main_window.ui.ea_reportmerge_base1_checkbox.isChecked()
    )
    merge_config.base2_config = (
        ea_main_window.ui.ea_reportmerge_base2_checkbox.isChecked()
    )
    merge_config.base3_config = (
        ea_main_window.ui.ea_reportmerge_base3_checkbox.isChecked()
    )

    merge_config.credit1_config = (
        ea_main_window.ui.ea_reportmerge_credit1_checkbox.isChecked()
    )
    merge_config.credit2_config = (
        ea_main_window.ui.ea_reportmerge_credit2_checkbox.isChecked()
    )
    merge_config.credit3_config = (
        ea_main_window.ui.ea_reportmerge_credit3_checkbox.isChecked()
    )

    merge_config.meals_config = (
        ea_main_window.ui.ea_reportmerge_meals_checkbox.isChecked()
    )
    merge_config.benefits_config = (
        ea_main_window.ui.ea_reportmerge_benefits_checkbox.isChecked()
    )

    merge_config.taxstatus_config = (
        ea_main_window.ui.ea_reportmerge_taxstatus_checkbox.isChecked()
    )

    return merge_config


def merge_reports_function(
    ea_main_window: EAMainWindow, merge_config: MergeConfig
) -> None:
    """
    Merges the selected reports based on the merge configuration.

    Args:
        ea_main_window (EAMainWindow): The main window instance.
        merge_config (MergeConfig): The modified merge configuration dataclass.
    """
