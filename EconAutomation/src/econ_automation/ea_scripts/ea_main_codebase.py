import logging
import sys
from pathlib import Path
from typing import Any

from econ_automation.ea_scripts.data_extraction_scripts.mastertemplate_extraction_codebase import MasterTemplateExtractor
from econ_automation.ea_scripts.data_extraction_scripts.working_calc_extraction_codebase import WorkingCalcExtractor
from econ_automation.ea_scripts.data_extraction_scripts.pv2_extraction_codebase import PV2Extractor
from econ_automation.ea_scripts.data_extraction_scripts.hhspv_extraction_codebase import HHSPVExtractor

from econ_automation.ea_scripts.output_gen_scripts.output_core_codebase import WordTemplateProcessor

# Setting application name and version
APP_NAME = "EconAuto"
APP_VERSION = "0.1.0"
APP_FULL_NAME = f"Econ Workflow Automation ({APP_NAME}-{APP_VERSION})"

# Resource path function
def resource_path(relative_path: str) -> Path:
    """Resolve path to a bundled resource; works in dev and PyInstaller exe."""
    if hasattr(sys, '_MEIPASS'):
        return Path(sys._MEIPASS) / relative_path
    return Path(__file__).parent / relative_path

# Dictionary of all relevant (hardcoded) filepaths
def create_main_filepaths_dict() -> dict[str, dict[str, Path]]:
    main_filepaths_dict = {
    "WORKBOOKS": {
        "MASTERTEMPLATE": resource_path("supporting_docs/sorted_econ_files/MASTERTEMPLATE (color coded).xlsx"),
        "WORKING_CALC": resource_path("supporting_docs/sorted_econ_files/Working_CALC_VER1.11 (color coded).xlsx"),
        "PV2": resource_path("supporting_docs/sorted_econ_files/PV2 (color coded).xlsx"),
        "HHSPV": resource_path("supporting_docs/sorted_econ_files/HHS_PV_New (color coded).xlsx")
    },
    "TEMPLATES": {
        "EARNINGS_AND_PV_MEDS": resource_path("supporting_docs/sorted_econ_files/Earnings and PV Meds Report Template (color coded).docx"),
        "LCP_MASTERTEMPLATE": resource_path("supporting_docs/sorted_econ_files/LCP MASTERTEMPLATE (color coded).docx")
    },
    "OUTPUTS": {
        "OUTPUT_1": Path("/Users/ericmacbook/Documents/GitHub/EconAutomation-REP/EconAutomation/ea_outputs/generated_reports"),
        "OUTPUT_2": Path("/Users/ericmacbook/Documents/GitHub/EconAutomation-REP/EconAutomation/ea_outputs/generated_reports_2")
    }
}
    return main_filepaths_dict

# Module's logger instance
logger = logging.getLogger(__name__)

