from dataclasses import make_dataclass, fields, is_dataclass
import logging
from pathlib import Path
from typing import Any
from importlib.metadata import version, metadata

from pydantic import BaseModel

from econ_automation.ea_scripts.file_system_scripts.file_system_codebase import (
    FileSystemCore as fsc,
)
from econ_automation.ea_scripts.data_extraction_scripts.case_variables_extraction_codebase import (
    CaseVariablesExtractor,
)
from econ_automation.ea_scripts.data_extraction_scripts.working_calc_extraction_codebase import (
    WorkingCalcExtractor,
)
from econ_automation.ea_scripts.data_extraction_scripts.pv2_extraction_codebase import (
    PV2Extractor,
)
from econ_automation.ea_scripts.data_extraction_scripts.hhspv_extraction_codebase import (
    HHSPVExtractor,
)
from econ_automation.ea_scripts.case_setup_scripts.OFF_extraction_codebase import (
    OFFExtractor,
)

from econ_automation.ea_scripts.report_merge_scripts.report_merge_codebase import (
    AutofillWordTemplates,
)

# Setting application name and version
APP_NAME = metadata("econ_automation").get("Name")
APP_VERSION = version("econ_automation")
APP_FULL_NAME = f"{APP_NAME} v{APP_VERSION}"

# Module's logger instance
logger = logging.getLogger(__name__)


