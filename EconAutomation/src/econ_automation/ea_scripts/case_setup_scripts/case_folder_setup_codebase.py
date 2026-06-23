from pathlib import Path
from typing import Any, Callable
import logging
import shutil
import platform

from econ_automation.ea_scripts.case_setup_scripts.OFF_extraction_codebase import (
    CaseProfile,
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

_CASE_SUBFOLDERS = ["E-File", "Emails", "Report and Invoice", "Work Product"]


def _get_base_dir(base_filepaths: dict[str, Path], admin_bool: bool) -> Path:
    platform_key = "Mac" if platform.system() == "Darwin" else "Windows"
    key = (
        f"Test Claimant Directory {platform_key}"
        if admin_bool
        else f"Econ Claimant Directory {platform_key}"
    )
    return base_filepaths[key]


def find_existing_claimant_folder(
    case_profile: Any, base_filepaths: dict[str, Path], admin_bool: bool
) -> "Path | None":
    """
    Glob-matches an existing claimant folder by last name, first name.
    Returns the first match or None.
    """
    base_dir = _get_base_dir(base_filepaths, admin_bool)
    last_initial = case_profile.claimant_name_last_initial
    last_name = case_profile.claimant_name_last
    first_name = case_profile.claimant_name_first
    pattern = f"{last_initial}/{last_name}, {first_name}*"
    matches = list(base_dir.glob(pattern))
    return matches[0] if matches else None


def setup_new_case(
    sel_OFF_filepath: Path,
    base_filepaths: dict[str, Path],
    wb_template_dir: Path,
    admin_bool: bool,
    progress_callback: Callable[[str], None] | None = None,
) -> Path:
    """
    Sets up the econ claimant folder and copies workbook templates for a new claimant.
    Returns the path to the created claimant directory.
    """

    def _step(msg: str) -> None:
        if progress_callback:
            progress_callback(msg)

    _step("Extracting case information from OFF file...")
    case_profile = create_case_profile(sel_OFF_filepath)

    _step("Creating case folder structure...")
    claimant_dir = find_existing_claimant_folder(
        case_profile, base_filepaths, admin_bool
    )
    if claimant_dir is None:
        claimant_dir = initialize_case_folders(case_profile, base_filepaths, admin_bool)

    _step("Copying and configuring workbook templates...")
    work_product_dir = claimant_dir / "Work Products"
    work_product_dir.mkdir(exist_ok=True)
    save_claimant_workbook_templates(case_profile, wb_template_dir, work_product_dir)

    return claimant_dir


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

    econ_claimant_dir_base = _get_base_dir(base_filepaths, admin_bool)

    claimant_dir_filepath = f"{claimant_name_last_initial}/{claimant_name_last}, {claimant_name_first} ({attorney_name_first_initial}. {attorney_name_last})"
    claimant_dir = str(Path.joinpath(econ_claimant_dir_base, claimant_dir_filepath))

    try:
        Path(claimant_dir).mkdir(parents=True, exist_ok=True)
        for sub in _CASE_SUBFOLDERS:
            Path(claimant_dir + "/" + sub).mkdir(exist_ok=True)
    except PermissionError:
        logger.error("Permission denied to create claimant directory: %s", claimant_dir)
        raise

    return claimant_dir


def save_claimant_workbook_templates(
    case_profile: Any, wb_template_dir: Path, target_dir: Path
) -> None:
    """
    Saves claimant-specific template workbooks to target_dir (typically the Work Product subfolder).
    """
    for wb_template in wb_template_dir.iterdir():
        if wb_template.is_file() and wb_template.suffix in (
            ".xlsx",
            ".xlsm",
            ".xltx",
            ".xltm",
        ):
            if wb_template.stem == "Case_Variables":
                create_case_variables_excel_sheet(case_profile, wb_template, target_dir)
            else:
                target_path = target_dir / wb_template.name
                if target_path.exists():
                    logger.warning(
                        "Skipping %s: already exists in target directory.",
                        wb_template.name,
                    )
                else:
                    claimant_wb = shutil.copy2(wb_template, target_dir)
                    claimant_wb_path = Path(claimant_wb)
                    prepare_claimant_workbooks(case_profile, claimant_wb_path)


def prepare_claimant_workbooks(case_profile: Any, claimant_wb_path: Path) -> None:
    """
    Processes each non-"Case_Variables" workbook saved in the private claimant folder, adding case variable info where appropriate.
    """
    if claimant_wb_path.stem == "PV2_Current":
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
    elif claimant_wb_path.stem == "WorkingCalc_Current":
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


def create_folder_only(
    case_profile: Any,
    base_filepaths: dict[str, Path],
    admin_bool: bool,
    progress_callback: Callable[[str], None] | None = None,
) -> Path:
    """
    Creates the claimant folder (+ standard subfolders) without touching workbooks.
    Reuses an existing folder if one is found via glob match.
    """

    def _step(msg: str) -> None:
        if progress_callback:
            progress_callback(msg)

    _step("Checking for existing claimant folder...")
    claimant_dir = find_existing_claimant_folder(
        case_profile, base_filepaths, admin_bool
    )
    if claimant_dir is None:
        _step("Creating claimant folder structure...")
        claimant_dir = initialize_case_folders(case_profile, base_filepaths, admin_bool)
    else:
        _step("Using existing claimant folder...")
        for sub in _CASE_SUBFOLDERS:
            (claimant_dir / sub).mkdir(exist_ok=True)
    return claimant_dir


def setup_workbooks_from_profile(
    case_profile: Any,
    base_filepaths: dict[str, Path],
    wb_template_dir: Path,
    admin_bool: bool,
    progress_callback: Callable[[str], None] | None = None,
) -> Path:
    """
    Copies and configures workbook templates for a CaseProfile that was not sourced from an OFF.
    Checks for an existing claimant folder first; creates one if absent.
    Workbooks are placed in the Work Product subfolder.
    """

    def _step(msg: str) -> None:
        if progress_callback:
            progress_callback(msg)

    _step("Checking for existing claimant folder...")
    claimant_dir = find_existing_claimant_folder(
        case_profile, base_filepaths, admin_bool
    )
    if claimant_dir is None:
        _step("Creating claimant folder structure...")
        claimant_dir = initialize_case_folders(case_profile, base_filepaths, admin_bool)
    else:
        _step("Using existing claimant folder...")
        for sub in _CASE_SUBFOLDERS:
            (claimant_dir / sub).mkdir(exist_ok=True)

    _step("Copying and configuring workbook templates...")
    work_product_dir = claimant_dir / "Work Products"
    work_product_dir.mkdir(exist_ok=True)
    save_claimant_workbook_templates(case_profile, wb_template_dir, work_product_dir)
    return claimant_dir


def make_case_profile_from_basic_info(data: dict) -> CaseProfile:
    """
    Constructs a minimal CaseProfile from user-supplied form data (no OFF required).
    All fields not present in data default to empty string; __post_init__ derives
    name variants, pronouns, etc. automatically.
    """
    gender_map = {"M": "Male", "F": "Female"}
    claimant_sex = gender_map.get(data.get("gender", ""), "")
    attorney_sex = gender_map.get(data.get("attorney_gender", ""), "")

    dob_short, dob_long = OFFExtractor._format_date(data.get("dob", ""))
    doi_short, doi_long = OFFExtractor._format_date(data.get("doi", ""))
    ref_short, ref_long = OFFExtractor._format_date(data.get("reference_date", ""))

    trial_date_short = ref_short if data.get("trial_date_bool") else ""
    trial_date_long = ref_long if data.get("trial_date_bool") else ""

    attorney_first = data.get("attorney_name_first", "")
    attorney_last = data.get("attorney_name_last", "")

    return CaseProfile(
        claimant_name_first=data.get("claimant_name_first", ""),
        claimant_name_last=data.get("claimant_name_last", ""),
        claimant_sex=claimant_sex,
        claimant_DOB_short=dob_short,
        claimant_DOB_long=dob_long,
        claimant_DOI_short=doi_short,
        claimant_DOI_long=doi_long,
        reference_date_short=ref_short,
        reference_date_long=ref_long,
        trial_date_short=trial_date_short,
        trial_date_long=trial_date_long,
        attorney_name_first=attorney_first,
        attorney_name_last=attorney_last,
        attorney_sex=attorney_sex,
    )
