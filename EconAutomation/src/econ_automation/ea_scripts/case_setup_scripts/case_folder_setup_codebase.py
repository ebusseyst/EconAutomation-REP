from pathlib import Path
from typing import Any
import shutil

from econ_automation.ea_scripts.case_setup_scripts.OFF_extraction_codebase import (
    OFFExtractor,
)
from econ_automation.ea_scripts.case_setup_scripts.case_variables_creation_codebase import (
    create_case_variables_excel_sheet,
)


def setup_new_case(
    sel_OFF_filepath: Path, base_filepaths: dict[str, Path], wb_template_dir: Path
) -> None:
    """
    Fully sets up private and public claimant folders for new claimant.
    """
    case_profile = create_case_profile(sel_OFF_filepath)

    private_claimant_dir, public_claimant_dir = initialize_case_folders(
        case_profile, base_filepaths
    )

    save_claimant_workbook_templates(
        case_profile, wb_template_dir, private_claimant_dir
    )


def create_case_profile(sel_OFF_filepath: Path) -> Any:
    """
    Returns the case_profile dataclass from the selected OFF.
    """
    OFF_extractor = OFFExtractor(sel_OFF_filepath)
    return OFF_extractor.case_profile


def initialize_case_folders(
    case_profile: Any, base_filepaths: dict[str, Path]
) -> tuple[Path, Path]:
    """
    Creates the case folder structure based on the case_profile dataclass.
    """
    claimant_name_first = case_profile.claimant_name_first
    claimant_name_last = case_profile.claimant_name_last
    claimant_name_last_initial = case_profile.claimant_name_last_initial
    attorney_name_last = case_profile.attorney_name_last
    attorney_name_first_initial = case_profile.attorney_name_first_initial

    # "Private" claimant folder
    private_econ_folder_base = base_filepaths["Private Directory"]
    private_claimant_dir_filepath = f"{claimant_name_last_initial}/{claimant_name_last}, {claimant_name_first} ({attorney_name_first_initial}. {attorney_name_last})"
    private_claimant_dir = Path.joinpath(
        private_econ_folder_base, private_claimant_dir_filepath
    )

    private_claimant_dir.mkdir(parents=True, exist_ok=True)

    # "Public" claimant folder
    public_econ_folder_base = base_filepaths["Public Directory"]
    public_claimant_dir_filepath = f"{claimant_name_last_initial}/{claimant_name_last}, {claimant_name_first} ({attorney_name_first_initial}. {attorney_name_last})"
    public_claimant_dir = Path.joinpath(
        public_econ_folder_base, public_claimant_dir_filepath
    )

    public_claimant_dir.mkdir(parents=True, exist_ok=True)

    return private_claimant_dir, public_claimant_dir


def save_claimant_workbook_templates(
    case_profile: Any, wb_template_dir: Path, private_claimant_dir: Path
) -> None:
    """
    Saves claimant-specific template workbooks to private claimant folder.
    """
    for wb_template in wb_template_dir.iterdir():
        if wb_template.is_file() and wb_template.suffix == ".xlsx":
            if wb_template.name == "Case Variables.xlsx":
                create_case_variables_excel_sheet(
                    case_profile, wb_template, private_claimant_dir
                )
            else:
                claimant_wb = shutil.copy2(wb_template, private_claimant_dir)
                claimant_wb_path = Path(claimant_wb)
                new_wb_name = f"{case_profile.claimant_name_last}{case_profile.claimant_name_first_initial} - {Path(wb_template).name}"
                claimant_wb_path.rename(claimant_wb_path.parent.joinpath(new_wb_name))
