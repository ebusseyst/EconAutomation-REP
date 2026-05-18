import logging
import logging.config

from PySide6.QtWidgets import QMainWindow
import yaml

from econ_automation.ea_scripts.gui_files.gui_core.current_ea_gui import Ui_ea_MainWindow


# Top-level logger instance
with open(r"src/logging_resources/logging_config.yaml", "r") as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)

class EAMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_ea_MainWindow(self)
        self.ui.setupUi()


class GUIConnectionsHandler:
    def __init__(self) -> None:
        self.eaMainWindow = EAMainWindow()
        
    def connect_buttons(self, ui: Ui_ea_MainWindow, main_window: QMainWindow):
        """
        Connects all the buttons in the GUI to their respective functions.
        """
        # NEW CASE SET UP BUTTONS
        # self.eaMainWindow.ui.ea_setupcase_OFFSelect_button.clicked.connect(setupcase_OFFSelect_button_function)
        # self.eaMainWindow.ui.ea_setupcase_createcase_button.clicked.connect(setupcase_createcase_button_function)
        
        # REPORT MERGE BUTTONS
        # self.eaMainWindow.ui.ea_reportmerge_button.clicked.connect(reportmerge_button_function)
        
    def connect_checkboxes(self, ui: Ui_ea_MainWindow, ea_main_window: QMainWindow):
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
        
        
        
    def connect_comboboxes(self, ui: Ui_ea_MainWindow, ea_main_window: QMainWindow):
        """
        Connects all the comboboxes in the GUI to their respective functions.
        """
        # REPORT MERGE COMBOBOXES
        
            # Earnings Projection Type
        # self.eaMainWindow.ui.ea_reportmerge_projectiontype_combobox.currentIndexChanged.connect(ea_reportmerge_projectiontype_combobox_function)
            
            # Reference Type
        # self.eaMainWindow.ui.ea_reportmerge_referencetype_combobox.currentIndexChanged.connect(ea_reportmerge_referencetype_combobox_function)
