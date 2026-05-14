from pathlib import Path
from typing import Any

import openpyxl as opxl


def create_case_variables_excel_sheet(
    case_profile: Any,
    template_workbook: Path,
    output_filepath: Path,
) -> None:
    """
    Creates a new Excel workbook with the same structure as the template workbook.
    Populates the one worksheet with data from the case_profile dataclass.
    """

    # 1. Load the template workbook
    workbook = opxl.load_workbook(template_workbook)

    # 2. Get the one worksheet
    sheet = workbook["REPORT_OUTPUTS"]

    # 3. Populate the worksheet with data from the case_profile dataclass
    for field in case_profile.__dataclass_fields__.values():
        sheet[field.name] = getattr(case_profile, field.name)

    workbook.save(output_filepath)
