from __future__ import annotations

from pathlib import Path
import logging

try:
    import pythoncom as _pythoncom

    _USE_COM = True
except ImportError:
    _USE_COM = False

from PySide6.QtCore import Qt, Signal, QThread
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
)

from econ_automation.ea_scripts.case_setup_scripts.case_folder_setup_codebase import (
    create_folder_only,
    setup_workbooks_from_profile,
)
from econ_automation.ea_scripts.file_system_scripts.file_system_codebase import (
    FileSystemCore,
)
from econ_automation.ea_scripts.gui_files.gui_connections.gui_formatted_functions import (
    create_case_function,
)
from econ_automation.ea_scripts.ea_main_codebase import (
    build_selected_files_dict,
    run_extraction_and_report_merge,
)

logger = logging.getLogger(__name__)


class EAProgressDialog(QDialog):
    def __init__(self, parent, title: str, colors: dict):
        super().__init__(parent)
        self._colors = colors
        self._result_dir: Path | None = None
        self._worker_done = False
        self._error_message: str | None = None
        self._setup_ui(title)
        self._apply_style()
        self.setModal(True)
        self.setFixedWidth(420)
        self.setWindowTitle(title)

    def _setup_ui(self, title: str) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 20)
        layout.setSpacing(14)

        self._title_label = QLabel(title)
        self._title_label.setObjectName("progress_title")
        self._title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._title_label)

        sep = QFrame()
        sep.setObjectName("progress_sep")
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setFixedHeight(1)
        layout.addWidget(sep)

        self._step_label = QLabel("Initializing...")
        self._step_label.setObjectName("progress_step")
        self._step_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._step_label.setWordWrap(True)
        layout.addWidget(self._step_label)

        self._bar = QProgressBar()
        self._bar.setObjectName("progress_bar")
        self._bar.setRange(0, 0)
        self._bar.setTextVisible(False)
        self._bar.setFixedHeight(16)
        layout.addWidget(self._bar)

        btn_row = QHBoxLayout()
        btn_row.addItem(
            QSpacerItem(
                40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
            )
        )
        self._ok_btn = QPushButton("OK")
        self._ok_btn.setObjectName("progress_ok")
        self._ok_btn.setFixedWidth(88)
        self._ok_btn.setVisible(False)
        self._ok_btn.clicked.connect(self.accept)
        btn_row.addWidget(self._ok_btn)
        layout.addLayout(btn_row)

    def _apply_style(self) -> None:
        c = self._colors
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(c["dark_navy"]))
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        self.setStyleSheet(f"""
            QLabel#progress_title {{
                color: {c["light_gold"]};
                font-size: 14pt;
                font-weight: bold;
                background-color: transparent;
            }}
            QLabel#progress_step {{
                color: {c["off_white"]};
                font-size: 11pt;
                background-color: transparent;
            }}
            QFrame#progress_sep {{
                background-color: {c["dark_gold"]};
                border: none;
            }}
            QProgressBar#progress_bar {{
                background-color: rgba(255, 255, 255, 30);
                border: 1px solid {c["gold"]};
                border-radius: 4px;
            }}
            QProgressBar#progress_bar::chunk {{
                background-color: {c["gold"]};
                border-radius: 3px;
            }}
            QPushButton#progress_ok {{
                background-color: {c["gold"]};
                color: {c["dark_navy"]};
                border: none;
                border-radius: 4px;
                padding: 6px 0px;
                font-weight: bold;
                font-size: 11pt;
            }}
            QPushButton#progress_ok:hover {{
                background-color: {c["warm_gold"]};
            }}
            QPushButton#progress_ok:pressed {{
                background-color: {c["dark_gold"]};
            }}
        """)

    def update_step(self, text: str) -> None:
        self._step_label.setText(text)

    def on_success(self, result_dir: object) -> None:
        self._result_dir = Path(str(result_dir))
        self._worker_done = True
        self._bar.setRange(0, 100)
        self._bar.setValue(100)
        self._step_label.setText("Complete!")
        self._ok_btn.setVisible(True)

    def on_error(self, message: str) -> None:
        self._worker_done = True
        self._error_message = message
        self._bar.setRange(0, 100)
        self._bar.setValue(0)
        self._step_label.setText(f"Error: {message}")
        self._ok_btn.setVisible(True)

    def had_error(self) -> bool:
        return self._error_message is not None

    def error_message(self) -> str | None:
        return self._error_message

    def result_dir(self) -> Path | None:
        return self._result_dir

    def closeEvent(self, event) -> None:
        if not self._worker_done:
            event.ignore()
        else:
            super().closeEvent(event)

    def reject(self) -> None:
        if self._worker_done:
            super().reject()


