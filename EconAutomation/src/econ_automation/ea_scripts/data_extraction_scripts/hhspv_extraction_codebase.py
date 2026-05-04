import logging
from pathlib import Path

from econ_automation.ea_scripts.data_extraction_scripts.extraction_core_codebase import (
    DataExtractorCore,
    DataFormatterCore,
    WorkbookInfoCore,
)

# Module's logger instance
logger = logging.getLogger(__name__)


class HHSPVInfo(WorkbookInfoCore):
    """
    Class to obtain variable_names and their cell locations from the HHS workbook.
    """

    def __init__(
        self,
        hhspv_filepath: Path,
        workbook_outputs_sheet_name: str,
    ):
        # INSTANTIATING SUPERCLASS WORKBOOK INFO ATTRIBUTES
        super().__init__(
            workbook_filepath=hhspv_filepath,
            workbook_outputs_sheet_name=workbook_outputs_sheet_name,
        )

        # WORKBOOK VARIABLES DICTIONARY
        self.workbook_variables_dict = self.define_workbook_variables_dict(
            workbook_name=self.workbook_name,
            active_workbook=self.active_workbook,
            workbook_outputs_sheet_name=self.workbook_outputs_sheet_name,
        )

        # REFORMATTING LISTS DICTIONARY
        self.reformatting_lists_dict = self.create_reformatting_lists_dict()

        # WORKBOOK CHARTS DICTIONARY
        self.workbook_charts_dict = self.define_workbook_charts(
            workbook_name=self.workbook_name,
            active_workbook=self.active_workbook,
            workbook_outputs_sheet_name=self.workbook_outputs_sheet_name,
        )

        # WORKBOOK TABLES DICTIONARY
        self.workbook_tables_dict = self.define_workbook_tables(
            workbook_name=self.workbook_name,
            active_workbook=self.active_workbook,
            workbook_outputs_sheet_name=self.workbook_outputs_sheet_name,
        )

    def define_short_form_dates(self) -> list[str]:
        """
        Defines the short form dates for the relevant workbook.
        """
        short_form_dates_list = [""]
        return short_form_dates_list

    def define_long_form_dates(self) -> list[str]:
        """
        Defines the long form dates for the relevant workbook.
        """
        long_form_dates_list = [""]
        return long_form_dates_list

    def define_currency_values(self) -> list[str]:
        """
        Defines the currency values for the relevant workbook.
        """
        currency_values_list = [""]
        return currency_values_list

    def define_percentages(self) -> list[str]:
        """
        Defines the percentage values for the relevant workbook.
        """
        percentages_list = [""]
        return percentages_list

    def define_reformatted_floats(self) -> list[str]:
        """
        Defines the to-be-rounded float values for the relevant workbook.
        """
        reformatted_floats_list = [""]
        return reformatted_floats_list

    def create_reformatting_lists_dict(self) -> dict[str, list[str]]:
        """
        Creates a dictionary of the reformatting lists for the relevant workbook.
        """
        reformatting_lists_dict = {
            "short_form_dates": self.define_short_form_dates(),
            "long_form_dates": self.define_long_form_dates(),
            "currency_values": self.define_currency_values(),
            "percentages": self.define_percentages(),
            "floats": self.define_reformatted_floats(),
        }
        return reformatting_lists_dict


class HHSPVExtractor(DataExtractorCore):
    def __init__(
        self,
        hhspv_filepath: Path,
        workbook_outputs_sheet_name: str,
        temp_dir_path: Path,
    ):
        # INSTANTIATING WORKBOOK-SPECIFIC ATTRIBUTES
        self.hhspv_info = HHSPVInfo(
            hhspv_filepath=hhspv_filepath,
            workbook_outputs_sheet_name=workbook_outputs_sheet_name,
        )

        # DEFINING INSTANCE ATTRIBUTES
        self.workbook_variables_dict = self.hhspv_info.workbook_variables_dict
        self.reformatting_lists_dict = self.hhspv_info.reformatting_lists_dict
        self.workbook_charts_dict = self.hhspv_info.workbook_charts_dict
        self.workbook_tables_dict = self.hhspv_info.workbook_tables_dict

        super().__init__(
            workbook_pathstr=str(hhspv_filepath),
            workbook_variables_dict=self.workbook_variables_dict,
            workbook_charts_dict=self.workbook_charts_dict,
            workbook_tables_dict=self.workbook_tables_dict,
            temp_dir_path=temp_dir_path,
        )

        DataFormatterCore(
            workbook_dataclass=self.workbook_dataclass,
            reformatting_lists_dict=self.reformatting_lists_dict,
        )
