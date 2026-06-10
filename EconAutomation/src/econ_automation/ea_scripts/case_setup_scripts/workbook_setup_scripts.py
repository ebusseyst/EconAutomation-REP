from pathlib import Path
from typing import Any
from datetime import datetime
import dateutil.parser as parser
import logging

import xlwings as xlw

logger = logging.getLogger(__name__)


def set_PV2_case_variables(case_profile: Any, pv2_workbook_path: Path) -> None:
    """
    Sets the case variables in the PV2 workbook.
    """
    with xlw.App(visible=False) as app:
        with app.books.open(pv2_workbook_path, update_links=False) as pv2_wb:
            sheet_names = [s.name for s in pv2_wb.sheets]
            if "Case Inputs" not in sheet_names:
                logger.warning(
                    "PV2 workbook %s is missing 'Case Inputs' sheet (found: %s)",
                    pv2_workbook_path.name,
                    sheet_names,
                )
                return
            case_inputs_sheet = pv2_wb.sheets["Case Inputs"]
            case_inputs_sheet.range("B3").value = case_profile.claimant_name_full
            case_inputs_sheet.range("B4").value = (
                case_profile.claimant_DOB_short
                if case_profile.claimant_DOB_short != ""
                else "Missing Claimant DOB"
            )
            case_inputs_sheet.range("B5").value = (
                case_profile.claimant_DOI_short
                if case_profile.claimant_DOI_short != ""
                else "Missing Claimant DOI"
            )
            case_inputs_sheet.range("B6").value = (
                case_profile.trial_date_short
                if case_profile.trial_date_short != ""
                else "Missing Trial Date"
            )
            claimant_gender = (
                case_profile.claimant_gender
                if case_profile.claimant_gender != ""
                else "Missing Claimant Gender"
            )
            if claimant_gender == "man":
                case_inputs_sheet.range("B9").value = "M"
            else:
                case_inputs_sheet.range("B9").value = "F"

            pv2_wb.save(pv2_workbook_path)


def set_WC_case_variables(case_profile: Any, wc_workbook_path: Path) -> None:
    """
    Sets the case variables in the Working Calc workbook.
    """
    with xlw.App(visible=False) as app:
        with app.books.open(wc_workbook_path, update_links=False) as wc_wb:
            sheet_names = [s.name for s in wc_wb.sheets]
            if "DROPS" not in sheet_names:
                logger.warning(
                    "WC workbook %s is missing 'DROPS' sheet (found: %s)",
                    wc_workbook_path.name,
                    sheet_names,
                )
                return
            drops_sheet = wc_wb.sheets["DROPS"]

            if case_profile.trial_date_short == "":
                if case_profile.reference_date_short == "":
                    trial_date = "Error: Missing Trial Date"
                else:
                    trial_date = case_profile.reference_date_short
            else:
                trial_date = case_profile.trial_date_short

            try:
                drops_sheet.range("B10").value = datetime.strptime(
                    trial_date, "%m/%d/%Y"
                ).year
                drops_sheet.range("B12").value = trial_date
                drops_sheet.range("B13").value = (
                    case_profile.claimant_DOB_short
                    if case_profile.claimant_DOB_short != ""
                    else "Missing Claimant DOB"
                )
            except (ValueError, TypeError, AttributeError, parser.ParserError):
                drops_sheet.range("B10").value = "Error: Invalid Trial Date"
                drops_sheet.range("B12").value = "Error: Invalid Trial Date"

            wc_wb.save(wc_workbook_path)