class EconWorkflowAutomation:
    def __init__(self,
                 selected_workbooks_list: list[str]=["MASTERTEMPLATE", "WORKING_CALC", "PV2", "HHSPV"],
                 selected_templates_list: list[str]=["EARNINGS_AND_PV_MEDS", "LCP_MASTERTEMPLATE"], 
                 selected_outputs_list: list[str] = ["OUTPUT_1", "OUTPUT_2"]):
        # TEMP: Defining default save directories and selected templates in __init__
        # THIS IS IN A WONKY PLACE - NEED TO UNIFY WITH USER CHOICES, DELETE AFTER FRONTEND IS DONE
        self.workbook_filepaths_dict = create_main_filepaths_dict()["WORKBOOKS"]
        self.template_filepaths_dict = create_main_filepaths_dict()["TEMPLATES"]
        self.output_filepaths_dict = create_main_filepaths_dict()["OUTPUTS"]
        
        # CALLING METHODS
        self.initialize_extractors()
        
        self.selected_workbook_filepaths = self.select_workbook_filepaths(selected_workbooks_list, self.workbook_filepaths_dict)
        self.selected_template_filepaths = self.select_template_filepaths(selected_templates_list, self.template_filepaths_dict)
        self.selected_output_filepaths = self.select_output_filepaths(selected_outputs_list, self.output_filepaths_dict)
    
    def generate_reports (self,
                          main_reformatted_data_dict: dict[str, dict[str, Any]],
                          selected_template_filepaths: list[Path],
                          selected_output_filepaths: list[Path]
                          ):
        """
        Utilizes extracted/reformatted data to autofill and saved each selected report template.
        """
        try:
            word_template_processor = WordTemplateProcessor(
                main_reformatted_data_dict=main_reformatted_data_dict,
                selected_template_filepaths=selected_template_filepaths,
                selected_output_filepaths=selected_output_filepaths
            )
        except TypeError:
            logger.exception(f"EconWorkflowAutomation.generate_reports: Input data type error.")
            raise
    
    def select_workbook_filepaths(self, selected_workbooks_list: list[str], workbook_filepaths_dict: dict[str, Path]) -> list[Path]:
        """
        Obtains the workbook filepaths based on the selected workbooks.
        """
        # TEMP: THIS WHOLE FUNCTION IS A STAND-IN UNTIL THE FRONTEND IS DEVELOPED
        selected_workbook_filepaths = []

        for workbook_name in selected_workbooks_list:
            if workbook_name in workbook_filepaths_dict:
                selected_workbook_filepaths.append(workbook_filepaths_dict[workbook_name])
        
        return selected_workbook_filepaths
    
    def select_template_filepaths(self, selected_templates_list: list[str], template_filepaths_dict: dict[str, Path]) -> list[Path]:
        """
        Obtains the template filepaths based on the selected templates.
        """
        # TEMP: THIS WHOLE FUNCTION IS A STAND-IN UNTIL THE FRONTEND IS DEVELOPED
        selected_template_filepaths = []

        for template_name in selected_templates_list:
            if template_name in template_filepaths_dict:
                selected_template_filepaths.append(template_filepaths_dict[template_name])
        
        return selected_template_filepaths
    
    def select_output_filepaths(self, selected_outputs_list: list[str], output_filepaths_dict: dict[str, Path]) -> list[Path]:
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
        self.mastertemplate_extractor = MasterTemplateExtractor(mastertemplate_path=self.workbook_filepaths_dict["MASTERTEMPLATE"])
        self.working_calc_extractor = WorkingCalcExtractor(working_calc_path=self.workbook_filepaths_dict["WORKING_CALC"])
        self.pv2_extractor = PV2Extractor(pv2_path=self.workbook_filepaths_dict["PV2"])
        self.hhspv_extractor = HHSPVExtractor(hhspv_path=self.workbook_filepaths_dict["HHSPV"])

        self.main_extracted_data_dict = self.get_all_extracted_data()
        self.main_reformatted_data_dict = self.get_all_reformatted_data()

    def get_all_extracted_data(self) -> dict[str, dict[str, Any]]:
        """
        Returns all extracted data from all extractors.
        """
        return {
            "MASTERTEMPLATE": self.mastertemplate_extractor.extracted_data,
            "WORKING_CALC": self.working_calc_extractor.extracted_data,
            "PV2": self.pv2_extractor.extracted_data,
            "HHSPV": self.hhspv_extractor.extracted_data
        }

    def get_all_reformatted_data(self) -> dict[str, dict[str, Any]]:
        """
        Returns all reformatted data from all extractors.
        """
        return {
            "MASTERTEMPLATE": self.mastertemplate_extractor.reformatted_data_dict,
            "WORKING_CALC": self.working_calc_extractor.reformatted_data_dict,
            "PV2": self.pv2_extractor.reformatted_data_dict,
            "HHSPV": self.hhspv_extractor.reformatted_data_dict
        }
    
    
