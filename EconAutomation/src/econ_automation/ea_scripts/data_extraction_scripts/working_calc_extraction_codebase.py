from dataclasses import dataclass
from pathlib import Path
import logging

from econ_automation.ea_scripts.file_system_scripts.file_system_codebase import (
    FileSystemCore as fsc,
)
from econ_automation.ea_scripts.data_extraction_scripts.extraction_core_codebase import (
    DataExtractorCore,
    DataFormatterCore,
    WorkbookInfoCore,
)

# Module's logger instance
logger = logging.getLogger(__name__)


@dataclass
class WorkingCalcData:
    """Represents the data from the WORKING_CALC workbook."""


class WorkingCalcInfo(WorkbookInfoCore):
    """
    Class to obtain variable_names and their cell locations from the working_calc workbook.
    """

    def __init__(self):
        # INSTANTIATING SUPERCLASS WORKBOOK INFO ATTRIBUTES
        self.working_calc_path = Path(fsc().workbook_filepaths["WORKING_CALC"])
        super().__init__(workbook_filepath=self.working_calc_path)

        # DEFINING CLASS ATTRIBUTES
        self.workbook_variables_dict = self.define_workbook_variables_dict()
        self.reformatting_lists_dict = self.create_reformatting_lists_dict()

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


class WorkingCalcExtractor(DataExtractorCore):
    def __init__(self):
        # INSTANTIATING WORKBOOK-SPECIFIC ATTRIBUTES
        self.working_calc_info = WorkingCalcInfo()

        # DEFINING CLASS ATTRIBUTES
        self.workbook_variables_dict = self.working_calc_info.workbook_variables_dict
        self.reformatting_lists_dict = self.working_calc_info.reformatting_lists_dict

        super().__init__(
            workbook_name="WORKING_CALC",
            active_workbook=self.working_calc_info.active_workbook,
            workbook_variables_dict=self.workbook_variables_dict,
            workbook_dataclass=WorkingCalcData(),
        )

        DataFormatterCore(
            workbook_dataclass=self.workbook_dataclass,
            reformatting_lists_dict=self.reformatting_lists_dict,
        )
