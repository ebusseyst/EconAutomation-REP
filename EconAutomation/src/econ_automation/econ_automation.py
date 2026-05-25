import logging
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox

from logging_resources.log_context import setup_logging
# from econ_automation.ea_scripts.gui_files.gui_core.current_ea_gui import (
#     Ui_ea_MainWindow,
# )
# from econ_automation.ea_scripts.update_scripts.update_codebase import (
#     check_and_apply_update,
# )

from econ_automation.ea_scripts.ea_main_codebase import (
    run_extraction_and_report_merge,
)

setup_logging()

logger = logging.getLogger(__name__)


# def _update_prompt(message: str) -> bool:
#     """Show a QMessageBox asking the user whether to install an available update."""
#     dialog = QMessageBox()
#     dialog.setWindowTitle("Update Available")
#     dialog.setText(message)
#     dialog.setStandardButtons(
#         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
#     )
#     dialog.setDefaultButton(QMessageBox.StandardButton.Yes)
#     return dialog.exec() == QMessageBox.StandardButton.Yes


if __name__ == "__main__":
    run_extraction_and_report_merge()
    # app = QApplication(sys.argv)

    # # Set the color scheme to Light manually
    # app.styleHints().setColorScheme(Qt.ColorScheme.Light)

    # # Assign user-facing app name
    # app.setApplicationDisplayName("EconLightning")
    # app.setApplicationName("EconLightning")

    # # Check for updates before showing the main window
    # check_and_apply_update(prompt_fn=_update_prompt)

    # main_window = QMainWindow()
    # main_window_ui = Ui_ea_MainWindow(ea_MainWindow=main_window)
    # main_window_ui.setupUi()

    # main_window.show()
    # app.exec()
