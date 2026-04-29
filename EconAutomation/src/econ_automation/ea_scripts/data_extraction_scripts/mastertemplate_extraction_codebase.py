from dataclasses import dataclass
import logging
from pathlib import Path

from econ_automation.ea_scripts.data_extraction_scripts.extraction_core_codebase import (
    DataExtractorCore,
    DataFormatterCore,
    WorkbookInfoCore,
)

from econ_automation.ea_scripts.file_system_scripts.file_system_codebase import (
    FileSystemCore as fsc,
)

# Module's logger instance
logger = logging.getLogger(__name__)


@dataclass
class MasterTemplateData:
    """Represents the data from the MASTERTEMPLATE workbook."""

    claimant_employer: str | None = None
    job_title_1: str | None = None
    job_title_2: str | None = None
    wage_hourly: str | None = None
    wage_weekly: str | None = None
    LCP_expert: str | None = None


class MasterTemplateInfo(WorkbookInfoCore):
    """
    Class to obtain variable_names and their cell locations from the MASTERTEMPLATE workbook.
    """

    def __init__(self):
        # INSTANTIATING SUPERCLASS WORKBOOK INFO ATTRIBUTES
        self.mastertemplate_path = Path(fsc().workbook_filepaths["MASTERTEMPLATE"])
        super().__init__(workbook_filepath=self.mastertemplate_path)

        # DEFINING CLASS ATTRIBUTES
        self.workbook_variables_dict = self.define_workbook_variables_dict()
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
    def __init__(self):
        # INSTANTIATING WORKBOOK-SPECIFIC ATTRIBUTES
        mastertemplate_info = MasterTemplateInfo()

        # DEFINING CLASS ATTRIBUTES
        self.workbook_variables_dict = mastertemplate_info.workbook_variables_dict
        self.reformatting_lists_dict = mastertemplate_info.reformatting_lists_dict

        super().__init__(
            workbook_name="MASTERTEMPLATE",
            active_workbook=mastertemplate_info.active_workbook,
            workbook_variables_dict=self.workbook_variables_dict,
            workbook_dataclass=MasterTemplateData(),
        )

        DataFormatterCore(
            workbook_dataclass=self.workbook_dataclass,
            reformatting_lists_dict=self.reformatting_lists_dict,
        )
