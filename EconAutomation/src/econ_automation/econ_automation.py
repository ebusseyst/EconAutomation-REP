import logging
import logging.config
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
import yaml

from econ_automation.ea_scripts.gui_files.gui_core.current_ea_gui import Ui_ea_MainWindow
from econ_automation.ea_scripts.update_scripts.update_codebase import check_and_apply_update

# Top-level logger instance
with open(r"src/logging_resources/logging_config.yaml", "r") as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)
logger.error("This is an error log")
logger.info("This is an info log")

def _update_prompt(message: str) -> bool:
    """Show a QMessageBox asking the user whether to install an available update."""
    dialog = QMessageBox()
    dialog.setWindowTitle("Update Available")
    dialog.setText(message)
    dialog.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    dialog.setDefaultButton(QMessageBox.StandardButton.Yes)
    return dialog.exec() == QMessageBox.StandardButton.Yes


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set the color scheme to Light manually
    app.styleHints().setColorScheme(Qt.ColorScheme.Light)

    # Assign user-facing app name
    app.setApplicationDisplayName("EconLightning")
    app.setApplicationName("EconLightning")

    # Check for updates before showing the main window
    check_and_apply_update(prompt_fn=_update_prompt)

    main_window = QMainWindow()
    main_window_ui = Ui_ea_MainWindow(ea_MainWindow=main_window)
    main_window_ui.setupUi()

    main_window.show()
    app.exec()