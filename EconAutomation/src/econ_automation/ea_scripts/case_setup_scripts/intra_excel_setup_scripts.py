import logging
from pathlib import Path
from typing import Any

import openpyxl as opxl
from openpyxl.worksheet.worksheet import Worksheet

logger = logging.getLogger(__name__)


def load_working_calc_wb(
    case_profile: Any, claimant_dir: Path
) -> opxl.Workbook:
    """
    Loads the working calculator workbook for the case.
    """
    sel_working_calc_path = (
        claimant_dir
        / f"{case_profile.claimant_name_last}{case_profile.claimant_name_first_initial} - WorkingCalc_Current.xlsm"
    )
    return opxl.load_workbook(sel_working_calc_path)


def load_pv2_wb(
    case_profile: Any,
    claimant_dir: Path,
) -> opxl.Workbook:
    """
    Loads the PV2 workbook for the case.
    """
    sel_pv2_path = (
        claimant_dir
        / f"{case_profile.claimant_name_last}{case_profile.claimant_name_first_initial} - PV2_Current.xlsm"
    )
    return opxl.load_workbook(sel_pv2_path)


def write_if_cell_matches(
    worksheet: Worksheet,
    case_profile: Any,
    case_profile_attr: str,
    target_cell: str,
    condition_cell: str,
    condition_value: Any,
) -> None:
    """
    Writes the value of case_profile.<case_profile_attr> to target_cell
    if condition_cell's current value equals condition_value.

    Args:
        worksheet: The openpyxl worksheet to operate on.
        case_profile: A CaseProfile dataclass instance.
        case_profile_attr: Name of the CaseProfile attribute to write.
        target_cell: Cell address to write the value to (e.g. "B5").
        condition_cell: Cell address whose value is checked (e.g. "A5").
        condition_value: The value condition_cell must equal for the write to occur.
    """
    if worksheet[condition_cell].value == condition_value:
        value = getattr(case_profile, case_profile_attr, None)
        if value is None:
            logger.warning(
                f"write_if_cell_matches: '{case_profile_attr}' not found on case_profile — skipping {target_cell}"
            )
            return
        worksheet[target_cell].value = value
        logger.debug(
            f"write_if_cell_matches: wrote '{case_profile_attr}' to {target_cell} "
            f"(condition {condition_cell} == {condition_value!r})"
        )
