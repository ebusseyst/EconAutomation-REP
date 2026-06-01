from pathlib import Path
from typing import Any
import logging
import shutil
import platform

from econ_automation.ea_scripts.case_setup_scripts.OFF_extraction_codebase import (
    OFFExtractor,
)
from econ_automation.ea_scripts.case_setup_scripts.case_variables_creation_codebase import (
    create_case_variables_excel_sheet,
)

from econ_automation.ea_scripts.case_setup_scripts.workbook_setup_scripts import (
    set_PV2_case_variables,
    set_WC_case_variables,
)

logger = logging.getLogger(__name__)


def setup_new_case(
    sel_OFF_filepath: Path,
    base_filepaths: dict[str, Path],
    wb_template_dir: Path,
    admin_bool: bool,
) -> None:
    """
    Sets up the econ claimant folder and copies workbook templates for a new claimant.
    """
    case_profile = create_case_profile(sel_OFF_filepath)

    claimant_dir = initialize_case_folders(case_profile, base_filepaths, admin_bool)

    save_claimant_workbook_templates(case_profile, wb_template_dir, claimant_dir)


def create_case_profile(sel_OFF_filepath: Path) -> Any:
    """
    Returns the case_profile dataclass from the selected OFF.
    """
    OFF_extractor = OFFExtractor(sel_OFF_filepath)
    return OFF_extractor.case_profile


def initialize_case_folders(
    case_profile: Any, base_filepaths: dict[str, Path], admin_bool: bool
) -> Path:
    """
    Creates the claimant folder structure based on the case_profile dataclass.
    """
    claimant_name_first = case_profile.claimant_name_first
    claimant_name_last = case_profile.claimant_name_last
    claimant_name_last_initial = case_profile.claimant_name_last_initial
    attorney_name_last = case_profile.attorney_name_last
    attorney_name_first_initial = case_profile.attorney_name_first_initial

    platform_key = "Mac" if platform.system() == "Darwin" else "Windows"
    if admin_bool:
        econ_claimant_dir_base = base_filepaths[
            f"Test Claimant Directory {platform_key}"
        ]
    else:
        econ_claimant_dir_base = base_filepaths[
            f"Econ Claimant Directory {platform_key}"
        ]

    claimant_dir_filepath = f"{claimant_name_last_initial}/{claimant_name_last}, {claimant_name_first} ({attorney_name_first_initial}. {attorney_name_last})"
    claimant_dir = Path.joinpath(econ_claimant_dir_base, claimant_dir_filepath)

    claimant_dir.mkdir(parents=True, exist_ok=True)

    return claimant_dir


def save_claimant_workbook_templates(
    case_profile: Any, wb_template_dir: Path, claimant_dir: Path
) -> None:
    """
    Saves claimant-specific template workbooks to private claimant folder.
    """
    for wb_template in wb_template_dir.iterdir():
        if wb_template.is_file() and (
            wb_template.suffix == ".xlsx" or wb_template.suffix == ".xlsm"
        ):
            if wb_template.name == "Case_Variables.xlsx":
                create_case_variables_excel_sheet(
                    case_profile, wb_template, claimant_dir
                )
            else:
                claimant_wb = shutil.copy2(wb_template, claimant_dir)
                claimant_wb_path = Path(claimant_wb)
                prepare_claimant_workbooks(case_profile, claimant_wb_path)


def prepare_claimant_workbooks(case_profile: Any, claimant_wb_path: Path) -> None:
    """
    Processes each non-"Case_Variables" workbook saved in the private claimant folder, adding case variable info where appropriate.
    """
    if claimant_wb_path.name == "PV2_Current.xlsm":
        new_wb_name = f"{case_profile.claimant_name_last}{case_profile.claimant_name_first_initial} - {claimant_wb_path.name}"
        final_path = claimant_wb_path.parent / new_wb_name
        if final_path.exists():
            logger.warning(
                "Skipping %s: %s already exists.", claimant_wb_path.name, final_path
            )
            claimant_wb_path.unlink()
            return
        set_PV2_case_variables(case_profile, claimant_wb_path)
        claimant_wb_path.rename(final_path)
    elif claimant_wb_path.name in (
        "WorkingCalc_Current.xlsm",
        "WorkingCalc_Current.xlsx",
    ):
        new_wb_name = f"{case_profile.claimant_name_last}{case_profile.claimant_name_first_initial} - {claimant_wb_path.name}"
        final_path = claimant_wb_path.parent / new_wb_name
        if final_path.exists():
            logger.warning(
                "Skipping %s: %s already exists.", claimant_wb_path.name, final_path
            )
            claimant_wb_path.unlink()
            return
        set_WC_case_variables(case_profile, claimant_wb_path)
        claimant_wb_path.rename(final_path)
