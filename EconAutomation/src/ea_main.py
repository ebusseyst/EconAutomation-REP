import logging
import logging.config
from pathlib import Path
import datetime
import sys

import yaml

from ea_scripts.ea_main_codebase import EconWorkflowAutomation

# Top-level logger instance
with open("src/logging_resources/logging_config.yaml", "r") as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)
    
logger = logging.getLogger(__name__)

# Resource path function
def resource_path(relative_path: str) -> Path:
    """Resolve path to a bundled resource; works in dev and PyInstaller exe."""
    if hasattr(sys, '_MEIPASS'):
        return Path(sys._MEIPASS) / relative_path
    return Path(__file__).parent / relative_path

# TEMP: Will need to be changed to be more dynamic
MASTERTEMPLATE_FILEPATH = resource_path("supporting_docs/sorted_econ_files/MASTERTEMPLATE (color coded).xlsx")
WORKING_CALC_FILEPATH = resource_path("supporting_docs/sorted_econ_files/Working_CALC_VER1.11 (color coded).xlsx")
PV2_FILEPATH = resource_path("supporting_docs/sorted_econ_files/PV2 (color coded).xlsx")
HHS_FILEPATH = resource_path("supporting_docs/sorted_econ_files/HHS_PV_New (color coded).xlsx")

# TEMP: Will need to be changed to be more dynamic
EARNINGS_AND_PV_MEDS_TEMPLATE_FILEPATH = resource_path("supporting_docs/sorted_econ_files/Earnings and PV Meds Report Template (color coded).docx")
LCP_TEMPLATE_FILEPATH = resource_path("supporting_docs/sorted_econ_files/LCP MASTERTEMPLATE (color coded).docx")

# TEMP: Will need to be changed to be more dynamic
OUTPUT_SAVE_DIRECTORY = resource_path("data_output_files/output_files")

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
    input_workbooks_filepaths_dict = {
        "mastertemplate_filepath": MASTERTEMPLATE_FILEPATH,
        "working_calc_filepath": WORKING_CALC_FILEPATH,
        "pv2_filepath": PV2_FILEPATH,
        "hhs_filepath": HHS_FILEPATH
        }
        
    output_template_filepaths_dict = {
        "lcp_report_template_filepath": LCP_TEMPLATE_FILEPATH,
        }
    
    output_save_paths_list = [
        fr"{OUTPUT_SAVE_DIRECTORY}"
        ]
    
    econ_workflow_automation = EconWorkflowAutomation(input_workbooks_filepaths_dict, output_template_filepaths_dict, output_save_paths_list)