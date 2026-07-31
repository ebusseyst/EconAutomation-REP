import logging
import logging.config

import yaml

from econ_automation.ea_scripts.gui_files.gui_core.gui_core_codebase import (
    EAMainWindow,
)

from econ_automation.ea_scripts.gui_files.gui_connections.gui_formatted_functions import (
    select_OFF_file_modal,
    select_claimant_folder_modal,
    create_case_function,
)


# Top-level logger instance
with open(r"src/logging_resources/logging_config.yaml", "r") as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)


class GUIFormattedFunctionsHandler:
    def __init__(self, ea_main_window: EAMainWindow) -> None:
        self.eaMainWindow = ea_main_window
        self.ui = self.eaMainWindow.ui

    def update_selected_OFF_label(self, claimant_name: str, file_path: str) -> None:
        """
        Updates the selected OFF label in the GUI.
        """
        self.ui.ea_setupcase_selectedOFF_label.setText(f"Selected: {claimant_name}")
        self.ui.ea_setupcase_selectedOFF_label.setToolTip(file_path)
