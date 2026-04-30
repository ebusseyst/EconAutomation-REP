import datetime as dt
import logging
import locale
from decimal import Decimal
from pathlib import Path
from typing import Any
import openpyxl as opxl
from dataclasses import make_dataclass

# Module's logger instance
logger = logging.getLogger(__name__)


class WorkbookInfoCore:
    """
    Core class for workbook information.
    """

    def __init__(
        self,
        workbook_filepath: Path,
        workbook_outputs_sheet_name: str = "REPORT_OUTPUTS",
    ) -> None:

        # DEFINING CLASS ATTRIBUTES
        self.workbook_name = Path(workbook_filepath).name
        self.workbook_outputs_sheet_name = workbook_outputs_sheet_name
        self.active_workbook = opxl.load_workbook(workbook_filepath, data_only=True)

        # DEFINING WORKBOOK VARIABLES
        self.workbook_variables_dict = self.define_workbook_variables_dict()

    def define_workbook_variables_dict(self) -> dict[str, tuple[str, str]]:
        """
        Defines the target cells for the instanced workbook. Data is pulled from dedicated "REPORT_OUTPUTS" tab on each
        relevant worksheet and returned as a nested dictionary (e.g., {"variable_name": ("worksheet_name", "cell_address")}).
        """
        try:
            workbook_variables_dict = {}
            workbook_outputs_sheet = self.active_workbook[
                self.workbook_outputs_sheet_name
            ]
            for row in workbook_outputs_sheet.iter_rows(
                min_row=3, min_col=1, max_col=4, max_row=100, values_only=True
            ):
                variable_name = row[0]
                worksheet_name = row[1]
                cell_address = row[2]
                if (
                    (variable_name == "" or variable_name is None)
                    or (worksheet_name == "" or worksheet_name is None)
                    or (cell_address == "" or cell_address is None)
                ):
                    logger.debug(
                        "DataExtractorCore.define_workbook_variables_dict: Empty column(s) found in REPORT_OUTPUTS tab."
                    )
                    continue
                workbook_variables_dict[f"{variable_name}"] = (
                    f"{worksheet_name}",
                    f"{cell_address}",
                )
            logger.info(
                f"DataExtractorCore.define_workbook_variables_dict: {self.workbook_name} variables dict: {workbook_variables_dict}"
            )
            return workbook_variables_dict
        except KeyError:
            logger.exception(
                f"DataExtractorCore.define_workbook_variables_dict: KeyError defining workbook variables for {self.workbook_name}"
            )
            raise
        except IndexError:
            logger.exception(
                f"DataExtractorCore.define_workbook_variables_dict: IndexError defining workbook variables for {self.workbook_name}"
            )
            raise
        except TypeError:
            logger.exception(
                f"DataExtractorCore.define_workbook_variables_dict: TypeError defining workbook variables for {self.workbook_name}"
            )
            raise


