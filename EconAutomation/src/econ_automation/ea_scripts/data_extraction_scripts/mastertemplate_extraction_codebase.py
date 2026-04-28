import econ_automation
import logging
from pathlib import Path
from typing import Any

import openpyxl

from econ_automation.ea_scripts.data_extraction_scripts.extraction_core_codebase import DataExtractorCore, DataFormatterCore, WorkbookInfoCore
from econ_automation.ea_scripts.ea_main_codebase import create_main_filepaths_dict


# Module's logger instance
logger = logging.getLogger(__name__)

class MasterTemplateInfo(WorkbookInfoCore):
    """
    Class to obtain variable_names and their cell locations from the MASTERTEMPLATE workbook.
    """
    def __init__(self, mastertemplate_path: Path):
        # INSTANTIATING SUPERCLASS WORKBOOK INFO ATTRIBUTES
        super().__init__(workbook_filepath=mastertemplate_path)

        # DEFINING CLASS ATTRIBUTES
        self.workbook_variables_dict = self.define_workbook_variables_dict()
        self.reformatting_lists_dict = self.create_reformatting_lists_dict()
    
    def define_short_form_dates(self) -> list[str]:
        """
        Defines the short form dates for the relevant workbook.
        """
        short_form_dates_list = [
            "claimant_short_DOB",
            "report_date",
            "reference_date",
            "date_of_accident",
            "date_of_trial_short"
        ]
        return short_form_dates_list
    
    def define_long_form_dates(self) -> list[str]:
        """
        Defines the long form dates for the relevant workbook.
        """
        long_form_dates_list = [
            "claimant_long_DOB",
            "LCP_report_date",
            "date_of_trial_long"
        ]
        return long_form_dates_list
    
    def define_currency_values(self) -> list[str]:
        """
        Defines the currency values for the relevant workbook.
        """
        currency_values_list = [
            "LTB1_loss_to_trial_base_1",
            "ac1_after_credit_1",
            "primary_earnings_base_1",
            "primary_earnings_base_2",
            "alternative_earnings_base",
            "hourly_wage",
            "weekly_wage",
            "pv_employer_fringe_contrib",
            "loss_from_trial_wo_return_to_work",
            "loss_from_trial_after_credit_1",
            "pv_meds_low",
            "pv_meds_mid",
            "pv_meds_high",
            "estimate_lower_bound",
            "estimate_upper_bound",
            "estimate_midpoint"
        ]
        return currency_values_list
    
    def define_percentages(self) -> list[str]:
        """
        Defines the percentage values for the relevant workbook.
        """
        percentages_list = [
            "default_discount_rate",
            "real_discount_rate",
            "inflation_rate"
        ]
        return percentages_list
    
    def define_reformatted_floats(self) -> list[str]:
        """
        Defines the to-be-rounded float values for the relevant workbook.
        """
        reformatted_floats_list = [
            "age_at_reference",
            "life_expectancy",
            "duration_of_projection"
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
    
class MasterTemplateExtractor(DataExtractorCore):
    def __init__(self, mastertemplate_path: Path):
        super().__init__(mastertemplate_path)
        # INSTANTIATING WORKBOOK-SPECIFIC ATTRIBUTES
        self.mastertemplate_info = MasterTemplateInfo(mastertemplate_path)
        
        # DEFINING CLASS ATTRIBUTES
        self.workbook_variables_dict = self.mastertemplate_info.workbook_variables_dict
        self.reformatting_lists_dict = self.mastertemplate_info.reformatting_lists_dict

        # CALLING METHODS
        try:
            # EXTRACTING DATA FROM WORKBOOK
            self.extracted_data = self.extract_data(self.workbook_variables_dict)
            
            # CREATING CONSOLIDATED KEYS
            self.create_consolidated_keys()
        except TypeError:
            logger.exception(f"MasterTemplateExtractor.__init__: Input data type error.")
            raise
        
        if self.extracted_data:
            mastertemplate_formatter = DataFormatterCore(
                extracted_data_dict=self.extracted_data,
                reformatting_lists_dict=self.reformatting_lists_dict
            )
            self.reformatted_data_dict = mastertemplate_formatter.reformatted_data_dict
    
    def create_consolidated_keys(self) -> None:
        """
        Creates consolidated keys for the extracted data dictionary.
        """
        self.extracted_data["claimant_name_full"] = f"{self.extracted_data['claimant_name_first']} {self.extracted_data['claimant_name_last']}"
        self.extracted_data["claimant_salutation_with_name_last"] = f"{self.extracted_data['claimant_salutation']} {self.extracted_data['claimant_name_last']}"
        self.extracted_data["attorney_name_full"] = f"{self.extracted_data['attorney_name_first']} {self.extracted_data['attorney_name_last']}"
        self.extracted_data["attorney_salutation_with_name_full"] = f"{self.extracted_data['attorney_salutation']} {self.extracted_data['attorney_name_full']}"
        self.extracted_data["attorney_salutation_with_name_last"] = f"{self.extracted_data['attorney_salutation']} {self.extracted_data['attorney_name_last']}"
        self.extracted_data["firm_city_state_zip"] = f"{self.extracted_data['firm_city']}, {self.extracted_data['firm_state']} {self.extracted_data['firm_zip_code']}"
        self.extracted_data["firm_address_full"] = f"{self.extracted_data['firm_name']}\n{self.extracted_data['firm_street_address']}\n{self.extracted_data['firm_city_state_zip']}"
        
    # def extract_pv_summary_no_rounding_table(self):
    #     """
    #     Extracts the PowerQuery table from the PV_Summary_No_Rounding worksheet.
    #     """