import logging
from pathlib import Path
import datetime
import locale
from decimal import Decimal

import openpyxl
import pandas as pd

# Module's logger instance
logger = logging.getLogger(__name__)

class DataExtractorCore:
    def __init__(self, active_workbook_path: str):
        self.active_workbook_path = Path(active_workbook_path)
        self.active_workbook = openpyxl.load_workbook(active_workbook_path, data_only=True) # Returns only computed values of formulas
        
    def extract_data(self, workbook_targets_dict: dict[str, dict[str, str]]):
        """
        Extracts data from the specified worksheet based on its target cells subdictionaries.
        """
        extracted_dict = {}
        try:
            for worksheet_name, target_cells_dict in workbook_targets_dict.items():
                active_worksheet = self.active_workbook[worksheet_name]
                worksheet_targets_dict = workbook_targets_dict[worksheet_name]
                for value_name, cell_address in worksheet_targets_dict.items():
                    extracted_dict[value_name] = active_worksheet[cell_address].value
            logger.info(f"DataExtractorCore: Extracted data from {self.active_workbook_path}")
            logger.info(f"DataExtractorCore: Extracted data dict: {extracted_dict}")
            return extracted_dict
        except Exception as e:
            logger.exception(f"DataExtractorCore.extract_data: Error extracting data: {e}")
            return None
    
    def extract_tables(self, workbook_tables_list: list[str]=None):
        """
        Extracts tables from the specified worksheets based on their target table subdictionaries.
        """
        extracted_tables_dict = {}
        try:
            for worksheet_name in workbook_tables_list:
                for table_name, table in self.active_workbook[worksheet_name].tables.items():
                    df = pd.read_excel(self.active_workbook_path, sheet_name=worksheet_name, header=0, usecols=table.ref)
                    extracted_tables_dict[worksheet_name][table_name] = df
            logger.info(f"DataExtractorCore: Extracted tables from {self.active_workbook_path}")
            logger.info(f"DataExtractorCore: Extracted tables dict: {extracted_tables_dict}")
            return extracted_tables_dict
        except Exception as e:
            logger.exception(f"DataExtractorCore.extract_tables: Error extracting tables: {e}")
            return None
    
    def reprocess_currency_values(self, currency_values_list: list[str]=None, extracted_data_dict: dict[str, any]=None):
        """
        Reprocesses currency values to ensure they are in the correct format.
        """
        # Set locale for currency formatting
        locale.setlocale(locale.LC_ALL, "en_US.UTF-8")

        def format_currency(money_value: float) -> str:
            """
            Formats a float value as currency.
            """
            return locale.currency(money_value, symbol=True, grouping=True)
        
        if extracted_data_dict is None:
            return
        if currency_values_list is None:
            return
        else:
            try:
                for value_name in currency_values_list:
                    if extracted_data_dict[value_name] is None:
                        continue
                    extracted_data_dict[value_name] = format_currency(extracted_data_dict[value_name])
                logger.info(f"DataExtractorCore.reprocess_currency_values: Reprocessed currency values: {extracted_data_dict}")
                return extracted_data_dict
            except Exception as e:
                logger.exception(f"DataExtractorCore.reprocess_currency_values: Error reprocessing currency values: {e}")
                return
            
    def reprocess_dates(self, short_form_dates_list: list[str]=None, long_form_dates_list: list[str]=None, extracted_data_dict: dict[str, any]=None):
        """
        Reprocesses provided date values to ensure they are in the correct format.
        """
        if extracted_data_dict is None:
            return
        
        if short_form_dates_list is not None:
            try:
                for date_value_name in short_form_dates_list:
                    if extracted_data_dict[date_value_name] is None:
                        continue
                    extracted_data_dict[date_value_name] = extracted_data_dict[date_value_name].date()
                    extracted_data_dict[date_value_name] = datetime.datetime.strftime(extracted_data_dict[date_value_name], "%m/%d/%Y")
                    extracted_data_dict[date_value_name] = str(extracted_data_dict[date_value_name])
                logger.info(f"DataExtractorCore.reprocess_dates: Reprocessed short form dates: {extracted_data_dict}")
            except Exception as e:
                logger.exception(f"DataExtractorCore.reprocess_dates: Error reprocessing short form dates: {e}")
        
        if long_form_dates_list is not None:
            try:
                for date_value_name in long_form_dates_list:
                    if extracted_data_dict[date_value_name] is None:
                        continue
                    extracted_data_dict[date_value_name] = extracted_data_dict[date_value_name].date()
                    extracted_data_dict[date_value_name] = datetime.datetime.strftime(extracted_data_dict[date_value_name], "%B %#d, %Y")
                    extracted_data_dict[date_value_name] = str(extracted_data_dict[date_value_name])
                logger.info(f"DataExtractorCore.reprocess_dates: Reprocessed long form dates: {extracted_data_dict}")
            except Exception as e:
                logger.exception(f"DataExtractorCore.reprocess_dates: Error reprocessing long form dates: {e}")
        
        return extracted_data_dict
    
    def reprocess_percentages(self, percentages_list: list[str]=None, extracted_data_dict: dict[str, any]=None):
        """
        Reprocesses provided percentage values to ensure they are in the correct format.
        """
        if extracted_data_dict is None:
            return
        
        if percentages_list is not None:
            try:
                for percentage_value_name in percentages_list:
                    if extracted_data_dict[percentage_value_name] is None:
                        continue
                    extracted_data_dict[percentage_value_name] = extracted_data_dict[percentage_value_name] * 100
                    extracted_data_dict[percentage_value_name] = str(f"{extracted_data_dict[percentage_value_name]:.2f}%")
                logger.info(f"DataExtractorCore.reprocess_percentages: Reprocessed percentages: {extracted_data_dict}")
            except Exception as e:
                logger.exception(f"DataExtractorCore.reprocess_percentages: Error reprocessing percentages: {e}")
        
        return extracted_data_dict
    
    def reprocess_floats(self, floats_list: list[str]=None, extracted_data_dict: dict[str, any]=None):
        """
        Reprocesses provided float values to ensure they are in the correct format.
        """
        if extracted_data_dict is None:
            return
        
        if floats_list is not None:
            try:
                for float_value_name in floats_list:
                    if extracted_data_dict[float_value_name] is None:
                        continue
                    extracted_data_dict[float_value_name] = Decimal(extracted_data_dict[float_value_name]).quantize(Decimal("0.00"))
                    extracted_data_dict[float_value_name] = str(extracted_data_dict[float_value_name]) # TEMP: Convert to string for consistency
                logger.info(f"DataExtractorCore.reprocess_floats: Reprocessed floats: {extracted_data_dict}")
            except Exception as e:
                logger.exception(f"DataExtractorCore.reprocess_floats: Error reprocessing floats: {e}")
        
        return extracted_data_dict  