from PySide6.QtWidgets import QFileDialog
from pathlib import Path


def select_file_modal(self, title: str, filters: str) -> str:
    """Opens a modal file selection dialog."""
    filename, _ = QFileDialog.getOpenFileName(
        self,
        caption=title,
        dir=str(self.econ_cases_path),
        filter=filters,
    )

    if filename:
        return str(Path(filename).resolve())
    return ""
