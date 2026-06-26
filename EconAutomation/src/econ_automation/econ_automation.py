import ctypes
import logging
import subprocess
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
    save_install_location,
)
from econ_automation.ea_scripts.report_merge_scripts.pv_earnings_context_codebase import (
    PVEarningsToggles,
)
from econ_automation.ea_scripts.report_merge_scripts.pvlcp_context_codebase import (
    PVLCPToggles,
)

from econ_automation.ea_scripts.gui_files.gui_connections.gui_formatted_functions import (
    select_OFF_file_modal,
    select_claimant_folder_modal,
)
from econ_automation.ea_scripts.gui_files.gui_core.case_info_dialogs import (
    BugReportDialog,
    ConfirmCaseInfoDialog,
    CreateFolderDialog,
)
from econ_automation.ea_scripts.gui_files.gui_core.ea_progress_dialog import (
    CaseSetupWorker,
    CreateFolderWorker,
    EAProgressDialog,
    ReportMergeWorker,
    SetupWorkbooksWorker,
)
from econ_automation.ea_scripts.case_setup_scripts.case_folder_setup_codebase import (
    make_case_profile_from_basic_info,
)

from econ_automation._version import __version__ as app_version


setup_logging()

logger = logging.getLogger(__name__)


class EconAutomationMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_ea_MainWindow(self)
        self.ui.setupUi()
        self.ui.ea_reportmerge_reporttypes_PVLCP_checkbox.setChecked(True)
        self.ui.ea_reportmerge_referencereports_lcp_checkbox.setChecked(True)
        self.econ_cases_path = Path.home()
        self._selected_claimant_dir: Path | None = None
        self._setup_comboboxes()
        self._connect_signals()

    # ── Setup ─────────────────────────────────────────────────────────────────

    def _setup_comboboxes(self) -> None:
        proj = self.ui.ea_reportmerge_projectiontype_combobox
        proj.addItem("WLE", "WLE")
        proj.addItem("To Age", "toage")

    def _connect_signals(self) -> None:
        self.ui.ea_setupcase_createfolder_button.clicked.connect(self._on_create_folder)
        self.ui.ea_setupcase_OFFSelect_button.clicked.connect(self._on_prepare_with_off)
        self.ui.ea_setupcase_createcase_button.clicked.connect(
            self._on_prepare_without_off
        )
        self.ui.ea_reportmerge_claimantdirselect_button.clicked.connect(
            self._on_claimantdir_select
        )
        self.ui.ea_reportmerge_button.clicked.connect(self._on_merge_clicked)
        self.ui.ea_bugreport_button.clicked.connect(self._on_bug_report)

    # ── Slots ──────────────────────────────────────────────────────────────────

    def _on_create_folder(self) -> None:
        dlg = CreateFolderDialog(self, self.ui._color_dict)
        if dlg.exec() != CreateFolderDialog.DialogCode.Accepted:
            return
        data = dlg.form_data()
        case_profile = make_case_profile_from_basic_info(data)
        progress = EAProgressDialog(
            self, "Creating Claimant Folder", self.ui._color_dict
        )
        worker = CreateFolderWorker(case_profile, admin_bool=False)
        worker.step_changed.connect(progress.update_step)
        worker.finished.connect(progress.on_success)
        worker.error.connect(progress.on_error)
        worker.start()
        progress.exec()
        worker.wait()
        if progress.had_error():
            self._offer_bug_report(progress.error_message())
            return
        claimant_dir = progress.result_dir()
        if claimant_dir is not None:
            self._open_in_explorer(claimant_dir)

    def _on_prepare_with_off(self) -> None:
        claimant_name, file_path = select_OFF_file_modal(self)
        if not file_path:
            return
        progress = EAProgressDialog(self, "Setting Up Case", self.ui._color_dict)
        worker = CaseSetupWorker(file_path, admin_bool=False)
        worker.step_changed.connect(progress.update_step)
        worker.finished.connect(progress.on_success)
        worker.error.connect(progress.on_error)
        worker.start()
        progress.exec()
        worker.wait()
        if progress.had_error():
            self._offer_bug_report(progress.error_message())
            return
        claimant_dir = progress.result_dir()
        if claimant_dir is not None:
            self._open_in_explorer(claimant_dir / "Work Products")

    def _on_prepare_without_off(self) -> None:
        dlg = ConfirmCaseInfoDialog(self, self.ui._color_dict)
        if dlg.exec() != ConfirmCaseInfoDialog.DialogCode.Accepted:
            return
        case_profile = make_case_profile_from_basic_info(dlg.form_data())
        progress = EAProgressDialog(self, "Setting Up Case", self.ui._color_dict)
        worker = SetupWorkbooksWorker(case_profile, admin_bool=False)
        worker.step_changed.connect(progress.update_step)
        worker.finished.connect(progress.on_success)
        worker.error.connect(progress.on_error)
        worker.start()
        progress.exec()
        worker.wait()
        if progress.had_error():
            self._offer_bug_report(progress.error_message())
            return
        claimant_dir = progress.result_dir()
        if claimant_dir is not None:
            self._open_in_explorer(claimant_dir / "Work Products")

    def _on_claimantdir_select(self) -> None:
        result = select_claimant_folder_modal(self, "Select Econ Claimant Folder")
        if result:
            self._selected_claimant_dir = Path(result)
        label = self.ui.ea_reportmerge_selectedclaimantdir_label
        label.setText(
            Path(result).name if result else "No Econ claimant folder selected."
        )

    def _on_merge_clicked(self) -> None:
        if self._selected_claimant_dir is None:
            QMessageBox.warning(
                self,
                "No Claimant Folder Selected",
                "Please select an econ claimant folder in the 'Report Merge' section before merging.",
            )
            return

        ui = self.ui
        gui_overrides: dict = {}
        requested_template_keys: list[str] = []

        if ui.ea_reportmerge_reporttypes_PVearnings_checkbox.isChecked():
            gui_overrides["PV_Earnings_Report_Template"] = (
                self._collect_pv_earnings_toggles()
            )
            requested_template_keys.append("PV_EARNINGS_TEMPLATE")
        if ui.ea_reportmerge_reporttypes_PVLCP_checkbox.isChecked():
            gui_overrides["PVLCP_Report_Template"] = self._collect_pvlcp_toggles()
            requested_template_keys.append("PVLCP_TEMPLATE")

        dialog = EAProgressDialog(self, "Merging Reports", self.ui._color_dict)
        worker = ReportMergeWorker(
            claimant_dir=self._selected_claimant_dir,
            requested_template_keys=requested_template_keys or None,
            gui_overrides=gui_overrides or None,
        )
        worker.step_changed.connect(dialog.update_step)
        worker.finished.connect(dialog.on_success)
        worker.error.connect(dialog.on_error)
        worker.start()
        dialog.exec()
        worker.wait()
        if dialog.had_error():
            self._offer_bug_report(dialog.error_message())
            return
        if dialog.result_dir() is not None:
            self._open_in_explorer(self._selected_claimant_dir / "Reports and Invoices")

    # ── Helpers ────────────────────────────────────────────────────────────────

    def _on_bug_report(self) -> None:
        BugReportDialog(self, self.ui._color_dict).exec()

    def _offer_bug_report(self, error_msg: str | None) -> None:
        answer = QMessageBox.question(
            self,
            "Report Bug",
            "An error occurred. Would you like to submit a bug report?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes,
        )
        if answer == QMessageBox.StandardButton.Yes:
            BugReportDialog(self, self.ui._color_dict, error_message=error_msg).exec()

    def _open_in_explorer(self, path: Path) -> None:
        if platform.system() == "Darwin":
            subprocess.Popen(["open", str(path)])
        else:
            subprocess.Popen(["explorer", str(path)])

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


