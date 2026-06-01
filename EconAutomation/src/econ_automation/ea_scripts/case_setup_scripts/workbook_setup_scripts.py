from pathlib import Path
from typing import Any
from datetime import datetime

import xlwings as xlw


def set_PV2_case_variables(case_profile: Any, pv2_workbook_path: Path) -> None:
    """
    Sets the case variables in the PV2 workbook.
    """
    with xlw.App(visible=False) as app:
        with app.books.open(pv2_workbook_path) as pv2_wb:
            # Sets "Case Inputs" sheet values
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
                case_inputs_sheet.range("B8").value = "M"
            else:
                case_inputs_sheet.range("B8").value = "F"

            pv2_wb.save(pv2_workbook_path)


def set_WC_case_variables(case_profile: Any, wc_workbook_path: Path) -> None:
    """
    Sets the case variables in the Working Calc workbook.
    """
    with xlw.App(visible=False) as app:
        with app.books.open(wc_workbook_path) as wc_wb:
            # Sets "DROPS" sheet values
            drops_sheet = wc_wb.sheets["DROPS"]

            trial_date = (
                case_profile.trial_date_short
                if case_profile.trial_date_short != ""
                else "Missing Trial Date"
            )

            drops_sheet.range("B10").value = datetime.strptime(
                trial_date, "%m/%d/%Y"
            ).year
            drops_sheet.range("B12").value = trial_date
            drops_sheet.range("B13").value = (
                case_profile.claimant_DOB_short
                if case_profile.claimant_DOB_short != ""
                else "Missing Claimant DOB"
            )

            wc_wb.save(wc_workbook_path)
