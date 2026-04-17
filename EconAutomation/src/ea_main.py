import logging
import logging.config
from pathlib import Path
import datetime

import yaml

from ea_scripts.ea_main_codebase import EconWorkflowAutomation

# Top-level logger instance
with open("src/logging_resources/logging_config.yaml", "r") as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)
    
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # TEMP: PULLING TODAY'S DATE
    today = datetime.date.today()
    today_str = today.strftime("%Y-%m-%d")
    
    # DEFINING FILE PATHS (TO BE CHANGED LATER)
    mastertemplate_filepath = Path("C:\\Users\\EricBussey\\GitHub\\EconAutomation-REP\\EconAutomation\\src\\supporting_docs\\original_econ_files\\MASTERTEMPLATE.xlsx")
    output_template_filepath = Path("C:\\Users\\EricBussey\\GitHub\\EconAutomation-REP\\EconAutomation\\src\\supporting_docs\\econ_report_templates\\LCP_mastertemplate_report_template.docx")
    output_save_path = Path(f"C:\\Users\\EricBussey\\GitHub\\EconAutomation-REP\\EconAutomation\\src\\supporting_docs\\ea_generated_reports\\{today_str} gen_LCP_report.docx")
    
    econ_workflow_automation = EconWorkflowAutomation(mastertemplate_filepath, output_template_filepath, output_save_path)
    econ_workflow_automation.run_workflow()