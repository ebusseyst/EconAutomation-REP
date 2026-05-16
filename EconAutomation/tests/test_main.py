import logging
import logging.config
import sys
from PySide6.QtWidgets import QApplication

from PySide6.QtGui import QFontDatabase, QFont

from econ_automation.ea_scripts.gui_files.gui_core import ea_fontset1

# Setting up same logging config as main
logging.basicConfig(level=logging.INFO)

# Top-level test logger instance
logger = logging.getLogger(__name__)


# TEST CONSTANTS
CURRENT_VERSION = "0.0.1"
VERSION_URL = "https://github.com/ebusseyst/EconAutomation-REP/releases/tag/Test"
REQUEST_TIMEOUT = 5

# Create a QApplication instance
app = QApplication(sys.argv)

# 1. Load the font file
font_path_dict = {
    "DM Sans Regular": ":/fonts/DMSans-Regular-VariableFont.ttf",
    "DM Sans Italic": ":/fonts/DMSans-Italic-VariableFont.ttf",
    "Figtree Regular": ":/fonts/Figtree-Regular-VariableFont.ttf",
    "Figtree Italic": ":/fonts/Figtree-Italic-VariableFont.ttf",
    "IBM Plex Mono Regular": ":/fonts/IBMPlexMono-Regular.ttf",
    "IBM Plex Mono Italic": ":/fonts/IBMPlexMono-Italic.ttf",
}
font_dict = {}

for font_name, font_path in font_path_dict.items():
    font_id = QFontDatabase.addApplicationFont(font_path)
    font_dict[font_name] = font_id
    print(f"Font {font_name} loaded with ID {font_id}")

# for font_name, font_id in font_dict.items():
#     if font_id != -1:
#         font_families = QFontDatabase.applicationFontFamilies(font_id)
#         # DEBUGGING
#         logger.info("=================================================")
#         logger.info("Font Name: ", font_name)
#         logger.info("Font ID: ", font_id)
#         logger.info("Font Families: ", font_families)
#         logger.info("=================================================")
#         if font_families:
#             custom_font_family = font_families[0]
#             logger.info(custom_font_family)

# if __name__ == "__main__":
#     test_fetch_remote_version()


# TEST autoupdate function
# def test_update_check():
#     """
#     Tests possible Github update check
#     """