def _force_taskbar_icon(hwnd: int, ico_path: str) -> None:
    """Send WM_SETICON directly — Qt sometimes skips ICON_BIG on the Windows taskbar."""
    WM_SETICON = 0x0080
    IMAGE_ICON = 1
    LR_LOADFROMFILE = 0x0010
    LR_DEFAULTSIZE = 0x0040

    # pyrefly: ignore [missing-attribute]
    user32 = ctypes.windll.user32
    hicon = user32.LoadImageW(
        None, ico_path, IMAGE_ICON, 0, 0, LR_LOADFROMFILE | LR_DEFAULTSIZE
    )
    if hicon:
        user32.SendMessageW(hwnd, WM_SETICON, 1, hicon)  # ICON_BIG  → taskbar
        user32.SendMessageW(hwnd, WM_SETICON, 0, hicon)  # ICON_SMALL → title bar


def _update_prompt(message: str, parent=None) -> bool:
    dialog = QMessageBox(parent)
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

        # QRC resource — always available (compiled into ea_iconset1.py, imported above)
        _qrc_icon = QIcon(":/icons/bolt_boost_icon.ico")
        self.setWindowIcon(_qrc_icon)

        # Filesystem path — needed only for Win32 LoadImageW in _force_taskbar_icon
        if getattr(sys, "frozen", False):
            _ico = (
                # pyrefly: ignore [missing-attribute]
                Path(sys._MEIPASS)
                / "econ_automation/ea_scripts/gui_files/icons/bolt_boost_icon.ico"
            )
        else:
            _ico = (
                Path(__file__).resolve().parent
                / "ea_scripts/gui_files/icons/bolt_boost_icon.ico"
            )

        self.styleHints().setColorScheme(Qt.ColorScheme.Light)

        self.setApplicationDisplayName(f"EconAutomation v{app_version}")
        self.setApplicationName(f"EconAutomation v{app_version}")

        save_install_location()

        self.ea_main_window = EconAutomationMainWindow()
        self.ea_main_window.setWindowTitle(f"EconAutomation v{app_version}")
        self.ea_main_window.setWindowIcon(_qrc_icon)
        self.ea_main_window.show()

        if platform.system() == "Windows" and _ico.exists():
            _ico_str = str(_ico)
            # pyrefly: ignore [unnecessary-type-conversion]
            hwnd = int(self.ea_main_window.winId())
            QTimer.singleShot(0, lambda: _force_taskbar_icon(hwnd, _ico_str))

        # Check after show() so the dialog has a rendered parent window and
        # appears centered on it rather than as an orphaned system dialog.
        check_and_apply_update(
            prompt_fn=lambda msg: _update_prompt(msg, self.ea_main_window)
        )


def main() -> None:
    myappid = "EconAutomation.App"
    if platform.system() == "Windows":
        # pyrefly: ignore [missing-attribute]
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    ea_app = eaApp(argv=sys.argv)
    ea_app.exec()


if __name__ == "__main__":
    main()
