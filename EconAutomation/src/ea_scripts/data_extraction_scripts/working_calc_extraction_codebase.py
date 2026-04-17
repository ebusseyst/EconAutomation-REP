import logging

import openpyxl
import pandas as pd
import pydantic

from ea_scripts.data_extraction_scripts.extraction_core_codebase import DataExtractorCore

# Module's logger instance
logger = logging.getLogger(__name__)

class WorkingCalcInfo:
    """
    Class to hold information about the working calc workbook.
    """
    @staticmethod
    def define_working_calc_targets():
        """
        Defines the target cells for the working calc workbook. Dictionaries are currently hardcoded and
        are individually defined for readability.
        """
        # Currently hardcoded dictionaries of value_name: cell_address for each worksheet in the working_calc workbook
        
        # Item Inputs Worksheet is the only worksheet that contains cell values that need to be extracted (currently)
        item_inputs_dict = {
            "InitialCostLow": "G55", 
            "InitialCostHigh": "H55", 
            "Low Cost per Use": "I55", 
            "High Cost per Use": "J55"
            }

        # Higher scope nested dictionary to hold all target cell dictionaries (one per worksheet)
        working_calc_targets_dict = {
            "Item Inputs": item_inputs_dict
        }

        return working_calc_targets_dict

class WorkingCalcExtractor(DataExtractorCore):
    def __init__(self, active_workbook_path: str = r"C:/Users/EricBussey/GitHub/EconAutomation-REP/EconAutomation/src/supporting_docs/original_econ_files/Working_CALC_VER1.11.xlsx"):
        super().__init__(active_workbook_path)
        
        # DEFINING CLASS ATTRIBUTES
        self.target_cells_dict = WorkingCalcInfo.define_working_calc_targets()
        
        # CALLING METHODS
        self.extracted_data = self.extract_data(self.target_cells_dict)
        
    # def extract_pv_summary_no_rounding_table(self):
    #     """
    #     Extracts the PowerQuery table from the PV_Summary_No_Rounding worksheet.
    #     """
        