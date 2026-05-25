import ctypes
import logging
import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox

from logging_resources.log_context import setup_logging
from econ_automation.ea_scripts.gui_files.gui_core.current_ea_gui import (
    Ui_ea_MainWindow,
)
from econ_automation.ea_scripts.update_scripts.update_codebase import (
    check_and_apply_update,
)

setup_logging()

class EconAutomationMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_ea_MainWindow(self)
        self.ui.setupUi()


logger = logging.getLogger(__name__)


def _update_prompt(message: str) -> bool:
    """Show a QMessageBox asking the user whether to install an available update."""
    dialog = QMessageBox()
    dialog.setWindowTitle("Update Available")
    dialog.setText(message)
    dialog.setStandardButtons(
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    )
    dialog.setDefaultButton(QMessageBox.StandardButton.Yes)
    return dialog.exec() == QMessageBox.StandardButton.Yes


class eaApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)

        # Set the color scheme to Light manually
        self.styleHints().setColorScheme(Qt.ColorScheme.Light)

        # Assign user-facing app name
        self.setApplicationDisplayName("StarFire")
        self.setApplicationName("StarFire")

        # Check for updates before showing the main window
        check_and_apply_update(prompt_fn=_update_prompt)

        self.ea_main_window = QMainWindow()
        self.ea_main_window.setWindowIcon(
            QIcon(str(Path(r"src/gui_resources/images/starfire.png")))
        )
        self.ea_main_window_ui = Ui_ea_MainWindow(ea_MainWindow=self.ea_main_window)
        self.ea_main_window_ui.setupUi()

        self.ea_main_window.show()


if __name__ == "__main__":
    myappid = "StarFire"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    ea_app = eaApp(argv=sys.argv)
    ea_app.exec()
