from PySide6.QtWidgets import QMainWindow

from econ_automation.ea_scripts.gui_files.gui_core.current_ea_gui import (
    Ui_ea_MainWindow,
)


class EAMainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_ea_MainWindow(self)
        self.ui.setupUi()
