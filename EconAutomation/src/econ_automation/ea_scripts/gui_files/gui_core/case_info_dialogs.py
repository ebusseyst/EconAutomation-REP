from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette
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
    QVBoxLayout,
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

        form.addRow("Claimant First Name:", self._claimant_first)
        form.addRow("Claimant Last Name:", self._claimant_last)
        form.addRow("Attorney First Name:", self._attorney_first)
        form.addRow("Attorney Last Name:", self._attorney_last)
        layout.addLayout(form)

        btn_row = QHBoxLayout()
        btn_row.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
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
        }


class ConfirmCaseInfoDialog(QDialog):
    """'Confirm Case Information' — pre-fills from cache, collects additional fields for no-OFF workbook setup."""

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
        btn_row.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
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
