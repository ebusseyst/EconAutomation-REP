import logging
from pathlib import Path

from econ_automation.ea_scripts.data_extraction_scripts.extraction_core_codebase import (
    DataExtractorCore,
    DataFormatterCore,
    WorkbookInfoCore,
)

# Module's logger instance
logger = logging.getLogger(__name__)


class MasterTemplateInfo(WorkbookInfoCore):
    """
    Class to obtain variable_names and their cell locations from the MASTERTEMPLATE workbook.
    """

    def __init__(
        self,
        mastertemplate_filepath: Path,
        workbook_outputs_sheet_name: str,
    ):
        # INSTANTIATING SUPERCLASS WORKBOOK INFO ATTRIBUTES
        super().__init__(
            workbook_filepath=mastertemplate_filepath,
            workbook_outputs_sheet_name=workbook_outputs_sheet_name,
        )

        # DEFINING CLASS ATTRIBUTES
        self.reformatting_lists_dict = self.create_reformatting_lists_dict()

    def define_currency_values(self) -> list[str]:
        """
        Defines the currency values for the relevant workbook.
        """
        currency_values_list = [
            "wage_hourly",
            "wage_weekly",
        ]
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
        reformatting_lists_dict = {
            "currency_values": self.define_currency_values(),
            "percentages": self.define_percentages(),
            "floats": self.define_reformatted_floats(),
        }
        return reformatting_lists_dict


class MasterTemplateExtractor(DataExtractorCore):
    def __init__(
        self,
        mastertemplate_filepath: Path,
        workbook_outputs_sheet_name: str,
        temp_dir_path: Path,
    ):
        # INSTANTIATING WORKBOOK-SPECIFIC ATTRIBUTES
        mastertemplate_info = MasterTemplateInfo(
            mastertemplate_filepath=mastertemplate_filepath,
            workbook_outputs_sheet_name=workbook_outputs_sheet_name,
        )

        # DEFINING CLASS ATTRIBUTES
        self.workbook_variables_dict = mastertemplate_info.workbook_variables_dict
        self.reformatting_lists_dict = mastertemplate_info.reformatting_lists_dict
        self.workbook_charts_dict = mastertemplate_info.workbook_charts_dict
        self.workbook_tables_dict = mastertemplate_info.workbook_tables_dict

        super().__init__(
            workbook_pathstr=str(mastertemplate_filepath),
            workbook_variables_dict=self.workbook_variables_dict,
            workbook_charts_dict=self.workbook_charts_dict,
            workbook_tables_dict=self.workbook_tables_dict,
            temp_dir_path=temp_dir_path,
        )

        DataFormatterCore(
            workbook_dataclass=self.workbook_dataclass,
            reformatting_lists_dict=self.reformatting_lists_dict,
        )
