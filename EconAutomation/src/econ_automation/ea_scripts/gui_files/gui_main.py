import ctypes
import logging
import sys
from pathlib import Path
import platform

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
from econ_automation.ea_scripts.report_merge_scripts.pv_earnings_context_codebase import (
    PVEarningsToggles,
)
from econ_automation.ea_scripts.report_merge_scripts.pvlcp_context_codebase import (
    PVLCPToggles,
)
from econ_automation.ea_scripts.ea_main_codebase import run_extraction_and_report_merge

setup_logging()

logger = logging.getLogger(__name__)


class EconAutomationMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_ea_MainWindow(self)
        self.ui.setupUi()
        self._setup_comboboxes()
        self._connect_signals()

    # ── Setup ─────────────────────────────────────────────────────────────────

    def _setup_comboboxes(self) -> None:
        """Populate comboboxes with their allowed values."""
        proj = self.ui.ea_reportmerge_projectiontype_combobox
        proj.addItem("WLE", "WLE")
        proj.addItem("To Age", "toage")

        ref = self.ui.ea_reportmerge_referencetype_combobox
        ref.addItem("LCP", "LCP")
        ref.addItem("MCP", "MCP")
        ref.addItem("LCP + MCP", "LCP+MCP")

    def _connect_signals(self) -> None:
        self.ui.ea_reportmerge_button.clicked.connect(self._on_merge_clicked)

    # ── Slots ──────────────────────────────────────────────────────────────────

    def _on_merge_clicked(self) -> None:
        ui = self.ui
        gui_overrides: dict = {}
        if ui.ea_reportmerge_reporttypes_PVearnings_checkbox.isChecked():
            gui_overrides["PV_Earnings_Report_Template"] = self._collect_pv_earnings_toggles()
        if ui.ea_reportmerge_reporttypes_PVLCP_checkbox.isChecked():
            gui_overrides["PVLCP_Report_Template"] = self._collect_pvlcp_toggles()
        try:
            run_extraction_and_report_merge(gui_overrides=gui_overrides or None)
        except Exception:
            logger.exception("Report merge failed")

    # ── Helpers ────────────────────────────────────────────────────────────────

    def _collect_pv_earnings_toggles(self) -> PVEarningsToggles:
        """Read all relevant GUI widgets and return a PVEarningsToggles instance."""
        ui = self.ui

        rehab: list[str] = []
        if ui.ea_reportmerge_reporttypes_PVLCP_checkbox.isChecked():
            rehab.append("LCP")
        # When a Voc checkbox is added: if ui.<voc_checkbox>.isChecked(): rehab.append("Voc")

        return PVEarningsToggles(
            base1_toggle=ui.ea_reportmerge_base1_checkbox.isChecked(),
            base2_toggle=ui.ea_reportmerge_base2_checkbox.isChecked(),
            base3_toggle=ui.ea_reportmerge_base3_checkbox.isChecked(),
            credit1_toggle=ui.ea_reportmerge_credit1_checkbox.isChecked(),
            credit2_toggle=ui.ea_reportmerge_credit2_checkbox.isChecked(),
            credit3_toggle=ui.ea_reportmerge_credit3_checkbox.isChecked(),
            meals_toggle=ui.ea_reportmerge_meals_checkbox.isChecked(),
            benefits_toggle=ui.ea_reportmerge_benefits_checkbox.isChecked(),
            taxed_toggle=ui.ea_reportmerge_taxstatus_checkbox.isChecked(),
            projection_type_toggle=ui.ea_reportmerge_projectiontype_combobox.currentData(),
            rehab_report_types=rehab,
        )

    def _collect_pvlcp_toggles(self) -> PVLCPToggles:
        """Read the Reference Type combobox and return a PVLCPToggles instance."""
        ref_data = self.ui.ea_reportmerge_referencetype_combobox.currentData()
        if ref_data == "LCP+MCP":
            rehab = ["LCP", "MCP"]
        elif ref_data in ("LCP", "MCP"):
            rehab = [ref_data]
        else:
            rehab = ["LCP"]  # safe default if combobox is unpopulated
        return PVLCPToggles(rehab_report_types=rehab)


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

        self.ea_main_window = EconAutomationMainWindow()
        self.ea_main_window.setWindowIcon(
            QIcon(str(Path(r"src/gui_resources/images/starfire.png")))
        )

        self.ea_main_window.show()


if __name__ == "__main__":
    myappid = "StarFire"
    if platform.system() == "Windows":
        # pyrefly: ignore [missing-attribute]
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    ea_app = eaApp(argv=sys.argv)
    ea_app.exec()
