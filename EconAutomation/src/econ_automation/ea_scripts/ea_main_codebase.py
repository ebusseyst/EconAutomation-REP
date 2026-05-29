from dataclasses import make_dataclass, fields, is_dataclass
import logging
from pathlib import Path
from typing import Any
from importlib.metadata import version, metadata

from pydantic import BaseModel

from econ_automation.ea_scripts.file_system_scripts.file_system_codebase import (
    FileSystemCore as fsc,
)
from econ_automation.ea_scripts.case_setup_scripts.case_folder_setup_codebase import (
    setup_new_case,
)

from econ_automation.ea_scripts.data_extraction_scripts.case_variables_extraction_codebase import (
    CaseVariablesExtractor,
)
from econ_automation.ea_scripts.data_extraction_scripts.working_calc_extraction_codebase import (
    WorkingCalcExtractor,
)
from econ_automation.ea_scripts.data_extraction_scripts.pv2_extraction_codebase import (
    PV2Extractor,
)
from econ_automation.ea_scripts.data_extraction_scripts.hhspv_extraction_codebase import (
    HHSPVExtractor,
)

from econ_automation.ea_scripts.report_merge_scripts.report_merge_codebase import (
    merge_reports_core,
)

APP_NAME = metadata("econ_automation").get("Name")
APP_VERSION = version("econ_automation")
APP_FULL_NAME = f"{APP_NAME} v{APP_VERSION}"

WORKBOOK_OUTPUTS_SHEET_NAME: str = "REPORT_OUTPUTS"

logger = logging.getLogger(__name__)

# Glob patterns used by build_selected_files_dict to locate workbooks inside a
# claimant directory.  Each list is tried in order; first match wins.
_WORKBOOK_GLOB_PATTERNS: dict[str, list[str]] = {
    "CASE_VARIABLES": ["*Case Variables*.xlsx", "*Case_Variables*.xlsx"],
    "WORKING_CALC":   ["*WorkingCalc*.xlsm", "*WorkingCalc*.xlsx"],
    "PV2":            ["*PV2*.xlsm"],
    "HHSPV":          ["*HHS_PV*.xlsx"],
}

_DEFAULT_SELECTED_FILES: dict[str, dict[str, Path]] = {
    "workbook_filepaths": {
        "CASE_VARIABLES": Path("/Users/ericmacbook/Documents/GitHub/EconAutomation-REP/EconAutomation/ea_outputs/private_claimant_directories/G/Gaston, Casper (J. D’Attorney)/GastonC - Case Variables.xlsx"),
        "WORKING_CALC": Path("/Users/ericmacbook/Documents/GitHub/EconAutomation-REP/EconAutomation/ea_outputs/private_claimant_directories/G/Gaston, Casper (J. D’Attorney)/GastonC - WorkingCalc_Current.xlsm"),
        "PV2": Path("/Users/ericmacbook/Documents/GitHub/EconAutomation-REP/EconAutomation/ea_outputs/private_claimant_directories/G/Gaston, Casper (J. D’Attorney)/GastonC - PV2_Current.xlsm"),
        "HHSPV": Path("/Users/ericmacbook/Documents/GitHub/EconAutomation-REP/EconAutomation/ea_outputs/private_claimant_directories/G/Gaston, Casper (J. D’Attorney)/HHS_PV_New (color coded).xlsx")
    },
    "template_filepaths": {
        "PV_EARNINGS_TEMPLATE": Path("/Users/ericmacbook/Documents/GitHub/EconAutomation-REP/EconAutomation/src/supporting_docs/econ_report_templates/PV_Earnings_Report_Template.docx"),
        "PVLCP_TEMPLATE": Path("/Users/ericmacbook/Documents/GitHub/EconAutomation-REP/EconAutomation/src/supporting_docs/econ_report_templates/PVLCP_Report_Template.docx")
    },
    "output_filepaths": {
        "SAMPLE_CLAIMANT_DIR": Path("/Users/ericmacbook/Documents/GitHub/EconAutomation-REP/EconAutomation/ea_outputs/private_claimant_directories/G/Gaston, Casper (J. D’Attorney)")
    }
}


# ── Primary entry points ──────────────────────────────────────────────────────


def setup_new_case_workflow(
    sel_OFF_filepath: Path,
    base_filepaths: dict[str, Path],
    wb_template_dir: Path,
) -> None:
    """
    Creates the claimant folder structure, copies workbook templates, and
    populates them from the selected OFF file.

    Args:
        sel_OFF_filepath: Path to the selected Open File Form (.docx).
        base_filepaths: Base directory paths for the claimant case folders.
        wb_template_dir: Parent directory containing the Excel workbook templates.

    Raises:
        ValueError: If sel_OFF_filepath does not point to an existing file.
    """
    if not sel_OFF_filepath.is_file():
        raise ValueError(f"OFF file not found: {sel_OFF_filepath}")
    setup_new_case(sel_OFF_filepath, base_filepaths, wb_template_dir)


