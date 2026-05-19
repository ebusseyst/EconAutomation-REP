from pathlib import Path
import openpyxl as opxl
from typing import Any


def load_working_calc_wb(
    case_profile: Any, private_claimant_dir: Path
) -> opxl.Workbook:
    """
    Loads the working calculator workbook for the case.
    """
    sel_working_calc_path = (
        private_claimant_dir
        / f"{case_profile.claimant_name_last}{case_profile.claimant_name_first_initial} - WorkingCalc_Current.xlsm"
    )
    return opxl.load_workbook(sel_working_calc_path)

def setup_working_calc_wb(case_profile: Any, claimant: Path) -> None:
    
