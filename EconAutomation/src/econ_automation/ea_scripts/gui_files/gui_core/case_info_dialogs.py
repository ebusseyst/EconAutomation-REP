from __future__ import annotations

import platform
import urllib.parse
from datetime import datetime as dt
from pathlib import Path

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QColor, QDesktopServices, QPalette
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QFrame,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QTextEdit,
    QVBoxLayout,
)

from econ_automation._version import __version__ as _app_version
from logging_resources.log_context import _get_log_dir
from econ_automation.ea_scripts.case_setup_scripts.case_folder_setup_codebase import (
    create_case_profile,
)
from econ_automation.ea_scripts.case_setup_scripts.case_info_persistence import (
    load_case_info,
    save_case_info,
)


def _apply_dialog_style(dialog: QDialog, colors: dict) -> None:
    c = colors
    palette = dialog.palette()
    palette.setColor(QPalette.ColorRole.Window, QColor(c["dark_navy"]))
    dialog.setPalette(palette)
    dialog.setAutoFillBackground(True)
    dialog.setStyleSheet(f"""
        QLabel#dialog_title {{
            color: {c["light_gold"]};
            font-size: 14pt;
            font-weight: bold;
            background-color: transparent;
        }}
        QFrame#dialog_sep {{
            background-color: {c["dark_gold"]};
            border: none;
        }}
        QLabel {{
            color: {c["off_white"]};
            font-size: 11pt;
            background-color: transparent;
        }}
        QLineEdit {{
            background-color: white;
            color: {c["dark_navy"]};
            border: 1px solid {c["warm_gold"]};
            border-radius: 3px;
            padding: 3px 5px;
            font-size: 11pt;
        }}
        QLineEdit:focus {{
            border: 1px solid {c["light_gold"]};
        }}
        QComboBox {{
            background-color: white;
            color: {c["dark_navy"]};
            border: 1px solid {c["warm_gold"]};
            border-radius: 3px;
            padding: 3px 5px;
            font-size: 11pt;
        }}
        QTextEdit {{
            background-color: white;
            color: {c["dark_navy"]};
            border: 1px solid {c["warm_gold"]};
            border-radius: 3px;
            padding: 3px 5px;
            font-size: 11pt;
        }}
        QTextEdit:focus {{
            border: 1px solid {c["light_gold"]};
        }}
        QCheckBox {{
            color: {c["off_white"]};
            font-size: 11pt;
            background-color: transparent;
        }}
        QPushButton#dialog_btn {{
            background-color: {c["gold"]};
            color: {c["dark_navy"]};
            border: none;
            border-radius: 4px;
            padding: 6px 16px;
            font-weight: bold;
            font-size: 11pt;
            min-width: 70px;
        }}
        QPushButton#dialog_btn:hover {{
            background-color: {c["warm_gold"]};
        }}
        QPushButton#dialog_btn:pressed {{
            background-color: {c["dark_gold"]};
        }}
    """)


def _make_separator() -> QFrame:
    sep = QFrame()
    sep.setObjectName("dialog_sep")
    sep.setFrameShape(QFrame.Shape.HLine)
    sep.setFixedHeight(1)
    return sep


