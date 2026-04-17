import logging
import platform
import datetime

import openpyxl

from ea_scripts.data_extraction_scripts.data_extraction_codebase import DataExtractorCore

# Module's logger instance
logger = logging.getLogger(__name__)

# TEMP hardcoded file paths
if platform.system() == "Darwin":
    MASTERTEMPLATE_PATH = r"/Users/ericmacbook/Documents/GitHub/EconAutomation-REP/EconAutomation/src/supporting_docs/original_econ_files/MASTERTEMPLATE.xlsx"
    
elif platform.system() == "Windows":
    MASTERTEMPLATE_PATH = r"C:/Users/EricBussey/GitHub/EconAutomation-REP/EconAutomation/src/supporting_docs/original_econ_files/MASTERTEMPLATE.xlsx"

class MasterTemplateInfo:
    """
    Organizational class to define information about the target cells for the MASTERTEMPLATE workbook.
    """
    @staticmethod
    def define_workbook_targets():
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
            "date_of_trial": "B15",
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
    
class MasterTemplateExtractor(DataExtractorCore):
    def __init__(self, active_workbook_path: str = MASTERTEMPLATE_PATH):
        super().__init__(active_workbook_path)
        
        # DEFINING CLASS ATTRIBUTES
        self.target_cells_dict = MasterTemplateInfo.define_workbook_targets()
        
        # CALLING METHODS
        self.extracted_data = self.extract_data(self.target_cells_dict)
        
    # def extract_pv_summary_no_rounding_table(self):
    #     """
    #     Extracts the PowerQuery table from the PV_Summary_No_Rounding worksheet.
    #     """