class EconReportGenerator:
    def __init__(
        self,
        selected_files_dict: dict[str, list[str]] = {
            "OFF_filepaths": ["OFF_FILE_A"],
            "workbook_filepaths": [
                "CASE_VARIABLES",
                "WORKING_CALC",
                "PV2",
                "HHSPV",
            ],
            "template_filepaths": ["PVLCP_TEMPLATE"],
            "output_filepaths": ["OUTPUT_1", "OUTPUT_2"],
        },
    ):
        # INSTANTIATING FILE SYSTEM CORE
        self.file_system_core = fsc()

        # DEFINING CLASS ATTRIBUTES FROM FILE SYSTEM CORE
        self.temp_dir = self.file_system_core.temp_dir
        self.temp_dir_filepath = self.file_system_core.temp_dir_filepath

        # LOADING ea_config.yaml FILEPATHS INTO MAIN FILEPATHS DICTIONARY
        self.main_filepaths_dict = self.file_system_core.main_filepaths_dict

        # GETTING SELECTED FILEPATHS
        self.selected_filepaths_dict = self._select_relevant_filepaths(
            selected_files_dict, self.main_filepaths_dict
        )

        # INITIALIZING EXTRACTORS
        self.initialize_extractors(
            selected_OFF_filepaths=list(
                self.selected_filepaths_dict["OFF_filepaths"].values()
            )
        )

        # EXTRACTING FORMATTED WORKBOOK DATACLASSES FROM SELECTED WORKBOOKS
        econ_data_list = self.get_all_reformatted_data()

        # FLATTENING EXTRACTED DATA INTO A SINGLE MAIN DATACLASS
        self.ea_main_dataclass = self.flatten_all_extracted_data(econ_data_list)

        # GENERATING REPORTS
        self.generate_reports(
            ea_main_dataclass=self.ea_main_dataclass,
            selected_template_filepaths=list(
                self.selected_filepaths_dict["template_filepaths"].values()
            ),
            selected_output_filepaths=list(
                self.selected_filepaths_dict["output_filepaths"].values()
            ),
        )

    def generate_reports(
        self,
        ea_main_dataclass: Any,
        selected_template_filepaths: list[Path],
        selected_output_filepaths: list[Path],
    ):
        """
        Utilizes extracted/reformatted data to autofill and saved each selected report template.
        """
        try:
            AutofillWordTemplates(
                ea_main_dataclass=ea_main_dataclass,
                selected_template_filepaths=selected_template_filepaths,
                selected_output_filepaths=selected_output_filepaths,
            )
        except TypeError:
            logger.exception(
                "EconWorkflowAutomation.generate_reports: Input data type error."
            )
            raise

    def _select_relevant_filepaths(
        self,
        selected_files_dict: dict[str, list[str]],
        main_filepaths_dict: dict[str, dict[str, Path]],
    ) -> dict[str, dict[str, Path]]:
        """
        Selects relevant filepaths from a main_filepaths_dict based on the selected items,
        returns dict[str, dict[str, Path]].

        Args:
            selected_files_dict (dict[str, list[str]]): Dictionary of user-selected file names.
            main_filepaths_dict (dict[str, dict[str, Path]]): Dictionary of filepaths.

        Returns:
            dict[str, dict[str, Path]]: Dictionary of selected filepaths, keyed by category.
        """
        selected_filepaths_dict = {}

        for category, filenames_list in selected_files_dict.items():
            temp_sel_fps_dict = {}
            for filename in filenames_list:
                if filename in main_filepaths_dict[category].keys():
                    temp_sel_fps_dict[filename] = main_filepaths_dict[category][
                        filename
                    ]
            selected_filepaths_dict[category] = temp_sel_fps_dict

        return selected_filepaths_dict

    def initialize_extractors(self, selected_OFF_filepaths: list[Path]) -> None:
        """
        Initializes all data extractors.

        Args:
            selected_OFF_filepaths (list[Path]): List of selected OFF filepaths.
        """
        # TEMP: THIS WHOLE FUNCTION IS A STAND-IN UNTIL THE FRONTEND (AND MULTI-OFF EXTRACTION SUPPORT) IS DEVELOPED
        self.off_extractor = OFFExtractor(selected_OFF_filepaths[0])

        workbook_outputs_sheet_name = "REPORT_OUTPUTS"

        self.case_variables_extractor = CaseVariablesExtractor(
            case_variables_filepath=self.selected_filepaths_dict["workbook_filepaths"][
                "CASE_VARIABLES"
            ],
            workbook_outputs_sheet_name=workbook_outputs_sheet_name,
            temp_dir_path=self.temp_dir_filepath,
        )
        self.working_calc_extractor = WorkingCalcExtractor(
            working_calc_filepath=self.selected_filepaths_dict["workbook_filepaths"][
                "WORKING_CALC"
            ],
            workbook_outputs_sheet_name=workbook_outputs_sheet_name,
            temp_dir_path=self.temp_dir_filepath,
        )
        self.pv2_extractor = PV2Extractor(
            pv2_filepath=self.selected_filepaths_dict["workbook_filepaths"]["PV2"],
            workbook_outputs_sheet_name=workbook_outputs_sheet_name,
            temp_dir_path=self.temp_dir_filepath,
        )
        self.hhspv_extractor = HHSPVExtractor(
            hhspv_filepath=self.selected_filepaths_dict["workbook_filepaths"]["HHSPV"],
            workbook_outputs_sheet_name=workbook_outputs_sheet_name,
            temp_dir_path=self.temp_dir_filepath,
        )

    def get_all_reformatted_data(self) -> list[Any]:
        """
        Returns all reformatted data from all extractors as a list of dataclasses.
        """
        return [
            self.off_extractor.case_profile,
            self.case_variables_extractor.workbook_dataclass,
            self.working_calc_extractor.workbook_dataclass,
            self.pv2_extractor.workbook_dataclass,
            self.hhspv_extractor.workbook_dataclass,
        ]

    def flatten_all_extracted_data(self, econ_data_list: list[Any]) -> Any:
        """
        Returns a flattened dataclass of all extracted data.

        Args:
            econ_data_list (list[Any]): List of dataclasses to flatten.

        Returns:
            Any: Flattened dataclass of all extracted data.
        """
        all_fields = []
        all_values = {}
        for dc in econ_data_list:
            if isinstance(dc, BaseModel):
                for name in type(dc).model_fields.keys():
                    all_fields.append((name, Any))
                    all_values[name] = getattr(dc, name)
            elif is_dataclass(dc):
                for f in fields(dc):
                    all_fields.append((f.name, Any))
                    all_values[f.name] = getattr(dc, f.name)
            else:
                raise TypeError(f"Unsupported type in econ_data_list: {type(dc)}")

        EconAutomationData = make_dataclass("EconAutomationData", all_fields)
        return EconAutomationData(**all_values)