class CreateFolderDialog(QDialog):
    """'Enter Basic Case Information' — collects the four name fields needed to create a claimant folder."""

    def __init__(self, parent, colors: dict):
        super().__init__(parent)
        self.setWindowTitle("Enter Basic Case Information")
        self.setModal(True)
        self.setMinimumWidth(380)
        self._colors = colors
        self._build_ui()
        _apply_dialog_style(self, colors)

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 16)
        layout.setSpacing(12)

        title = QLabel("Enter Basic Case Information")
        title.setObjectName("dialog_title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        layout.addWidget(_make_separator())

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form.setHorizontalSpacing(12)
        form.setVerticalSpacing(8)

        self._claimant_first = QLineEdit()
        self._claimant_last = QLineEdit()
        self._attorney_first = QLineEdit()
        self._attorney_last = QLineEdit()
        self._attorney_gender = QComboBox()
        self._attorney_gender.addItems(["Male", "Female"])

        form.addRow("Claimant First Name:", self._claimant_first)
        form.addRow("Claimant Last Name:", self._claimant_last)
        form.addRow("Attorney First Name:", self._attorney_first)
        form.addRow("Attorney Last Name:", self._attorney_last)
        form.addRow("Attorney Gender:", self._attorney_gender)
        layout.addLayout(form)

        btn_row = QHBoxLayout()
        btn_row.addItem(
            QSpacerItem(
                40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
            )
        )
        ok_btn = QPushButton("OK")
        ok_btn.setObjectName("dialog_btn")
        ok_btn.clicked.connect(self._on_accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("dialog_btn")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(ok_btn)
        btn_row.addWidget(cancel_btn)
        layout.addLayout(btn_row)

    def _on_accept(self) -> None:
        save_case_info(self.form_data())
        self.accept()

    def form_data(self) -> dict:
        return {
            "claimant_name_first": self._claimant_first.text().strip(),
            "claimant_name_last": self._claimant_last.text().strip(),
            "attorney_name_first": self._attorney_first.text().strip(),
            "attorney_name_last": self._attorney_last.text().strip(),
            "attorney_gender": self._attorney_gender.currentText(),
        }


class ConfirmCaseInfoDialog(QDialog):
    """'Confirm Case Information' — pre-fills from OFF cache, requests user confirmation of essential values."""

    def __init__(self, parent, colors: dict):
        super().__init__(parent)
        self.setWindowTitle("Confirm Case Information")
        self.setModal(True)
        self.setMinimumWidth(400)
        self._colors = colors
        self._build_ui()
        self._prefill()
        _apply_dialog_style(self, colors)

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 16)
        layout.setSpacing(12)

        title = QLabel("Confirm Case Information")
        title.setObjectName("dialog_title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        layout.addWidget(_make_separator())

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form.setHorizontalSpacing(12)
        form.setVerticalSpacing(8)

        self._claimant_first = QLineEdit()
        self._claimant_last = QLineEdit()
        self._attorney_first = QLineEdit()
        self._attorney_last = QLineEdit()

        form.addRow("Claimant First Name:", self._claimant_first)
        form.addRow("Claimant Last Name:", self._claimant_last)
        form.addRow("Attorney First Name:", self._attorney_first)
        form.addRow("Attorney Last Name:", self._attorney_last)

        layout.addLayout(form)
        layout.addWidget(_make_separator())

        form2 = QFormLayout()
        form2.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form2.setHorizontalSpacing(12)
        form2.setVerticalSpacing(8)

        self._trial_date_check = QCheckBox("Trial Date?")
        self._attorney_gender_combo = QComboBox()
        self._attorney_gender_combo.addItems(["Male", "Female"])
        self._gender_combo = QComboBox()
        self._gender_combo.addItems(["Male", "Female"])
        self._reference_date = QLineEdit()
        self._reference_date.setPlaceholderText("MM/DD/YYYY")
        self._dob = QLineEdit()
        self._dob.setPlaceholderText("MM/DD/YYYY")
        self._doi = QLineEdit()
        self._doi.setPlaceholderText("MM/DD/YYYY")

        form2.addRow(self._trial_date_check, QLabel(""))
        form2.addRow("Attorney Gender:", self._attorney_gender_combo)
        form2.addRow("Claimant Gender:", self._gender_combo)
        form2.addRow("Trial/Reference Date:", self._reference_date)
        form2.addRow("Claimant DOB:", self._dob)
        form2.addRow("Claimant DOI:", self._doi)
        layout.addLayout(form2)

        btn_row = QHBoxLayout()
        btn_row.addItem(
            QSpacerItem(
                40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
            )
        )
        ok_btn = QPushButton("OK")
        ok_btn.setObjectName("dialog_btn")
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("dialog_btn")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(ok_btn)
        btn_row.addWidget(cancel_btn)
        layout.addLayout(btn_row)

    def _prefill(self) -> None:
        cached = load_case_info()
        if not cached:
            return
        self._claimant_first.setText(cached.get("claimant_name_first", ""))
        self._claimant_last.setText(cached.get("claimant_name_last", ""))
        self._attorney_first.setText(cached.get("attorney_name_first", ""))
        self._attorney_last.setText(cached.get("attorney_name_last", ""))

    def form_data(self) -> dict:
        return {
            "claimant_name_first": self._claimant_first.text().strip(),
            "claimant_name_last": self._claimant_last.text().strip(),
            "attorney_name_first": self._attorney_first.text().strip(),
            "attorney_name_last": self._attorney_last.text().strip(),
            "trial_date_bool": self._trial_date_check.isChecked(),
            "attorney_gender": self._attorney_gender_combo.currentText(),
            "gender": self._gender_combo.currentText(),
            "reference_date": self._reference_date.text().strip(),
            "dob": self._dob.text().strip(),
            "doi": self._doi.text().strip(),
        }


class ConfirmReferenceData(QDialog):
    """
    Pre-fills trial date from OFF extraction.

    User confirms pre-populated trial/reference date, attorney/claimant genders, and claimant DOB/DOI.
    """

    def __init__(self, parent, colors: dict, off_path: Path) -> None:
        super().__init__(parent)
        self.setWindowTitle("Confirm Case Information")
        self.setModal(True)
        self.setMinimumWidth(400)
        self._colors = colors
        self._off_path = off_path
        self._build_ui()
        self._prefill()
        _apply_dialog_style(self, colors)

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 16)
        layout.setSpacing(12)

        title = QLabel("Confirm Case Information")
        title.setObjectName("dialog_title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        layout.addWidget(_make_separator())

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form.setHorizontalSpacing(12)
        form.setVerticalSpacing(8)

        self._claimant_first = QLineEdit()
        self._claimant_last = QLineEdit()
        self._attorney_first = QLineEdit()
        self._attorney_last = QLineEdit()

        form.addRow("Claimant First Name:", self._claimant_first)
        form.addRow("Claimant Last Name:", self._claimant_last)
        form.addRow("Attorney First Name:", self._attorney_first)
        form.addRow("Attorney Last Name:", self._attorney_last)

        layout.addLayout(form)
        layout.addWidget(_make_separator())

        form2 = QFormLayout()
        form2.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form2.setHorizontalSpacing(12)
        form2.setVerticalSpacing(8)

        self._trial_date_check = QCheckBox("Trial Date?")
        self._attorney_gender_combo = QComboBox()
        self._attorney_gender_combo.addItems(["M", "F"])
        self._gender_combo = QComboBox()
        self._gender_combo.addItems(["M", "F"])
        self._reference_date = QLineEdit()
        self._reference_date.setPlaceholderText("MM/DD/YYYY")
        self._dob = QLineEdit()
        self._dob.setPlaceholderText("MM/DD/YYYY")
        self._doi = QLineEdit()
        self._doi.setPlaceholderText("MM/DD/YYYY")

        form2.addRow(self._trial_date_check, QLabel(""))
        form2.addRow("Attorney Gender:", self._attorney_gender_combo)
        form2.addRow("Claimant Gender:", self._gender_combo)
        form2.addRow("Trial/Reference Date:", self._reference_date)
        form2.addRow("Claimant DOB:", self._dob)
        form2.addRow("Claimant DOI:", self._doi)
        layout.addLayout(form2)

        btn_row = QHBoxLayout()
        btn_row.addItem(
            QSpacerItem(
                40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
            )
        )
        ok_btn = QPushButton("OK")
        ok_btn.setObjectName("dialog_btn")
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("dialog_btn")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(ok_btn)
        btn_row.addWidget(cancel_btn)
        layout.addLayout(btn_row)

    def _prefill(self) -> None:
        case_profile = create_case_profile(self._off_path)
        self._claimant_first.setText(case_profile.claimant_name_first)
        self._claimant_last.setText(case_profile.claimant_name_last)
        self._attorney_first.setText(case_profile.attorney_name_first)
        self._attorney_last.setText(case_profile.attorney_name_last)
        self._attorney_gender_combo.setCurrentText(case_profile.attorney_gender)
        self._gender_combo.setCurrentText(case_profile.claimant_gender)
        self._reference_date.setText(case_profile.trial_date)
        self._dob.setText(case_profile.claimant_dob)
        self._doi.setText(case_profile.claimant_doi)

    def form_data(self) -> dict:
        return {
            "claimant_name_first": self._claimant_first.text().strip(),
            "claimant_name_last": self._claimant_last.text().strip(),
            "attorney_name_first": self._attorney_first.text().strip(),
            "attorney_name_last": self._attorney_last.text().strip(),
            "trial_date_bool": self._trial_date_check.isChecked(),
            "attorney_gender": self._attorney_gender_combo.currentText(),
            "gender": self._gender_combo.currentText(),
            "reference_date": self._reference_date.text().strip(),
            "dob": self._dob.text().strip(),
            "doi": self._doi.text().strip(),
        }


def _read_recent_log() -> str | None:
    try:
        log_dir = _get_log_dir()
        log_files = list(log_dir.glob("econ_automation_*.txt"))
        if not log_files:
            return None

        latest = max(log_files, key=lambda f: f.stat().st_mtime)
        text = latest.read_text(encoding="utf-8", errors="replace")
        entries = [e.strip() for e in text.split("\n\n") if e.strip()]
        snippet = "\n\n".join(entries[-10:])
        if len(snippet) > 3000:
            snippet = "...[truncated]\n\n" + snippet[-3000:]
        return snippet
    except Exception:
        return None


class BugReportDialog(QDialog):
    """'Send Bug Report' — pre-fills a GitHub new-issue URL and opens it in the browser."""

    def __init__(self, parent, colors: dict, error_message: str | None = None):
        super().__init__(parent)
        self.setWindowTitle("Send Bug Report")
        self.setModal(True)
        self.setMinimumWidth(440)
        self._colors = colors
        self._error_message = error_message
        self._log_snippet = _read_recent_log()
        self._build_ui()
        _apply_dialog_style(self, colors)

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 16)
        layout.setSpacing(12)

        title = QLabel("Send Bug Report")
        title.setObjectName("dialog_title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        layout.addWidget(_make_separator())

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form.setHorizontalSpacing(12)
        form.setVerticalSpacing(8)
        self._title_edit = QLineEdit()
        self._title_edit.setText("Bug Report")
        self._title_edit.setPlaceholderText("Brief summary of the issue")
        form.addRow("Title:", self._title_edit)
        layout.addLayout(form)

        desc_label = QLabel("Description:")
        layout.addWidget(desc_label)
        self._desc_edit = QTextEdit()
        self._desc_edit.setPlaceholderText(
            "Describe the issue and steps to reproduce..."
        )
        self._desc_edit.setFixedHeight(100)
        layout.addWidget(self._desc_edit)

        btn_row = QHBoxLayout()
        btn_row.addItem(
            QSpacerItem(
                40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
            )
        )
        submit_btn = QPushButton("Submit")
        submit_btn.setObjectName("dialog_btn")
        submit_btn.clicked.connect(self._on_submit)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("dialog_btn")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(submit_btn)
        btn_row.addWidget(cancel_btn)
        layout.addLayout(btn_row)

    def _on_submit(self) -> None:
        today = dt.now().strftime("%Y-%m-%d")
        title = f"{today} - {self._title_edit.text().strip() or 'Bug Report'}"
        description = self._desc_edit.toPlainText().strip()

        body_parts = [
            "**Description:**",
            description if description else "(no description provided)",
            "",
            "**Environment:**",
            f"- App Version: v{_app_version}",
            f"- OS: {platform.system()} {platform.version()}",
        ]

        if self._error_message:
            body_parts += ["", "**Error Message:**", f"```\n{self._error_message}\n```"]

        if self._log_snippet:
            body_parts += [
                "",
                "**Recent Log Entries:**",
                f"```\n{self._log_snippet}\n```",
            ]

        body = "\n".join(body_parts)
        params = urllib.parse.urlencode({"title": title, "body": body, "labels": "bug"})
        url = f"https://github.com/ebusseyst/EconAutomation-REP/issues/new?{params}"
        QDesktopServices.openUrl(QUrl(url))
        self.accept()
