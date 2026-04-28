import logging
from pathlib import Path
import datetime
import locale
from decimal import Decimal
from typing import Any

import openpyxl as opxl

# Module's logger instance
logger = logging.getLogger(__name__)

class WorkbookInfoCore:
    """
    Core class for workbook information.
    """
    def __init__(self, workbook_filepath: Path, workbook_outputs_sheet_name: str="REPORT_OUTPUTS") -> None:
        # DEFINING CLASS ATTRIBUTES
        self.workbook = opxl.load_workbook(workbook_filepath)
        self.workbook_outputs_sheet_name = workbook_outputs_sheet_name
        
        # DEFINING WORKBOOK VARIABLES
        self.workbook_variables_dict = self.define_workbook_variables_dict()
    
    def define_workbook_variables_dict(self) -> dict[str, tuple[str, str]]:
        """
        Defines the target cells for the instanced workbook. Data is pulled from dedicated "REPORT_OUTPUTS" tab on each
        relevant worksheet and returned as a nested dictionary (e.g., {"variable_name": ("worksheet_name", "cell_address")}).
        """
        try:
            workbook_variables_dict = {}
            workbook_outputs_sheet = self.workbook[self.workbook_outputs_sheet_name]
            for row in workbook_outputs_sheet.iter_rows(min_row=3, min_col=1, max_col=4, max_row=100, values_only=True):
                variable_name = row[0]
                worksheet_name = row[1]
                cell_address = row[2]
                if variable_name == "" or worksheet_name == "" or cell_address == "":
                    logger.debug("DataExtractorCore.define_workbook_variables_dict: Empty column(s) found in REPORT_OUTPUTS tab.")
                    continue
                workbook_variables_dict[f"{variable_name}"] = (f"{worksheet_name}", f"{cell_address}")
            return workbook_variables_dict
        except KeyError:
            logger.exception("DataExtractorCore.define_workbook_variables_dict: KeyError defining workbook variables.")
            raise
        except IndexError:
            logger.exception("DataExtractorCore.define_workbook_variables_dict: IndexError defining workbook variables.")
            raise
        except TypeError:
            logger.exception("DataExtractorCore.define_workbook_variables_dict: TypeError defining workbook variables.")
            raise

class DataFormatterCore:
    """
    Formats relevant values extracted from the workbook.
    """
    def __init__(self, 
                extracted_data_dict: dict[str, Any],
                reformatting_lists_dict: dict[str, list[str]]
                ):
        # DEFINING CLASS ATTRIBUTES
        self.extracted_data_dict = extracted_data_dict
        self.reformatting_lists_dict = reformatting_lists_dict
        
        # CALLING MAIN REPROCESSING METHOD
        self.reprocess_all_relevant_data()
        
        self.reformatted_data_dict = self.extracted_data_dict
        
    def reprocess_all_relevant_data(self) -> None:
        """
        Reprocesses all relevant data in the instanced extracted data dictionary.
        """
        for list_name, list_of_variables in self.reformatting_lists_dict.items():
            if list_name == "short_form_dates":
                self.reprocess_short_form_dates(short_form_dates_list=list_of_variables)
            elif list_name == "long_form_dates":
                self.reprocess_long_form_dates(long_form_dates_list=list_of_variables)
            elif list_name == "currency_values":
                self.reprocess_currency_values(currency_values_list=list_of_variables)
            elif list_name == "percentages":
                self.reprocess_percentages(percentages_list=list_of_variables)
            elif list_name == "floats":
                self.reprocess_floats(floats_list=list_of_variables)

    def reprocess_currency_values(self, currency_values_list: list[str]) -> None:
        """
        Reprocesses currency values to ensure they are in the correct format.
        """
        # Set locale for currency formatting
        locale.setlocale(locale.LC_ALL, "en_US.UTF-8")

        def format_currency(money_value: float) -> str:
            """
            Formats a float value as currency.
            """
            return locale.format_string("$%.0f", money_value, grouping=True)
            
        try:
            for value_name in currency_values_list:
                if self.extracted_data_dict.get(value_name) == "" or value_name not in self.extracted_data_dict:
                    continue
                self.extracted_data_dict[value_name] = format_currency(self.extracted_data_dict[value_name])
            logger.info(f"DataExtractorCore.reprocess_currency_values: Reprocessed currency values: {self.extracted_data_dict}")
        except Exception as e:
            logger.exception(f"DataExtractorCore.reprocess_currency_values: Error reprocessing currency values: {e}")

    def reprocess_short_form_dates(self, short_form_dates_list: list[str]) -> None:
        """
        Reprocesses provided date values to ensure they are in short-form format.
        """
        try:
            for date_value_name in short_form_dates_list:
                if self.extracted_data_dict.get(date_value_name) is None:
                    continue
                self.extracted_data_dict[date_value_name] = self.extracted_data_dict[date_value_name].date()
                self.extracted_data_dict[date_value_name] = datetime.datetime.strftime(self.extracted_data_dict[date_value_name], "%m/%d/%Y")
                self.extracted_data_dict[date_value_name] = str(self.extracted_data_dict[date_value_name])
            logger.info(f"DataExtractorCore.reprocess_short_form_dates: Reprocessed short form dates: {self.extracted_data_dict}")
        except Exception as e:
            logger.exception(f"DataExtractorCore.reprocess_short_form_dates: Error reprocessing short form dates: {e}")
    
    def reprocess_long_form_dates(self, long_form_dates_list: list[str]) -> None:
        """
        Reprocesses provided date values to ensure they are in long-form format.
        """
        try:
            for date_value_name in long_form_dates_list:
                if self.extracted_data_dict.get(date_value_name) is None:
                    continue
                self.extracted_data_dict[date_value_name] = self.extracted_data_dict[date_value_name].date()
                self.extracted_data_dict[date_value_name] = datetime.datetime.strftime(self.extracted_data_dict[date_value_name], "%B %#d, %Y")
                self.extracted_data_dict[date_value_name] = str(self.extracted_data_dict[date_value_name])
            logger.info(f"DataExtractorCore.reprocess_long_form_dates: Reprocessed long form dates: {self.extracted_data_dict}")
        except Exception as e:
            logger.exception(f"DataExtractorCore.reprocess_long_form_dates: Error reprocessing long form dates: {e}")
        
    def reprocess_percentages(self, percentages_list: list[str]) -> None:
        """
        Reprocesses provided percentage values to ensure they are in the correct format.
        """
        try:
            for percentage_variable in percentages_list:
                if self.extracted_data_dict.get(percentage_variable) == "" or self.extracted_data_dict.get(percentage_variable) is None:
                    continue
                self.extracted_data_dict[percentage_variable] = self.extracted_data_dict[percentage_variable] * 100
                self.extracted_data_dict[percentage_variable] = f"{self.extracted_data_dict[percentage_variable]:.2f}%"
            logger.info(f"DataExtractorCore.reprocess_percentages - reprocessed percentages: {self.extracted_data_dict}")
        except Exception as e:
            logger.exception(f"DataExtractorCore.reprocess_percentages - Error reprocessing percentages: {e}")
        
    def reprocess_floats(self, floats_list: list[str]) -> None:
        """
        Reprocesses provided float values to ensure they are in the correct format.
        """
        try:
            for float_variable in floats_list:
                if self.extracted_data_dict.get(float_variable) == "" or self.extracted_data_dict.get(float_variable) is None:
                    continue
                self.extracted_data_dict[float_variable] = Decimal(self.extracted_data_dict[float_variable]).quantize(Decimal("0.00"))
                self.extracted_data_dict[float_variable] = str(self.extracted_data_dict[float_variable]) # TEMP: Convert to string for consistency
            logger.info(f"DataExtractorCore.reprocess_floats: Reprocessed floats: {self.extracted_data_dict}")
        except Exception as e:
            logger.exception(f"DataExtractorCore.reprocess_floats: Error reprocessing floats: {e}")

