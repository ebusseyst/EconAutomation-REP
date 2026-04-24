import logging

from ea_scripts.data_extraction_scripts.extraction_core_codebase import DataExtractorCore, DataFormatterCore

# Module's logger instance
logger = logging.getLogger(__name__)

class HHSPVTemplateInfo:
    """
    Organizational class to define information about the target cells for the relevant workbook.
    """
    @staticmethod
    def define_workbook_targets():
        """
        Defines the target cells for the relevant workbook. Dictionaries are currently hardcoded and
        are individually defined for readability.
        """
        # Currently hardcoded dictionaries of value_name: cell_address for each worksheet in the HHSPV workbook
        
        hhs_pv_audit_detail_dict = {
            "": "",
            }
        
        hhs_pv_household_services_pv_dict = {
            "": "",
        }

        hhs_pv_case_info_dict = {
            "": "",
        }

        hhs_pv_drops_dict = {
            "": "",
        }

        hhs_pv_category_selection_dict = {
            "": "",
        }
        
        # Higher scope nested dictionary to hold all target cell dictionaries (one per worksheet)
        hhs_pv_targets_dict = {
            "AuditDetail": hhs_pv_audit_detail_dict,
            "HouseholdServices_PV": hhs_pv_household_services_pv_dict,
            "Case Info": hhs_pv_case_info_dict,
            "DROPS": hhs_pv_drops_dict,
            "CategorySelection": hhs_pv_category_selection_dict
        }

        return hhs_pv_targets_dict
    
    @staticmethod
    def define_short_form_dates():
        """
        Defines the short form dates list from the workbook's relevant variable names.
        """
        short_form_dates_list = [
            "claimant_short_DOB",
        ]
        return short_form_dates_list
    
    @staticmethod
    def define_long_form_dates():
        """
        Defines the long form dates from the workbook's relevant variable names.
        """
        long_form_dates_list = [
            "claimant_long_DOB",
            "LCP_report_date",
            "date_of_trial_long"
        ]
        return long_form_dates_list
    
    @staticmethod
    def define_currency_values():
        """
        Defines the currency values from the workbook's relevant variable names.
        """
        currency_values_list = [
            "",
        ]
        return currency_values_list
    
    @staticmethod
    def define_percentages():
        """
        Defines the percentage values from the workbook's relevant variable names.
        """
        percentages_list = [
            "",
        ]
        return percentages_list
    
    @staticmethod
    def define_reformatted_floats():
        """
        Defines the to-be-rounded float values from the workbook's relevant variable names.
        """
        reformatted_floats_list = [
            "",
        ]
        return reformatted_floats_list