import logging
import sys
from pathlib import Path
from typing import Any

import openpyxl

# Logger instance
logger = logging.getLogger(__name__)

class ExcelInserterCore:
    def __init__(self, source_data_dict: dict, selected_workbook_filepaths: dict[str, Path]):
        self.source_data_dict = source_data_dict
        self.selected_workbook_filepaths = selected_workbook_filepaths
    
    def insert_into_workbook(self) -> None:
        try:
            
        
        