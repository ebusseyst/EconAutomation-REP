import logging
from pathlib import Path

from econ_automation.ea_scripts.data_extraction_scripts.extraction_core_codebase import (
    DataExtractorCore,
    WorkbookInfoCore,
)

logger = logging.getLogger(__name__)


class CaseVariablesExtractor(DataExtractorCore):
    def __init__(
        self,
        case_variables_filepath: Path,
        workbook_outputs_sheet_name: str,
        temp_dir_path: Path,
    ):
        workbook_info = WorkbookInfoCore(
            workbook_filepath=case_variables_filepath,
            workbook_outputs_sheet_name=workbook_outputs_sheet_name,
        )
        super().__init__(
            workbook_pathstr=str(case_variables_filepath),
            workbook_variables_dict=workbook_info.workbook_variables_dict,
            workbook_charts_dict=workbook_info.workbook_charts_dict,
            workbook_tables_dict=workbook_info.workbook_tables_dict,
            temp_dir_path=temp_dir_path,
        )
