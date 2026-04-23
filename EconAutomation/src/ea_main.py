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

def get_project_root() -> Path:
    """Search upwards for a marker file to find the project root."""
    for p in Path(__file__).resolve().parents:
        if (p / ".git").exists() or (p / "pyproject.toml").exists():
            return p
    return Path(__file__).resolve().parent  # Fallback

if __name__ == "__main__":
    
    # TEMP: PULLING TODAY'S DATE
    today = datetime.date.today()
    today_str = today.strftime("%Y-%m-%d")
    
    # DEFINING FILE PATHS (TO BE CHANGED LATER)
    mastertemplate_filepath = fr"C:\Users\EricBussey\GitHub\EconAutomation-REP\EconAutomation\src\supporting_docs\original_econ_files\MASTERTEMPLATE.xlsx"
    output_template_filepath = fr"C:\Users\EricBussey\GitHub\EconAutomation-REP\EconAutomation\src\supporting_docs\econ_report_templates\LCP_mastertemplate_report_template.docx"
    output_save_path = fr"C:\Users\EricBussey\GitHub\EconAutomation-REP\EconAutomation\src\supporting_docs\ea_generated_reports\{today_str} gen_LCP_report.docx"
    
    econ_workflow_automation = EconWorkflowAutomation(mastertemplate_filepath, output_template_filepath, output_save_path)