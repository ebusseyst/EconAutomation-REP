import logging
from pathlib import Path
from typing import Any

import openpyxl

from ea_scripts.data_extraction_scripts.extraction_core_codebase import DataExtractorCore, DataFormatterCore

# Module's logger instance
logger = logging.getLogger(__name__)

class MasterTemplateInfo:
    """
    Organizational class to define information about the target cells for the MASTERTEMPLATE workbook.
    """
    def __init__(self):
        self.workbook_variables_dict = self.define_workbook_variables_dict()
        self.reformatting_lists_dict = self.create_reformatting_lists_dict()

    def define_workbook_variables_dict(self) -> dict[str, dict[str, Any]]:
        """
        Defines the target cells for the relevant workbook. Dictionaries are currently hardcoded and
        are individually defined for readability.
        """
        # Currently hardcoded dictionaries of value_name: cell_address for each worksheet in the MASTERTEMPLATE workbook
        
        # "Inputs" worksheet is the only worksheet that contains cell values that need to be extracted (currently)
        mastertemplate_inputs_dict = {
            "claimant_salutation": "B4",
            "claimant_name_first": "B5",
            "claimant_name_last": "B6",
            "claimant_pronoun": "B7",
            "claimant_gender": "B8",
            "claimant_ethnicity": "B9",
            "claimant_long_DOB": "B10",
            "claimant_short_DOB": "B11",
            "report_date": "B12",
            "reference_date": "B13",
            "date_of_accident": "B14",
            "date_of_trial_short": "B15",
            "date_of_trial_long" : "B15",
            "LTB1_loss_to_trial_base_1": "B16",
            "ac1_after_credit_1": "B17",
            "place_of_trial": "B18",
            "claimant_employer": "B19",
            "job_title_1": "B20",
            "job_title_2": "B21",
            "age_at_reference": "B22",
            "life_expectancy": "B23",
            "primary_earnings_base_1": "B24",
            "primary_earnings_base_2": "B25",
            "alternative_earnings_base": "B26",
            "hourly_wage": "B27",
            "weekly_wage": "B28",
            "pv_employer_fringe_contrib": "B29",
            "loss_from_trial_wo_return_to_work": "B30",
            "loss_from_trial_after_credit_1": "B31",
            "pv_meds_low": "B32",
            "pv_meds_mid": "B33",
            "pv_meds_high": "B34",

            "attorney_salutation": "B38",
            "attorney_name_first": "B39",
            "attorney_name_last": "B40",
            "firm_name": "B41",
            "firm_street_address": "B42",
            "firm_city": "B43",
            "firm_state": "B44",
            "firm_zip_code": "B45",
            "firm_phone": "B46",
            "firm_email": "B47",
            "firm_fax": "B48",

            "LCP_preparer": "B51",
            "LCP_report_date": "B52",
            "estimate_lower_bound": "B53",
            "estimate_upper_bound": "B54",
            "estimate_midpoint": "B55",

            "duration_of_projection": "B57",
            "default_discount_rate": "B59",
            "real_discount_rate": "B60",
            "inflation_rate": "B61",
            "consistent_with": "B62"
            }
        
        # Higher scope nested dictionary to hold all target cell dictionaries (one per worksheet)
        mastertemplate_targets_dict = {
            "Inputs": mastertemplate_inputs_dict
        }

        return mastertemplate_targets_dict
    
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
            "reformatted_floats": self.define_reformatted_floats()
        }
        return reformatting_lists_dict
    
class MasterTemplateExtractor(DataExtractorCore):
    def __init__(self, mastertemplate_path: Path, data_formatter: DataFormatterCore):
        super().__init__(mastertemplate_path, data_formatter)
        
        # INSTANTIATING WORKBOOK-SPECIFIC ATTRIBUTES
        self.mastertemplate_info = MasterTemplateInfo()
        
        # DEFINING CLASS ATTRIBUTES
        self.target_cells_dict = self.mastertemplate_info.define_workbook_variables_dict()
        self.short_form_dates_list = self.mastertemplate_info.define_short_form_dates()
        self.long_form_dates_list = self.mastertemplate_info.define_long_form_dates()
        self.currency_values_list = self.mastertemplate_info.define_currency_values()
        self.percentages_list = self.mastertemplate_info.define_percentages()
        self.reformatted_floats_list = self.mastertemplate_info.define_reformatted_floats()
        
        self.reformatting_lists_dict = self.mastertemplate_info.create_reformatting_lists_dict()
        
        self.data_formatter = data_formatter

        # CALLING METHODS
        try:
            # EXTRACTING DATA FROM WORKBOOK
            self.extracted_data = self.extract_data(self.target_cells_dict)
            
            # REPROCESSING INDIVIDUAL FIELDS
            self.extracted_data = self.data_formatter.reprocess_dates(short_form_dates_list=self.short_form_dates_list, long_form_dates_list=self.long_form_dates_list, extracted_data_dict=self.extracted_data)
            self.extracted_data = self.data_formatter.reprocess_currency_values(currency_values_list=self.currency_values_list, extracted_data_dict=self.extracted_data)
            self.extracted_data = self.data_formatter.reprocess_percentages(percentages_list=self.percentages_list, extracted_data_dict=self.extracted_data)
            self.extracted_data = self.data_formatter.reprocess_floats(floats_list=self.reformatted_floats_list, extracted_data_dict=self.extracted_data)
            
            # CREATING CONSOLIDATED KEYS
            self.extracted_data["claimant_name_full"] = f"{self.extracted_data['claimant_name_first']} {self.extracted_data['claimant_name_last']}"
            self.extracted_data["claimant_salutation_with_name_last"] = f"{self.extracted_data['claimant_salutation']} {self.extracted_data['claimant_name_last']}"
            self.extracted_data["attorney_name_full"] = f"{self.extracted_data['attorney_name_first']} {self.extracted_data['attorney_name_last']}"
            self.extracted_data["attorney_salutation_with_name_full"] = f"{self.extracted_data['attorney_salutation']} {self.extracted_data['attorney_name_full']}"
            self.extracted_data["attorney_salutation_with_name_last"] = f"{self.extracted_data['attorney_salutation']} {self.extracted_data['attorney_name_last']}"
            self.extracted_data["firm_city_state_zip"] = f"{self.extracted_data['firm_city']}, {self.extracted_data['firm_state']} {self.extracted_data['firm_zip_code']}"
            self.extracted_data["firm_address_full"] = f"{self.extracted_data['firm_name']}\n{self.extracted_data['firm_street_address']}\n{self.extracted_data['firm_city_state_zip']}"
        except Exception as e:
            logger.exception(f"MasterTemplateExtractor.__init__: Error extracting data from workbook.")
            raise ValueError("Error extracting data from workbook.")  
        
    # def extract_pv_summary_no_rounding_table(self):
    #     """
    #     Extracts the PowerQuery table from the PV_Summary_No_Rounding worksheet.
    #     """