from pathlib import Path

from econ_automation.ea_scripts.case_setup_scripts.case_folder_setup_codebase import create_case_profile
from econ_automation.ea_scripts.report_merge_scripts.report_merge_codebase import merge_reports_core


# TEST FILEPATHS
sel_OFF_filepath = Path(
    r"/Users/ericmacbook/Documents/GitHub/EconAutomation-REP/EconAutomation/src/supporting_docs/sample_OFFs/Gaston, C -- TEST Open File Form.docx"
)

base_filepaths = {
    "Private Directory": Path(
        r"/Users/ericmacbook/Documents/GitHub/EconAutomation-REP/EconAutomation/ea_outputs/private_claimant_directories"
    ),
    "Public Directory": Path(
        r"/Users/ericmacbook/Documents/GitHub/EconAutomation-REP/EconAutomation/ea_outputs/public_claimant_directories"
    ),
}

wb_template_dir = Path(
    r"/Users/ericmacbook/Documents/GitHub/EconAutomation-REP/EconAutomation/src/supporting_docs/econ_wb_templates"
)

report_template_dir = Path(
    r"/Users/ericmacbook/Documents/GitHub/EconAutomation-REP/EconAutomation/src/supporting_docs/econ_report_templates"
)

if __name__ == "__main__":
    ea_main_dataclass = create_case_profile(sel_OFF_filepath)
    merge_reports_core(ea_main_dataclass=ea_main_dataclass, selected_template_filepaths=[Path(r"/Users/ericmacbook/Documents/GitHub/EconAutomation-REP/EconAutomation/src/supporting_docs/econ_report_templates/PV_Earnings_Report_Template.docx")], selected_output_filepaths=[base_filepaths["Private Directory"]])
