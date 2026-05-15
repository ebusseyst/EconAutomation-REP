import logging
from pathlib import Path

from econ_automation.ea_scripts.data_extraction_scripts.extraction_core_codebase import (
    DataExtractorCore,
    DataFormatterCore,
    WorkbookInfoCore,
)

# Module's logger instance
logger = logging.getLogger(__name__)


class CaseVariablesInfo(WorkbookInfoCore):
    """
    Class to obtain variable_names and their cell locations from the Case Variables workbook.
    """

    def __init__(
        self,
        case_variables_filepath: Path,
        workbook_outputs_sheet_name: str,
    ):
        # INSTANTIATING SUPERCLASS WORKBOOK INFO ATTRIBUTES
        super().__init__(
            workbook_filepath=case_variables_filepath,
            workbook_outputs_sheet_name=workbook_outputs_sheet_name,
        )

        # DEFINING CLASS ATTRIBUTES
        self.reformatting_lists_dict = self.create_reformatting_lists_dict()

    def define_currency_values(self) -> list[str]:
        """
        Defines the currency values for the relevant workbook.
        """
        currency_values_list = []
        return currency_values_list

    def define_percentages(self) -> list[str]:
        """
        Defines the percentage values for the relevant workbook.
        """
        percentages_list = []
        return percentages_list

    def define_reformatted_floats(self) -> list[str]:
        """
        Defines the to-be-rounded float values for the relevant workbook.
        """
        reformatted_floats_list = []
        return reformatted_floats_list

    def create_reformatting_lists_dict(self) -> dict[str, list[str]]:
        """
        Creates a dictionary of the reformatting lists for the relevant workbook.
        """
        reformatting_lists_dict = {}
        return reformatting_lists_dict


class CaseVariablesExtractor(DataExtractorCore):
    def __init__(
        self,
        case_variables_filepath: Path,
        workbook_outputs_sheet_name: str,
        temp_dir_path: Path,
    ):
        # INSTANTIATING WORKBOOK-SPECIFIC ATTRIBUTES
        case_variables_info = CaseVariablesInfo(
            case_variables_filepath=case_variables_filepath,
            workbook_outputs_sheet_name=workbook_outputs_sheet_name,
        )

        # DEFINING CLASS ATTRIBUTES
        self.workbook_variables_dict = case_variables_info.workbook_variables_dict
        self.reformatting_lists_dict = case_variables_info.reformatting_lists_dict
        self.workbook_charts_dict = case_variables_info.workbook_charts_dict
        self.workbook_tables_dict = case_variables_info.workbook_tables_dict

        super().__init__(
            workbook_pathstr=str(case_variables_filepath),
            workbook_variables_dict=self.workbook_variables_dict,
            workbook_charts_dict=self.workbook_charts_dict,
            workbook_tables_dict=self.workbook_tables_dict,
            temp_dir_path=temp_dir_path,
        )

        DataFormatterCore(
            workbook_dataclass=self.workbook_dataclass,
            reformatting_lists_dict=self.reformatting_lists_dict,
        )