def build_selected_files_dict(
    claimant_dir: Path,
    requested_template_keys: list[str] | None = None,
) -> dict[str, dict[str, Path]]:
    """
    Builds a selected_files_dict for run_extraction_and_report_merge by
    scanning claimant_dir for known workbook patterns and resolving template
    paths from ea_config.yaml.

    Args:
        claimant_dir: Path to the selected claimant's working directory.
        requested_template_keys: Template keys to include (e.g.
            ["PV_EARNINGS_TEMPLATE"]).  None includes all configured templates.

    Returns:
        A dict with "workbook_filepaths", "template_filepaths", and
        "output_filepaths" ready for run_extraction_and_report_merge.
    """
    workbook_fps: dict[str, Path] = {}
    for key, patterns in _WORKBOOK_GLOB_PATTERNS.items():
        for pattern in patterns:
            matches = list(claimant_dir.glob(pattern))
            if matches:
                workbook_fps[key] = matches[0]
                break
        else:
            logger.warning("build_selected_files_dict: no match for %s in %s", key, claimant_dir)

    fs = fsc()
    all_template_fps: dict[str, Path] = fs.main_filepaths_dict["template_filepaths"]
    if requested_template_keys is not None:
        template_fps = {k: v for k, v in all_template_fps.items() if k in requested_template_keys}
    else:
        template_fps = all_template_fps

    return {
        "workbook_filepaths": workbook_fps,
        "template_filepaths": template_fps,
        "output_filepaths": {"CLAIMANT_DIR": claimant_dir},
    }


def run_extraction_and_report_merge(
    selected_files_dict: dict[str, dict[str, Path]] = _DEFAULT_SELECTED_FILES,
    gui_overrides: dict[str, Any] | None = None,
) -> None:
    """
    Runs the full data extraction and report merge workflow: initializes the
    file system, extracts data from the selected Excel workbooks, flattens it
    into a single dataclass, and renders Word report templates.

    Args:
        selected_files_dict: Maps file-category keys to lists of named file
            identifiers as defined in ea_config.yaml. Defaults to
            _DEFAULT_SELECTED_FILES.
        gui_overrides: Maps template stem → PVEarningsToggles (or analogous
            toggles object for other templates).  When provided, the context
            builder for that template uses GUI widget state instead of
            inferring toggles from the extracted dataclass.
    """
    file_system_core = fsc()
    main_filepaths_dict = file_system_core.main_filepaths_dict

    selected_filepaths_dict = _select_relevant_filepaths(
        selected_files_dict, main_filepaths_dict
    )

    extractors = _initialize_extractors(
        selected_filepaths_dict=selected_filepaths_dict,
        temp_dir_filepath=file_system_core.temp_dir_filepath,
    )

    econ_data_list = _get_all_reformatted_data(extractors)
    ea_main_dataclass = _flatten_all_extracted_data(econ_data_list)
    image_paths = _collect_image_paths(extractors)

    _generate_reports(
        ea_main_dataclass=ea_main_dataclass,
        selected_template_filepaths=list(
            selected_filepaths_dict["template_filepaths"].values()
        ),
        selected_output_filepaths=list(
            selected_filepaths_dict["output_filepaths"].values()
        ),
        gui_overrides=gui_overrides,
        image_paths=image_paths,
    )


# ── Private helpers ───────────────────────────────────────────────────────────


def _select_relevant_filepaths(
    selected_files_dict: dict[str, dict[str, Path]],
    main_filepaths_dict: dict[str, dict[str, Path]],
) -> dict[str, dict[str, Path]]:
    """
    Selects relevant filepaths from main_filepaths_dict based on user-selected
    items, returns dict[str, dict[str, Path]].

    Args:
        selected_files_dict: Dictionary of user-selected file names.
        main_filepaths_dict: Dictionary of filepaths.

    Returns:
        Dictionary of selected filepaths, keyed by category.
    """
    selected_filepaths_dict = {}

    for category, filenames_dict in selected_files_dict.items():
        if category == "output_filepaths":
            selected_filepaths_dict[category] = filenames_dict
            continue
        temp_sel_fps_dict = {}
        for filename, filepath in filenames_dict.items():
            if filename in main_filepaths_dict[category].keys():
                temp_sel_fps_dict[filename] = filepath
        selected_filepaths_dict[category] = temp_sel_fps_dict

    return selected_filepaths_dict