class DataFormatterCore:
    """
    Formats relevant values extracted from the workbook.
    """

    def __init__(
        self,
        workbook_dataclass: Any,
        reformatting_lists_dict: dict[str, list[str]],
    ):
        # DEFINING CLASS ATTRIBUTES
        self.workbook_dataclass = workbook_dataclass
        self.reformatting_lists_dict = reformatting_lists_dict

        # CALLING MAIN REPROCESSING METHOD
        self.reprocess_all_relevant_data()

    # ── Private parsing helpers ──────────────────────────────────────────

    @staticmethod
    def _parse_date_value(date_value: str | dt.date) -> dt.date:
        """Converts a date value to a date object."""
        if isinstance(date_value, dt.date):
            return date_value
        else:
            formats = [
                "%Y-%m-%d",
                "%Y/%m/%d",
                "%m-%d-%Y",
                "%m/%d/%Y",
                "%m-%d-%y",
                "%m/%d/%y",
                "%B %#d, %Y",
                "%B %d, %Y",
                "%b %#d, %Y",
                "%b %d, %Y",
            ]
            for fmt in formats:
                try:
                    return dt.datetime.strptime(date_value, fmt).date()
                except ValueError:
                    continue
            raise ValueError(f"Unable to parse date value: {date_value}")

    @staticmethod
    def _parse_currency_value(currency_value: str | float) -> float:
        """
        Parses a currency value to ensure it is in the correct format.
        """
        if isinstance(currency_value, float):
            return currency_value
        else:
            return float(currency_value)

    @staticmethod
    def _parse_percentage_value(percentage_value: str | float) -> float:
        """
        Parses a percentage value to ensure it is in the correct format.
        """
        if isinstance(percentage_value, float):
            return percentage_value
        else:
            return float(percentage_value)

    @staticmethod
    def _parse_float_value(float_value: str | float) -> float:
        """
        Parses a float value to ensure it is in the correct format.
        """
        if isinstance(float_value, float):
            return float_value
        else:
            return float(float_value)

    # ── Main reformatting methods ───────────────────────────────────────

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
                if getattr(
                    self.workbook_dataclass, value_name, None
                ) == "" or not hasattr(self.workbook_dataclass, value_name):
                    continue
                setattr(
                    self.workbook_dataclass,
                    value_name,
                    format_currency(
                        self._parse_currency_value(
                            getattr(self.workbook_dataclass, value_name)
                        )
                    ),
                )
            logger.debug(
                f"DataExtractorCore.reprocess_currency_values: Reprocessed currency values: {self.workbook_dataclass}"
            )
        except Exception as e:
            logger.exception(
                f"DataExtractorCore.reprocess_currency_values: Error reprocessing currency values: {e}"
            )

    def reprocess_short_form_dates(self, short_form_dates_list: list[str]) -> None:
        """
        Reprocesses provided date values to ensure they are in short-form format.
        """
        try:
            for date_value_name in short_form_dates_list:
                if getattr(self.workbook_dataclass, date_value_name, None) is None:
                    continue
                setattr(
                    self.workbook_dataclass,
                    date_value_name,
                    self._parse_date_value(
                        getattr(self.workbook_dataclass, date_value_name)
                    ).strftime("%m/%d/%Y"),
                )
            logger.debug(
                f"DataExtractorCore.reprocess_short_form_dates: Reprocessed short form dates: {self.workbook_dataclass}"
            )
        except Exception as e:
            logger.exception(
                f"DataExtractorCore.reprocess_short_form_dates: Error reprocessing short form dates: {e}"
            )

    def reprocess_long_form_dates(self, long_form_dates_list: list[str]) -> None:
        """
        Reprocesses provided date values to ensure they are in long-form format.
        """
        try:
            for date_value_name in long_form_dates_list:
                if getattr(self.workbook_dataclass, date_value_name, None) is None:
                    continue
                setattr(
                    self.workbook_dataclass,
                    date_value_name,
                    self._parse_date_value(
                        getattr(self.workbook_dataclass, date_value_name)
                    ).strftime("%B %d, %Y"),
                )
            logger.debug(
                f"DataExtractorCore.reprocess_long_form_dates: Reprocessed long form dates: {self.workbook_dataclass}"
            )
        except Exception as e:
            logger.exception(
                f"DataExtractorCore.reprocess_long_form_dates: Error reprocessing long form dates: {e}"
            )

    def reprocess_percentages(self, percentages_list: list[str]) -> None:
        """
        Reprocesses provided percentage values to ensure they are in the correct format.
        """
        try:
            for percentage_variable in percentages_list:
                if (
                    getattr(self.workbook_dataclass, percentage_variable, None) == ""
                    or getattr(self.workbook_dataclass, percentage_variable, None)
                    is None
                ):
                    continue
                parsed = (
                    self._parse_percentage_value(
                        getattr(self.workbook_dataclass, percentage_variable)
                    )
                    * 100
                )
                setattr(
                    self.workbook_dataclass,
                    percentage_variable,
                    f"{parsed:.2f}%",
                )
            logger.debug(
                f"DataExtractorCore.reprocess_percentages - reprocessed percentages: {self.workbook_dataclass}"
            )
        except Exception as e:
            logger.exception(
                f"DataExtractorCore.reprocess_percentages - Error reprocessing percentages: {e}"
            )

    def reprocess_floats(self, floats_list: list[str]) -> None:
        """
        Reprocesses provided float values to ensure they are in the correct format.
        """
        try:
            for float_variable in floats_list:
                if (
                    getattr(self.workbook_dataclass, float_variable, None) == ""
                    or getattr(self.workbook_dataclass, float_variable, None) is None
                ):
                    continue
                quantized = Decimal(
                    self._parse_float_value(
                        getattr(self.workbook_dataclass, float_variable)
                    )
                ).quantize(Decimal("0.00"))
                setattr(
                    self.workbook_dataclass,
                    float_variable,
                    str(quantized),  # TEMP: Convert to string for consistency
                )
            logger.debug(
                f"DataExtractorCore.reprocess_floats: Reprocessed floats: {self.workbook_dataclass}"
            )
        except Exception as e:
            logger.exception(
                f"DataExtractorCore.reprocess_floats: Error reprocessing floats: {e}"
            )


class DataExtractorCore:
    """
    Core class for extracting data from an active Excel workbook.
    """

    def __init__(
        self,
        workbook_name: str,
        active_workbook: opxl.Workbook,
        workbook_variables_dict: dict[str, tuple[str, str]],
    ):
        self.workbook_name = workbook_name
        self.active_workbook = active_workbook
        self.workbook_variables_dict = workbook_variables_dict

        self.workbook_dataclass = self.build_workbook_dataclass(
            self.workbook_name, self.workbook_variables_dict
        )

        # CALLING EXTRACT DATA METHOD
        self.extract_data(
            self.active_workbook, self.workbook_variables_dict, self.workbook_dataclass
        )

    def extract_data(
        self,
        active_workbook: opxl.Workbook,
        workbook_variables_dict: dict[str, tuple[str, str]],
        workbook_dataclass: type[Any],
    ) -> None:
        """
        Extracts data from the specified worksheet based on its target cells subdictionaries.
        """
        dataclass_object = workbook_dataclass
        try:
            for variable_name, value_tuple in workbook_variables_dict.items():
                worksheet_name, cell_address = value_tuple
                setattr(
                    dataclass_object,
                    variable_name,
                    active_workbook[worksheet_name][cell_address].value,
                )
            logger.info(
                f"DataExtractorCore.extract_data: Extracted data variables: {workbook_variables_dict.keys()}"
            )
            logger.info(
                f"DataExtractorCore.extract_data: Created dataclass object: {dataclass_object}"
            )
        except Exception as e:
            logger.exception(
                f"DataExtractorCore.extract_data: Error extracting data: {e}"
            )
            raise

    def build_workbook_dataclass(
        self,
        workbook_name: str,
        workbook_variables_dict: dict[str, tuple[str, str]],
    ) -> type[Any]:
        """
        Returns the workbook's dataclass object.
        """
        return make_dataclass(
            f"{workbook_name}Data",
            [(key, Any) for key in workbook_variables_dict.keys()],
        )

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