class CaseSetupWorker(QThread):
    step_changed = Signal(str)
    finished = Signal(object)
    error = Signal(str)

    def __init__(self, off_path: str, admin_bool: bool):
        super().__init__()
        self._off_path = off_path
        self._admin_bool = admin_bool

    def _emit_step(self, msg: str) -> None:
        self.step_changed.emit(msg)
        logger.info(msg)

    def run(self) -> None:
        if _USE_COM:
            _pythoncom.CoInitialize()
        try:
            claimant_dir = create_case_function(
                OFF_filepath=self._off_path,
                admin_bool=self._admin_bool,
                progress_callback=self._emit_step,
            )
            self.finished.emit(claimant_dir)
        except Exception as exc:
            logger.exception("Case setup failed in worker")
            self.error.emit(str(exc))
        finally:
            if _USE_COM:
                _pythoncom.CoUninitialize()


class CreateFolderWorker(QThread):
    step_changed = Signal(str)
    finished = Signal(object)
    error = Signal(str)

    def __init__(self, case_profile, admin_bool: bool):
        super().__init__()
        self._case_profile = case_profile
        self._admin_bool = admin_bool

    def _emit_step(self, msg: str) -> None:
        self.step_changed.emit(msg)
        logger.info(msg)

    def run(self) -> None:
        if _USE_COM:
            _pythoncom.CoInitialize()
        try:
            fs = FileSystemCore()
            base_filepaths = fs.main_filepaths_dict["base_filepaths"]
            claimant_dir = create_folder_only(
                case_profile=self._case_profile,
                base_filepaths=base_filepaths,
                admin_bool=self._admin_bool,
                progress_callback=self._emit_step,
            )
            self.finished.emit(claimant_dir)
        except Exception as exc:
            logger.exception("Folder creation failed in worker")
            self.error.emit(str(exc))
        finally:
            if _USE_COM:
                _pythoncom.CoUninitialize()


class SetupWorkbooksWorker(QThread):
    step_changed = Signal(str)
    finished = Signal(object)
    error = Signal(str)

    def __init__(self, case_profile, admin_bool: bool):
        super().__init__()
        self._case_profile = case_profile
        self._admin_bool = admin_bool

    def _emit_step(self, msg: str) -> None:
        self.step_changed.emit(msg)
        logger.info(msg)

    def run(self) -> None:
        if _USE_COM:
            _pythoncom.CoInitialize()
        try:
            import platform as _platform

            fs = FileSystemCore()
            base_filepaths = fs.main_filepaths_dict["base_filepaths"]
            platform_key = "Mac" if _platform.system() == "Darwin" else "Windows"
            wb_template_dir = fs.main_filepaths_dict["wb_template_dir"][platform_key]
            claimant_dir = setup_workbooks_from_profile(
                case_profile=self._case_profile,
                base_filepaths=base_filepaths,
                wb_template_dir=wb_template_dir,
                admin_bool=self._admin_bool,
                progress_callback=self._emit_step,
            )
            self.finished.emit(claimant_dir)
        except Exception as exc:
            logger.exception("Workbook setup failed in worker")
            self.error.emit(str(exc))
        finally:
            if _USE_COM:
                _pythoncom.CoUninitialize()


class ReportMergeWorker(QThread):
    step_changed = Signal(str)
    finished = Signal(object)
    error = Signal(str)

    def __init__(
        self,
        claimant_dir: Path,
        requested_template_keys: list[str] | None,
        gui_overrides: dict | None,
    ):
        super().__init__()
        self._claimant_dir = claimant_dir
        self._requested_template_keys = requested_template_keys
        self._gui_overrides = gui_overrides

    def _emit_step(self, msg: str) -> None:
        self.step_changed.emit(msg)
        logger.info(msg)

    def run(self) -> None:
        if _USE_COM:
            _pythoncom.CoInitialize()
        try:
            self._emit_step("Building file list...")
            selected_files = build_selected_files_dict(
                self._claimant_dir,
                requested_template_keys=self._requested_template_keys,
            )
            run_extraction_and_report_merge(
                selected_files_dict=selected_files,
                gui_overrides=self._gui_overrides,
                progress_callback=self._emit_step,
            )
            self.finished.emit(self._claimant_dir)
        except Exception as exc:
            logger.exception("Report merge failed in worker")
            self.error.emit(str(exc))
        finally:
            if _USE_COM:
                _pythoncom.CoUninitialize()
