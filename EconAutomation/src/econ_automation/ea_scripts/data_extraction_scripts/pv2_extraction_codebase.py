import logging
from pathlib import Path

from econ_automation.ea_scripts.data_extraction_scripts.extraction_core_codebase import (
    DataExtractorCore,
    DataFormatterCore,
    WorkbookInfoCore,
)


# Module's logger instance
logger = logging.getLogger(__name__)


class PV2Info(WorkbookInfoCore):
    """
    Class to obtain variable_names and their cell locations from the PV2 workbook.
    """

    def __init__(
        self,
        pv2_filepath: Path,
        workbook_outputs_sheet_name: str,
    ):
        # INSTANTIATING SUPERCLASS WORKBOOK INFO ATTRIBUTES
        super().__init__(
            workbook_filepath=pv2_filepath,
            workbook_outputs_sheet_name=workbook_outputs_sheet_name,
        )

        # DEFINING CLASS ATTRIBUTES
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
        currency_values_list = [
            "b1e_WLE_earnings",
            "b1e_WLE_pretrial_loss_notax",
            "b1e_WLE_pretrial_loss_adj",
            "b1e_WLE_posttrial_loss_notax",
            "b1e_WLE_posttrial_loss_adj",
            "b1e_toage_earnings",
            "b1e_toage_growth_rate",
            "b1e_toage_pretrial_loss_notax",
            "b1e_toage_pretrial_loss_adj",
            "b1e_toage_posttrial_loss_notax",
            "b1e_toage_posttrial_loss_adj",
            "b1e_WLE_total_loss_notax",
            "b1e_WLE_total_loss_adj",
            "b1e_toage_total_loss_notax",
            "b1e_toage_total_loss_adj",
            "b2e_WLE_earnings",
            "b2e_WLE_growth_rate",
            "b2e_WLE_pretrial_loss_notax",
            "b2e_WLE_pretrial_loss_adj",
            "b2e_WLE_posttrial_loss_notax",
            "b2e_WLE_posttrial_loss_adj",
            "b2e_toage_earnings",
            "b2e_toage_growth_rate",
            "b2e_toage_pretrial_loss_notax",
            "b2e_toage_pretrial_loss_adj",
            "b2e_toage_posttrial_loss_notax",
            "b2e_toage_posttrial_loss_adj",
            "b2e_WLE_total_loss_notax",
            "b2e_WLE_total_loss_adj",
            "b2e_toage_total_loss_notax",
            "b2e_toage_total_loss_adj",
            "b3e_WLE_earnings",
            "b3e_WLE_growth_rate",
            "b3e_WLE_pretrial_loss_notax",
            "b3e_WLE_pretrial_loss_adj",
            "b3e_WLE_posttrial_loss_notax",
            "b3e_WLE_posttrial_loss_adj",
            "b3e_toage_earnings",
            "b3e_toage_growth_rate",
            "b3e_toage_pretrial_loss_notax",
            "b3e_toage_pretrial_loss_adj",
            "b3e_toage_posttrial_loss_notax",
            "b3e_toage_posttrial_loss_adj",
            "b3e_WLE_total_loss_notax",
            "b3e_WLE_total_loss_adj",
            "b3e_toage_total_loss_notax",
            "b3e_toage_total_loss_adj",
            "b4e_WLE_pretrial_loss_notax",
            "b4e_WLE_pretrial_loss_adj",
            "b4e_WLE_posttrial_loss_notax",
            "b4e_WLE_posttrial_loss_adj",
            "b4e_toage_earnings",
            "b4e_toage_growth_rate",
            "b4e_toage_pretrial_loss_notax",
            "b4e_toage_pretrial_loss_adj",
            "b4e_toage_posttrial_loss_notax",
            "b4e_toage_posttrial_loss_adj",
            "b4e_WLE_total_loss_notax",
            "b4e_WLE_total_loss_adj",
            "b4e_toage_total_loss_notax",
            "b4e_toage_total_loss_adj",
            "b5e_WLE_earnings",
            "b5e_WLE_growth_rate",
            "b5e_WLE_pretrial_loss_notax",
            "b5e_WLE_pretrial_loss_adj",
            "b5e_WLE_posttrial_loss_notax",
            "b5e_WLE_posttrial_loss_adj",
            "b5e_toage_earnings",
            "b5e_toage_growth_rate",
            "b5e_toage_pretrial_loss_notax",
            "b5e_toage_pretrial_loss_adj",
            "b5e_toage_posttrial_loss_notax",
            "b5e_toage_posttrial_loss_adj",
            "b5e_WLE_total_loss_notax",
            "b5e_WLE_total_loss_adj",
            "b5e_toage_total_loss_notax",
            "b5e_toage_total_loss_adj",
        ]
        return currency_values_list

    def define_percentages(self) -> list[str]:
        """
        Defines the percentage values for the relevant workbook.
        """
        percentages_list = [
            "b1e_WLE_growth_rate",
            "b2e_WLE_growth_rate",
            "b3e_WLE_growth_rate",
            "b4e_WLE_growth_rate",
            "b5e_WLE_growth_rate",
            "b1e_toage_growth_rate",
            "b2e_toage_growth_rate",
            "b3e_toage_growth_rate",
            "b4e_toage_growth_rate",
            "b5e_toage_growth_rate",
        ]
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


class PV2Extractor(DataExtractorCore):
    def __init__(
        self,
        pv2_filepath: Path,
        workbook_outputs_sheet_name: str,
        temp_dir_path: Path,
    ):
        # INSTANTIATING WORKBOOK-SPECIFIC ATTRIBUTES
        pv2_info = PV2Info(
            pv2_filepath=pv2_filepath,
            workbook_outputs_sheet_name=workbook_outputs_sheet_name,
        )

        # DEFINING CLASS ATTRIBUTES
        self.workbook_variables_dict = pv2_info.workbook_variables_dict
        self.reformatting_lists_dict = pv2_info.reformatting_lists_dict
        self.workbook_charts_dict = pv2_info.workbook_charts_dict
        self.workbook_tables_dict = pv2_info.workbook_tables_dict

        super().__init__(
            workbook_pathstr=str(pv2_filepath),
            workbook_variables_dict=self.workbook_variables_dict,
            workbook_charts_dict=self.workbook_charts_dict,
            workbook_tables_dict=self.workbook_tables_dict,
            temp_dir_path=temp_dir_path,
        )

        DataFormatterCore(
            workbook_dataclass=self.workbook_dataclass,
            reformatting_lists_dict=self.reformatting_lists_dict,
        )
