import logging
from pathlib import Path
from typing import Any
from importlib.metadata import version, metadata

from econ_automation.ea_scripts.file_system_scripts.file_system_codebase import (
    FileSystemCore as fsc,
)

from econ_automation.ea_scripts.data_extraction_scripts.mastertemplate_extraction_codebase import (
    MasterTemplateExtractor,
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
from econ_automation.ea_scripts.data_extraction_scripts.OFF_extraction_codebase import (
    OFFExtractor,
)

from econ_automation.ea_scripts.output_gen_scripts.output_core_codebase import (
    AutofillWordTemplates,
)

# Setting application name and version
APP_NAME = metadata("econ_automation").get("Name")
APP_VERSION = version("econ_automation")
APP_FULL_NAME = f"{APP_NAME} v{APP_VERSION}"

# Module's logger instance
logger = logging.getLogger(__name__)


class EconWorkflowAutomation:
    def __init__(
        self,
        selected_OFFs_list: list[str] = [
            "OFF_FILE_A",
        ],
        selected_workbooks_list: list[str] = [
            "MASTERTEMPLATE",
            "WORKING_CALC",
            "PV2",
            "HHSPV",
            "OFF",
        ],
        selected_templates_list: list[str] = [
            "PV_EARNINGS_MEDS_TEMPLATE",
            "PVLCP_MASTERTEMPLATE",
        ],
        selected_outputs_list: list[str] = ["OUTPUT_1", "OUTPUT_2"],
    ):
        # THIS IS IN A WONKY PLACE - NEED TO UNIFY WITH USER CHOICES, DELETE AFTER FRONTEND IS DONE
        # Load ea_config.yaml and populate class attributes with filepaths
        self.OFF_filepaths_dict = fsc().OFF_filepaths
        self.workbook_filepaths_dict = fsc().workbook_filepaths
        self.template_filepaths_dict = fsc().template_filepaths
        self.output_filepaths_dict = fsc().output_filepaths

        # CALLING METHODS
        self.selected_OFF_filepaths = self.select_OFF_filepaths(
            selected_OFFs_list, self.OFF_filepaths_dict
        )
        self.selected_workbook_filepaths = self.select_workbook_filepaths(
            selected_workbooks_list, self.workbook_filepaths_dict
        )
        self.selected_template_filepaths = self.select_template_filepaths(
            selected_templates_list, self.template_filepaths_dict
        )
        self.selected_output_filepaths = self.select_output_filepaths(
            selected_outputs_list, self.output_filepaths_dict
        )

        self.initialize_extractors()

        # CALLING GENERATE REPORTS
        self.generate_reports(
            main_reformatted_data_dict=self.main_reformatted_data_dict,
            selected_template_filepaths=self.selected_template_filepaths,
            selected_output_filepaths=self.selected_output_filepaths,
        )

    def generate_reports(
        self,
        main_reformatted_data_dict: dict[str, Any],
        selected_template_filepaths: list[Path],
        selected_output_filepaths: list[Path],
    ):
        """
        Utilizes extracted/reformatted data to autofill and saved each selected report template.
        """
        try:
            AutofillWordTemplates(
                main_reformatted_data_dict=main_reformatted_data_dict,
                selected_template_filepaths=selected_template_filepaths,
                selected_output_filepaths=selected_output_filepaths,
            )
        except TypeError:
            logger.exception(
                "EconWorkflowAutomation.generate_reports: Input data type error."
            )
            raise

    def select_OFF_filepaths(
        self, selected_OFFs_list: list[str], OFF_filepaths_dict: dict[str, Path]
    ) -> list[Path]:
        """
        Obtains the OFF filepaths based on the selected OFFs.
        """
        # TEMP: THIS WHOLE FUNCTION IS A STAND-IN UNTIL THE FRONTEND IS DEVELOPED
        selected_OFF_filepaths = []

        for OFF_name in selected_OFFs_list:
            if OFF_name in OFF_filepaths_dict:
                selected_OFF_filepaths.append(OFF_filepaths_dict[OFF_name])

        return selected_OFF_filepaths

    def select_workbook_filepaths(
        self,
        selected_workbooks_list: list[str],
        workbook_filepaths_dict: dict[str, Path],
    ) -> list[Path]:
        """
        Obtains the workbook filepaths based on the selected workbooks.
        """
        # TEMP: THIS WHOLE FUNCTION IS A STAND-IN UNTIL THE FRONTEND IS DEVELOPED
        selected_workbook_filepaths = []

        for workbook_name in selected_workbooks_list:
            if workbook_name in workbook_filepaths_dict:
                selected_workbook_filepaths.append(
                    workbook_filepaths_dict[workbook_name]
                )

        return selected_workbook_filepaths

    def select_template_filepaths(
        self,
        selected_templates_list: list[str],
        template_filepaths_dict: dict[str, Path],
    ) -> list[Path]:
        """
        Obtains the template filepaths based on the selected templates.
        """
        # TEMP: THIS WHOLE FUNCTION IS A STAND-IN UNTIL THE FRONTEND IS DEVELOPED
        selected_template_filepaths = []

        for template_name in selected_templates_list:
            if template_name in template_filepaths_dict:
                selected_template_filepaths.append(
                    template_filepaths_dict[template_name]
                )

        return selected_template_filepaths

    def select_output_filepaths(
        self, selected_outputs_list: list[str], output_filepaths_dict: dict[str, Path]
    ) -> list[Path]:
        """
        Obtains the output filepaths based on the selected outputs.
        """
        # TEMP: THIS WHOLE FUNCTION IS A STAND-IN UNTIL THE FRONTEND IS DEVELOPED
        selected_output_filepaths = []

        for output_name in selected_outputs_list:
            if output_name in output_filepaths_dict:
                selected_output_filepaths.append(output_filepaths_dict[output_name])

        return selected_output_filepaths

    def initialize_extractors(self) -> None:
        """
        Initializes all data extractors.
        """
        # TEMP: THIS WHOLE FUNCTION IS A STAND-IN UNTIL THE FRONTEND (AND MULTI-OFF EXTRACTION SUPPORT) IS DEVELOPED
        self.off_extractor = OFFExtractor(self.selected_OFF_filepaths[0])

        self.mastertemplate_extractor = MasterTemplateExtractor()
        self.working_calc_extractor = WorkingCalcExtractor()
        self.pv2_extractor = PV2Extractor()
        self.hhspv_extractor = HHSPVExtractor()

        self.main_reformatted_data_dict = self.get_all_reformatted_data()

    def get_all_reformatted_data(self) -> dict[str, Any]:
        """
        Returns all reformatted data from all extractors.
        """
        return {
            "OFF": self.off_extractor.case_profile,
            "MASTERTEMPLATE": self.mastertemplate_extractor.workbook_dataclass,
            "WORKING_CALC": self.working_calc_extractor.workbook_dataclass,
            "PV2": self.pv2_extractor.workbook_dataclass,
            "HHSPV": self.hhspv_extractor.workbook_dataclass,
        }