def _initialize_extractors(
    selected_filepaths_dict: dict[str, dict[str, Path]],
    temp_dir_filepath: Path,
) -> dict[str, Any]:
    """
    Initializes all data extractors and returns them as a dict.

    # TEMP: THIS WHOLE FUNCTION IS A STAND-IN UNTIL THE FRONTEND
    # (AND MULTI-OFF EXTRACTION SUPPORT) IS DEVELOPED.

    Args:
        selected_filepaths_dict: Dictionary of selected filepaths by category.
        temp_dir_filepath: Path to the temporary directory for workbook copies.

    Returns:
        Dictionary of initialized extractor instances keyed by short name.
    """
    workbook_fps = selected_filepaths_dict["workbook_filepaths"]

    return {
        "case_variables": CaseVariablesExtractor(
            case_variables_filepath=workbook_fps["CASE_VARIABLES"],
            workbook_outputs_sheet_name=WORKBOOK_OUTPUTS_SHEET_NAME,
            temp_dir_path=temp_dir_filepath,
        ),
        "working_calc": WorkingCalcExtractor(
            working_calc_filepath=workbook_fps["WORKING_CALC"],
            workbook_outputs_sheet_name=WORKBOOK_OUTPUTS_SHEET_NAME,
            temp_dir_path=temp_dir_filepath,
        ),
        "pv2": PV2Extractor(
            pv2_filepath=workbook_fps["PV2"],
            workbook_outputs_sheet_name=WORKBOOK_OUTPUTS_SHEET_NAME,
            temp_dir_path=temp_dir_filepath,
        ),
        "hhspv": HHSPVExtractor(
            hhspv_filepath=workbook_fps["HHSPV"],
            workbook_outputs_sheet_name=WORKBOOK_OUTPUTS_SHEET_NAME,
            temp_dir_path=temp_dir_filepath,
        ),
    }


def _collect_image_paths(extractors: dict[str, Any]) -> dict[str, Path]:
    """Collects all extracted image paths from every extractor into one dict."""
    image_paths: dict[str, Path] = {}
    for extractor in extractors.values():
        image_paths.update(getattr(extractor, "extracted_image_paths", {}))
    return image_paths


def _get_all_reformatted_data(extractors: dict[str, Any]) -> list[Any]:
    """Returns all reformatted data from all extractors as a list of dataclasses."""
    return [
        extractors["case_variables"].workbook_dataclass,
        extractors["working_calc"].workbook_dataclass,
        extractors["pv2"].workbook_dataclass,
        extractors["hhspv"].workbook_dataclass,
    ]


def _flatten_all_extracted_data(econ_data_list: list[Any]) -> Any:
    """
    Returns a flattened dataclass of all extracted data.

    Args:
        econ_data_list: List of dataclasses to flatten.

    Returns:
        Single flattened dataclass containing all extracted fields.
    """
    all_fields = []
    all_values = {}
    for dc in econ_data_list:
        if isinstance(dc, BaseModel):
            for name in type(dc).model_fields.keys():
                all_fields.append((name, Any))
                all_values[name] = getattr(dc, name)
        elif is_dataclass(dc):
            for f in fields(dc):
                all_fields.append((f.name, Any))
                all_values[f.name] = getattr(dc, f.name)
        else:
            raise TypeError(f"Unsupported type in econ_data_list: {type(dc)}")

    EconAutomationData = make_dataclass("EconAutomationData", all_fields)
    return EconAutomationData(**all_values)


def _generate_reports(
    ea_main_dataclass: Any,
    selected_template_filepaths: list[Path],
    selected_output_filepaths: list[Path],
    gui_overrides: dict[str, Any] | None = None,
    image_paths: dict[str, Path] | None = None,
) -> None:
    """
    Renders each selected report template with extracted data and saves output files.

    Args:
        ea_main_dataclass: Flattened dataclass containing all extracted/reformatted data.
        selected_template_filepaths: Paths to Word template files (.docx).
        selected_output_filepaths: Paths to output directories for each template.
        gui_overrides: Forwarded to merge_reports_core; maps template stem →
            toggles object.
        image_paths: Maps template variable name → Path for chart/table images.
    """
    try:
        merge_reports_core(
            ea_main_dataclass=ea_main_dataclass,
            selected_template_filepaths=selected_template_filepaths,
            selected_output_filepaths=selected_output_filepaths,
            gui_overrides=gui_overrides,
            image_paths=image_paths,
        )
    except TypeError:
        logger.exception("_generate_reports: Input data type error.")
        raise
