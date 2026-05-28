import ctypes
import logging
import sys
from pathlib import Path
import platform

from PySide6.QtCore import Qt, QTimer
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

from econ_automation.ea_scripts.gui_files.gui_connections.gui_formatted_functions import (
    select_OFF_file_modal,
    select_claimant_folder_modal,
    create_case_function,
)


setup_logging()

logger = logging.getLogger(__name__)


class EconAutomationMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_ea_MainWindow(self)
        self.ui.setupUi()
        self.econ_cases_path = Path.home()
        self._selected_off_path: str = ""
        self._resize_timer = QTimer(self)
        self._resize_timer.setSingleShot(True)
        self._resize_timer.timeout.connect(self._on_resize_settled)
        self._setup_comboboxes()
        self._connect_signals()

    # ── Setup ─────────────────────────────────────────────────────────────────

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._resize_timer.start(120)

    def _on_resize_settled(self) -> None:
        scale = self.height() / self.ui.BASE_HEIGHT
        self.ui._apply_styles(scale)

    def _setup_comboboxes(self) -> None:
        proj = self.ui.ea_reportmerge_projectiontype_combobox
        proj.addItem("WLE", "WLE")
        proj.addItem("To Age", "toage")

    def _connect_signals(self) -> None:
        self.ui.ea_setupcase_OFFSelect_button.clicked.connect(self._on_off_select)
        self.ui.ea_setupcase_createcase_button.clicked.connect(self._on_create_case)
        self.ui.ea_reportmerge_claimantdirselect_button.clicked.connect(
            self._on_claimantdir_select
        )
        self.ui.ea_reportmerge_button.clicked.connect(self._on_merge_clicked)

    # ── Slots ──────────────────────────────────────────────────────────────────

    def _on_off_select(self) -> None:
        claimant_name, file_path = select_OFF_file_modal(self)
        self._selected_off_path = file_path
        label = self.ui.ea_setupcase_selectedOFF_label
        label.setText(claimant_name if claimant_name else "No claimant OFF selected.")

    def _on_create_case(self) -> None:
        if self._selected_off_path:
            create_case_function(self._selected_off_path)

    def _on_claimantdir_select(self) -> None:
        result = select_claimant_folder_modal(self, "Select Econ Claimant Folder")
        label = self.ui.ea_reportmerge_selectedclaimantdir_label
        label.setText(
            Path(result).name if result else "No Econ claimant folder selected."
        )

    def _on_merge_clicked(self) -> None:
        ui = self.ui
        gui_overrides: dict = {}
        if ui.ea_reportmerge_reporttypes_PVearnings_checkbox.isChecked():
            gui_overrides["PV_Earnings_Report_Template"] = (
                self._collect_pv_earnings_toggles()
            )
        if ui.ea_reportmerge_reporttypes_PVLCP_checkbox.isChecked():
            gui_overrides["PVLCP_Report_Template"] = self._collect_pvlcp_toggles()
        try:
            run_extraction_and_report_merge(gui_overrides=gui_overrides or None)
        except Exception:
            logger.exception("Report merge failed")

    # ── Helpers ────────────────────────────────────────────────────────────────

    def _collect_pv_earnings_toggles(self) -> PVEarningsToggles:
        ui = self.ui

        rehab: list[str] = []
        if ui.ea_reportmerge_referencereports_lcp_checkbox.isChecked():
            rehab.append("LCP")
        if ui.ea_reportmerge_referencereports_mcp_checkbox.isChecked():
            rehab.append("MCP")
        if ui.ea_reportmerge_referencereports_voc_checkbox.isChecked():
            rehab.append("VOC")

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
        ui = self.ui

        rehab: list[str] = []
        if ui.ea_reportmerge_referencereports_lcp_checkbox.isChecked():
            rehab.append("LCP")
        if ui.ea_reportmerge_referencereports_mcp_checkbox.isChecked():
            rehab.append("MCP")
        if ui.ea_reportmerge_referencereports_voc_checkbox.isChecked():
            rehab.append("VOC")

        return PVLCPToggles(rehab_report_types=rehab)


def _update_prompt(message: str) -> bool:
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

        self.styleHints().setColorScheme(Qt.ColorScheme.Light)

        self.setApplicationDisplayName("StarFire")
        self.setApplicationName("StarFire")

        check_and_apply_update(prompt_fn=_update_prompt)

        self.ea_main_window = EconAutomationMainWindow()
        self.ea_main_window.setWindowIcon(
            QIcon(str(Path(r"src/gui_resources/images/starfire.png")))
        )

        self.ea_main_window.show()


if __name__ == "__main__":
    myappid = "StarFire"
    if platform.system() == "Windows":
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    ea_app = eaApp(argv=sys.argv)
    ea_app.exec()
