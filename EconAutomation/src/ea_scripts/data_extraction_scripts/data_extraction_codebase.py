import logging
from pathlib import Path

import openpyxl

# Module's logger instance
logger = logging.getLogger(__name__)

class DataExtractorCore:
    def __init__(self, active_workbook_path: str):
        self.active_workbook_path = Path(active_workbook_path)
        self.active_workbook = openpyxl.load_workbook(active_workbook_path, data_only=True) # Returns only computed values of formulas

    def extract_table_data(self, worksheet_targets_dict: dict[str, dict[str, str]]):
        """
        Extracts data from the specified worksheet based on its target cells subdictionaries.
        """
        extracted_dict = {}
        for worksheet_name, target_cells_dict in worksheet_targets_dict.items():
            active_worksheet = self.active_workbook[worksheet_name]
            for value_name, cell_address in target_cells_dict.items():
                extracted_dict[value_name] = active_worksheet[cell_address].value
        return extracted_dict