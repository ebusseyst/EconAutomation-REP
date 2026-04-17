import logging
from pathlib import Path

from ea_scripts.data_extraction_scripts.mastertemplate_extraction_codebase import MasterTemplateExtractor
from ea_scripts.output_gen_scripts.output_core_codebase import WordTemplateProcessor

# Setting application name and version
APP_NAME = "EconAuto"
APP_VERSION = "0.1.0"
APP_FULL_NAME = f"Econ Workflow Automation ({APP_NAME}-{APP_VERSION})"

# Module's logger instance
logger = logging.getLogger(__name__)

class EconWorkflowAutomation:
    def __init__(self, mastertemplate_filepath: Path=None, output_template_filepath: Path=None, output_save_path: Path=None):
        # DEFINING FILE PATHS (TO BE CHANGED LATER)
        self.mastertemplate_filepath = mastertemplate_filepath
        self.output_template_filepath = output_template_filepath
        self.output_save_path = output_save_path
    
    def run_workflow(self):
        # INSTANTIATING (AND AUTOMATICALLY EXECUTING) SUB-CLASSES
        self.masterdata_extractor = MasterTemplateExtractor(active_workbook_path=self.mastertemplate_filepath)
        self.word_template_processor = WordTemplateProcessor(extracted_data_dict=self.masterdata_extractor.extracted_data, template_filepath=self.output_template_filepath, output_save_path=self.output_save_path)