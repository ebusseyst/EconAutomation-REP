import logging
from pathlib import Path

from econ_automation.ea_scripts.data_extraction_scripts.extraction_core_codebase import DataExtractorCore, DataFormatterCore, WorkbookInfoCore
from econ_automation.ea_scripts.ea_main_codebase import create_main_filepaths_dict


# Module's logger instance
logger = logging.getLogger(__name__)

class PV2Info(WorkbookInfoCore):
    """
    Class to obtain variable_names and their cell locations from the PV2 workbook.
    """
    def __init__(self):
        # INSTANTIATING SUPERCLASS WORKBOOK INFO ATTRIBUTES
        self.workbook_filepath = create_main_filepaths_dict()["WORKBOOKS"]["PV2"]
        super().__init__(workbook_filepath=self.workbook_filepath)

        # DEFINING CLASS ATTRIBUTES
        self.workbook_variables_dict = self.define_workbook_variables_dict()
        self.reformatting_lists_dict = self.create_reformatting_lists_dict()
    
    def define_short_form_dates(self) -> list[str]:
        """
        Defines the short form dates for the relevant workbook.
        """
        short_form_dates_list = [
            ""
        ]
        return short_form_dates_list
    
    def define_long_form_dates(self) -> list[str]:
        """
        Defines the long form dates for the relevant workbook.
        """
        long_form_dates_list = [
            ""
        ]
        return long_form_dates_list
    
    def define_currency_values(self) -> list[str]:
        """
        Defines the currency values for the relevant workbook.
        """
        currency_values_list = [
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
            "b5e_toage_growth_rate"
        ]
        return percentages_list
    
    def define_reformatted_floats(self) -> list[str]:
        """
        Defines the to-be-rounded float values for the relevant workbook.
        """
        reformatted_floats_list = [
            ""
        ]
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
            "floats": self.define_reformatted_floats()
        }
        return reformatting_lists_dict

class PV2Extractor(DataExtractorCore):
    def __init__(self, pv2_path: Path):
        super().__init__(pv2_path)
        # INSTANTIATING WORKBOOK-SPECIFIC ATTRIBUTES
        self.pv2_info = PV2Info()
        
        # DEFINING CLASS ATTRIBUTES
        self.workbook_variables_dict = self.pv2_info.workbook_variables_dict
        self.reformatting_lists_dict = self.pv2_info.reformatting_lists_dict

        # CALLING METHODS
        try:
            # EXTRACTING DATA FROM WORKBOOK
            self.extracted_data = self.extract_data(self.workbook_variables_dict)
            
        except TypeError:
            logger.exception(f"PV2Extractor.__init__: Input data type error.")
            raise
        
        if self.extracted_data:
            pv2_formatter = DataFormatterCore(
                extracted_data_dict=self.extracted_data,
                reformatting_lists_dict=self.reformatting_lists_dict
            )
            self.reformatted_data_dict = pv2_formatter.reformatted_data_dict