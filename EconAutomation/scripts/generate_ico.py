"""Generate a multi-size .ico from the bolt_boost_icon.svg using PySide6 + Pillow.

Run from the repo root:
    python scripts/generate_ico.py
"""

import io
import sys
from pathlib import Path

from PIL import Image
from PySide6.QtCore import QByteArray
from PySide6.QtGui import QImage, QPainter
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QApplication

SIZES = [16, 32, 48, 256]

REPO_ROOT = Path(__file__).resolve().parent.parent
SVG_PATH = REPO_ROOT / "src/econ_automation/ea_scripts/gui_files/icons/bolt_boost_icon.svg"
ICO_ICONS = REPO_ROOT / "src/econ_automation/ea_scripts/gui_files/icons/bolt_boost_icon.ico"
ICO_INNOSETUP = REPO_ROOT / "innosetup/bolt_boost_icon.ico"


def svg_to_pil(svg_bytes: bytes, size: int) -> Image.Image:
    svg_data = QByteArray(svg_bytes)
    renderer = QSvgRenderer(svg_data)
    image = QImage(size, size, QImage.Format.Format_ARGB32)
    image.fill(0)  # transparent
    painter = QPainter(image)
    renderer.render(painter)
    painter.end()

    # Convert QImage to PIL via raw bytes
    ptr = image.bits()
    buf = bytes(ptr)
    pil = Image.frombytes("RGBA", (size, size), buf, "raw", "BGRA")
    return pil


def main() -> None:
    QApplication.instance() or QApplication(sys.argv)

    svg_bytes = SVG_PATH.read_bytes()
    # Render at maximum size; Pillow downscales to each requested size
    large = svg_to_pil(svg_bytes, max(SIZES))

    buf = io.BytesIO()
    large.save(buf, format="ICO", sizes=[(s, s) for s in SIZES])
    ico_bytes = buf.getvalue()
    ICO_ICONS.write_bytes(ico_bytes)
    ICO_INNOSETUP.write_bytes(ico_bytes)
    print(f"Written {len(SIZES)}-size ICO to {ICO_ICONS} and {ICO_INNOSETUP}")


if __name__ == "__main__":
    main()
