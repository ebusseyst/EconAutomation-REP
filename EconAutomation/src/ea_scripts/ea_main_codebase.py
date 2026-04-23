import logging
import sys
from pathlib import Path

from ea_scripts.data_extraction_scripts.mastertemplate_extraction_codebase import MasterTemplateExtractor
from ea_scripts.output_gen_scripts.output_core_codebase import WordTemplateProcessor

# Setting application name and version
APP_NAME = "EconAuto"
APP_VERSION = "0.1.0"
APP_FULL_NAME = f"Econ Workflow Automation ({APP_NAME}-{APP_VERSION})"

# Module's logger instance
logger = logging.getLogger(__name__)

# Resource path function
def resource_path(relative_path: str) -> Path:
    """Resolve path to a bundled resource; works in dev and PyInstaller exe."""
    if hasattr(sys, '_MEIPASS'):
        return Path(sys._MEIPASS) / relative_path
    return Path(__file__).parent / relative_path

# TEMP: Will need to be changed to be more dynamic
MASTERTEMPLATE_FILEPATH = resource_path("supporting_docs/sorted_econ_files/MASTERTEMPLATE (color coded kind of).xlsx")

# TEMP: Will need to be changed to be more dynamic
OUTPUT_TEMPLATE_FILEPATH = resource_path("data_output_files/output_templates/Default Output Template.docx")

# TEMP: Will need to be changed to be more dynamic
OUTPUT_SAVE_PATH = resource_path("data_output_files/output_files")

class EconWorkflowAutomation:
    def __init__(self, mastertemplate_filepath: str, output_template_filepath: str, output_save_path: str):
        # DEFINING CLASS ATTRIBUTES
        self.mastertemplate_filepath = mastertemplate_filepath # TEMP: Will need to be changed to be more dynamic
        self.output_template_filepath = output_template_filepath # TEMP: Will need to be changed to be more dynamic
        self.output_save_path = output_save_path # TEMP: Will need to be changed to be more dynamic
        
        # CALLING METHODS
        self.run_workflow()
    
    def run_workflow(self):
        """
        Runs the main workflow of the application.
        """
        # CALLING SUB-CLASS METHODS
        self.masterdata_extractor = MasterTemplateExtractor(active_workbook_path=str(self.mastertemplate_filepath))
        self.word_template_processor = WordTemplateProcessor(extracted_data_dict=self.masterdata_extractor.extracted_data, template_filepath=str(self.output_template_filepath), output_save_path=str(self.output_save_path))