class DataExtractorCore:
    """
    Core class for extracting data from an active Excel workbook.
    """
    def __init__(self, workbook_filepath: Path):
        self.workbook_filepath = workbook_filepath
        self.workbook = opxl.load_workbook(workbook_filepath, data_only=True) # Returns only computed values of formulas
        self.workbook_info = WorkbookInfoCore(workbook_filepath, workbook_outputs_sheet_name="REPORT_OUTPUTS")
        self.extracted_data = self.extract_data(self.workbook_info.workbook_variables_dict)
    
    def extract_data(self, workbook_variables_dict: dict[str, tuple[str, str]]):
        """
        Extracts data from the specified worksheet based on its target cells subdictionaries.
        """
        extracted_dict = {}
        try:
            for variable_name, value_tuple in workbook_variables_dict.items():
                worksheet_name, cell_address = value_tuple
                active_worksheet = self.workbook[worksheet_name]
                extracted_dict[variable_name] = active_worksheet[cell_address].value
            logger.info(f"DataExtractorCore.extract_data: Extracted data from {self.workbook}")
            logger.info(f"DataExtractorCore.extract_data: Extracted data dict: {extracted_dict}")
            return extracted_dict
        except Exception as e:
            logger.exception(f"DataExtractorCore.extract_data: Error extracting data: {e}")
            raise
    
    # def extract_tables(self, workbook_tables_list: list[str]=None):
    #     """
    #     Extracts tables from the specified worksheets based on their target table subdictionaries.
    #     """
    #     extracted_tables_dict = {}
    #     try:
    #         for worksheet_name in workbook_tables_list:
    #             for table_name, table in self.active_workbook[worksheet_name].tables.items():
    #                 df = pd.read_excel(self.active_workbook_path, sheet_name=worksheet_name, header=0, usecols=table.ref)
    #                 extracted_tables_dict[worksheet_name][table_name] = df
    #         logger.info(f"DataExtractorCore: Extracted tables from {self.active_workbook_path}")
    #         logger.info(f"DataExtractorCore: Extracted tables dict: {extracted_tables_dict}")
    #         return extracted_tables_dict
    #     except Exception as e:
    #         logger.exception(f"DataExtractorCore.extract_tables: Error extracting tables: {e}")
    #         return None
    
    