from pathlib import Path
from typing import Any
import logging

import openpyxl as opxl
from openpyxl.cell.cell import MergedCell

logger = logging.getLogger(__name__)


def create_case_variables_excel_sheet(
    case_profile: Any,
    case_var_wb_path: Path,
    private_claimant_dir: Path,
) -> None:
    """
    Creates a new Excel workbook with the same structure as the template workbook.
    Populates the one worksheet with data from the case_profile dataclass.
    """

    # 1. Load the template workbook
    workbook = opxl.load_workbook(str(case_var_wb_path))

    # 2. Get the one worksheet
    sheet = workbook["REPORT_OUTPUTS"]

    # 3. Populate the worksheet with data from the case_profile dataclass
    label_to_row = {
        cell.value: cell.row for cell in sheet["A"] if cell.value is not None
    }
    for field in case_profile.__dataclass_fields__.values():
        row = label_to_row.get(field.name)
        if row is not None:
            cell = sheet.cell(row=row, column=2)
            if isinstance(cell, MergedCell):
                for merge_range in sheet.merged_cells.ranges:
                    if (
                        merge_range.min_row <= row <= merge_range.max_row
                        and merge_range.min_col <= 2 <= merge_range.max_col
                    ):
                        top_left = sheet.cell(
                            row=merge_range.min_row, column=merge_range.min_col
                        )
                        if not isinstance(top_left, MergedCell):
                            top_left.value = getattr(case_profile, field.name)
                        break
            else:
                cell.value = getattr(case_profile, field.name)

    # 4. Save the workbook to the claimant's private directory
    case_var_new_name = f"{case_profile.claimant_name_last}{case_profile.claimant_name_first_initial} - Case Variables.xlsx"
    output_filepath = private_claimant_dir / case_var_new_name

    if output_filepath.exists():
        logger.warning("Skipping Case Variables: %s already exists.", output_filepath)
        return

    workbook.save(str(output_filepath))
