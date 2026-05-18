import logging
import logging.config

from PySide6.QtWidgets import QMainWindow
import yaml

from econ_automation.ea_scripts.gui_files.gui_core.gui_core_codebase import (
    EAMainWindow,
)

from econ_automation.ea_scripts.gui_files.gui_connections.gui_formatted_functions import (
    OFF_select_function,
    create_case_function,
    set_selected_OFF_label,
)


# Top-level logger instance
with open(r"src/logging_resources/logging_config.yaml", "r") as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)


class GUIConnectionsHandler:
    def __init__(self) -> None:
        self.eaMainWindow = EAMainWindow()

    def connect_buttons(self, ea_main_window: EAMainWindow):
        """
        Connects all the buttons in the GUI to their respective functions.
        """
        # NEW CASE SET UP BUTTONS
        # self.eaMainWindow.ui.ea_setupcase_OFFSelect_button.clicked.connect(setupcase_OFFSelect_button_function)
        # self.eaMainWindow.ui.ea_setupcase_createcase_button.clicked.connect(setupcase_createcase_button_function)

        # REPORT MERGE BUTTONS
        # self.eaMainWindow.ui.ea_reportmerge_button.clicked.connect(reportmerge_button_function)

    def connect_checkboxes(self, ea_main_window: EAMainWindow):
        """
        Connects all the checkboxes in the GUI to their respective functions.
        """
        # REPORT MERGE CHECKBOXES

        # Report Type(s)
        # self.eaMainWindow.ui.ea_reportmerge_reporttypes_PVLCP_checkbox.connect(reportmerge_reporttypes_PVLCP_function)
        # self.eaMainWindow.ui.ea_reportmerge_reporttypes_PVearnings_checkbox.connect(reportmerge_reporttypes_PVearnings_function)

        # Base(s)
        # self.eaMainWindow.ui.ea_reportmerge_base1_checkbox.stateChanged.connect(reportmerge_base1_checkbox_function)
        # self.eaMainWindow.ui.ea_reportmerge_base2_checkbox.stateChanged.connect(reportmerge_base2_checkbox_function)
        # self.eaMainWindow.ui.ea_reportmerge_base3_checkbox.stateChanged.connect(reportmerge_base3_checkbox_function)

        # Credit(s)
        # self.eaMainWindow.ui.ea_reportmerge_credit1_checkbox.stateChanged.connect(reportmerge_credit1_checkbox_function)
        # self.eaMainWindow.ui.ea_reportmerge_credit2_checkbox.stateChanged.connect(reportmerge_credit2_checkbox_function)
        # self.eaMainWindow.ui.ea_reportmerge_credit3_checkbox.stateChanged.connect(reportmerge_credit3_checkbox_function)

        # Meals
        # self.eaMainWindow.ui.ea_reportmerge_meals_checkbox.stateChanged.connect(reportmerge_meals_checkbox_function)

        # Tax Status
        # self.eaMainWindow.ui.ea_reportmerge_taxstatus_checkbox.stateChanged.connect(reportmerge_taxstatus_checkbox_function)

        # PLACEHOLDER REPORT MERGE CHECKBOXES

    def connect_comboboxes(self, ea_main_window: EAMainWindow):
        """
        Connects all the comboboxes in the GUI to their respective functions.
        """
        # REPORT MERGE COMBOBOXES

        # Earnings Projection Type
        # self.eaMainWindow.ui.ea_reportmerge_projectiontype_combobox.currentIndexChanged.connect(ea_reportmerge_projectiontype_combobox_function)

        # Reference Type
        # self.eaMainWindow.ui.ea_reportmerge_referencetype_combobox.currentIndexChanged.connect(ea_reportmerge_referencetype_combobox_function)


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
