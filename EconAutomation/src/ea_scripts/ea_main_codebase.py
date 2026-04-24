import logging
from pathlib import Path

from ea_scripts.data_extraction_scripts.mastertemplate_extraction_codebase import MasterTemplateExtractor
# from ea_scripts.data_extraction_scripts.working_calc_extraction_codebase import WorkingCalcExtractor
# from ea_scripts.data_extraction_scripts.pv2_extraction_codebase import PV2Extractor
from ea_scripts.data_extraction_scripts.hhs_pv_extraction_codebase import HHS_PVExtractor

from ea_scripts.output_gen_scripts.output_core_codebase import WordTemplateProcessor

# Setting application name and version
APP_NAME = "EconAuto"
APP_VERSION = "0.1.0"
APP_FULL_NAME = f"Econ Workflow Automation ({APP_NAME}-{APP_VERSION})"

# Module's logger instance
logger = logging.getLogger(__name__)

class EconWorkflowAutomation:
    def __init__(self, input_workbooks_dict: dict[str, Path], template_filepaths_dict: dict[str, Path], output_save_paths_list: list[Path]):
        # DEFINING CLASS ATTRIBUTES
        self.input_workbooks_dict = input_workbooks_dict
        self.template_filepaths_dict = template_filepaths_dict
        self.output_save_paths_list = output_save_paths_list
        
        # CALLING METHODS
        self.run_workflow()
    
    def run_workflow(self):
        """
        Runs the main workflow of the application.
        """
        # CALLING SUB-CLASS METHODS
        self.masterdata_extractor = MasterTemplateExtractor(mastertemplate_path=self.input_workbooks_dict["mastertemplate_filepath"])
        self.word_template_processor = WordTemplateProcessor(
            extracted_data_dict_1=self.masterdata_extractor.extracted_data,
            template_filepaths_dict=self.template_filepaths_dict,
            output_save_paths_list=self.output_save_paths_list
        )