# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'econ_automation_ui.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
from PySide6.QtWidgets import QSpacerItem
from pathlib import Path
import logging

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)
from econ_automation.ea_scripts.gui_files.gui_core import ea_fontset1
from econ_automation.ea_scripts.gui_files.gui_core import ea_iconset1

# Module's logger instance
logger = logging.getLogger(__name__)

# Get the folder where this script lives
basedir = Path(__file__).resolve().parent.parent

# Full path to the icon dir
icon_dir = str(basedir / "icons")

# Get absolute path to icon files
icon_dict = {}

for icon in Path(icon_dir).iterdir():
    if icon.suffix == ".png" or icon.suffix == ".svg":
        icon_name = icon.stem
        icon_path = icon
        icon_dict[icon_name] = str(icon_path)


class Ui_ea_MainWindow(object):
    def __init__(self, ea_MainWindow):
        self.ea_MainWindow = ea_MainWindow

    def setupUi(self):
        if not self.ea_MainWindow.objectName():
            self.ea_MainWindow.setObjectName("ea_MainWindow")

        horizontal_spacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )
        vertical_spacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        # 1. Load the font file
        font_path_dict = {
            "DM Sans": ":/fonts/DMSans-Regular-VariableFont.ttf",
            "DM Sans Italic": ":/fonts/DMSans-Italic-VariableFont.ttf",
            "Figtree": ":/fonts/Figtree-Regular-VariableFont.ttf",
            "Figtree Italic": ":/fonts/Figtree-Italic-VariableFont.ttf",
            "IBM Plex Mono Regular": ":/fonts/IBMPlexMono-Regular.ttf",
            "IBM Plex Mono Italic": ":/fonts/IBMPlexMono-Italic.ttf",
        }
        font_dict = {}

        for font_name, font_path in font_path_dict.items():
            font_id = QFontDatabase.addApplicationFont(font_path)
            font_dict[font_name] = font_id
            print(f"{font_name} loaded with id: {font_id}")

        color_dict = {
            "off_white": "#ECECEC",
            "dark_navy": "#011F5B",
            "light_blue": "#ADD8E6",
            "dark_light_blue": "#7EB8CB",
            "gold": "#AD9915",
            "light_gold": "#D0BC34",
            "dark_gold": "#8D7B00",
            "gold_border": "rgba(141,123,0,0.4)",
        }

        # Predefined stylesheets for specific widgets
        ea_CentralWidget_style = """
                                #ea_CentralWidget_frame {{
                                    border: none;
                                    border-radius: 0px;
                                    background-color: {dark_navy};
                                }}
                                """.format(
            **{key: value for key, value in color_dict.items()}
        )

        ea_subframe_style = """
                                QFrame {{
                                    border: 0px;
                                    border-radius: 10px;
                                    background-color: {gold};
                                    font-family: Figtree;
                                    font-size: 15pt;
                                    font-weight: 500;
                                    color: {dark_navy};
                                }}
                                QLabel {{
                                    background-color: {light_gold};
                                    border: 2px solid {gold_border};
                                    border-radius: 4px;
                                    font-family: DM Sans;
                                    font-size: 15pt;
                                    font-weight: 500;
                                    color: {dark_navy};
                                }}
                                QPushButton {{
                                    border: 1px solid {dark_navy};
                                    border-radius: 4px;
                                    background-color: white;
                                    font-family: Figtree;
                                    font-size: 12pt;
                                    font-weight: 500;
                                    color: {dark_navy};
                                }}
                                QPushButton:hover {{
                                    background-color: {off_white};
                                }}
                                
                                #ea_CentralWidget_label_frame {{
                                    border: 2px solid {gold_border};
                                }}
                                #ea_CentralWidget_label {{
                                    background-color: {light_gold};
                                    border: 2px solid {gold_border};
                                    border-radius: 4px;
                                    font-family: DM Sans;
                                    font-size: 18pt;
                                    font-weight: 800;
                                    font-style: italic;
                                    color: {dark_navy};
                                }}
                                
                                #ea_setupcase_frame {{
                                    border: 2px solid {gold_border};
                                    background-color: {gold};
                                    font-family: Figtree;
                                    font-size: 13pt;
                                    font-weight: 400;
                                    color: {dark_navy};
                                }}
                                #ea_setupcase_frame #ea_setupcase_label {{
                                    font-family: DM Sans;
                                    font-size: 13pt;
                                    font-weight: 600;
                                    padding: 3px;
                                }}
                                #ea_setupcase_frame #ea_setupcase_createcase_button {{
                                    font-family: Figtree;
                                    font-size: 10pt;
                                    font-weight: 400;
                                    color: {dark_navy};
                                    padding: 3px;
                                }}

                                #ea_setupcase_sub2frame {{
                                    border: 0px;
                                    background-color: transparent;
                                    font-family: Figtree;
                                    font-size: 11pt;
                                    font-weight: 400;
                                    color: {dark_navy};
                                }}
                                #ea_setupcase_sub2frame QFrame {{
                                    border: 0px;
                                    background-color: transparent;
                                    font-family: Figtree;
                                    font-size: 13pt;
                                    font-weight: 400;
                                    color: {dark_navy};
                                }}
                                #ea_setupcase_sub2frame QLabel {{
                                    background-color: transparent;
                                    border: 0px;
                                    font-family: Figtree;
                                    font-size: 11pt;
                                    font-weight: 400;
                                    color: {dark_navy};
                                }}
                                #ea_setupcase_sub2frame #ea_setupcase_selectedOFF_label {{
                                    background-color: white;
                                    border: 1px solid {dark_navy};
                                    border-radius: 4px;
                                    font-family: Figtree;
                                    font-size: 10pt;
                                    font-weight: 300;
                                    color: {dark_navy};
                                }}
                                
                                #ea_reportmerge_frame {{
                                    border: 2px solid {gold_border};
                                    background-color: {gold};
                                    font-family: Figtree;
                                    font-size: 13pt;
                                    font-weight: 500;
                                    color: {dark_navy};
                                }}
                                #ea_reportmerge_label_frame {{
                                    border: 2px solid {gold_border};
                                    background-color: {light_gold};
                                }}
                                #ea_reportmerge_label {{
                                    font-family: DM Sans;
                                    font-size: 13pt;
                                    font-weight: 600;
                                    padding: 3px;
                                }}
                                #ea_reportmerge_sub2frame {{
                                    border: 2px solid {gold_border};
                                    background-color: {light_gold};
                                    font-family: Figtree;
                                    font-size: 11pt;
                                    font-weight: 400;
                                    color: {dark_navy};
                                }}
                                #ea_reportmerge_sub2frame QFrame {{
                                    background-color: transparent;
                                    border: 0px;
                                }}
                                #ea_reportmerge_sub2frame QLabel {{
                                    background-color: transparent;
                                    border: 0px;
                                    font-family: Figtree;
                                    font-size: 10pt;
                                    font-weight: 400;
                                    color: {dark_navy};
                                }}
                                #ea_reportmerge_sub2frame QCheckBox::indicator {{
                                    width: 14px;
                                    height: 14px;
                                    background-color: white;
                                    border: 1px solid {dark_navy};
                                    border-radius: 4px;
                                    color: {dark_navy};
                                }}
                                #ea_reportmerge_sub2frame QCheckBox::indicator:unchecked {{
                                    background-color: white;
                                }}
                                #ea_reportmerge_sub2frame QCheckBox::indicator:disabled {{
                                    background-color: lightgray;
                                }}
                                #ea_reportmerge_sub2frame QCheckBox::indicator:checked {{
                                    background-color: white;
                                    image: url(src/econ_automation/ea_scripts/gui_files/icons/checkmark_icon.png);
                                }}
                                #ea_reportmerge_sub2frame QComboBox {{
                                    background-color: white;
                                    border: 1px solid {dark_navy};
                                    border-radius: 4px;
                                    color: {dark_navy};
                                }}
                                #ea_reportmerge_sub2frame QComboBox::drop-down {{
                                    subcontrol-origin: padding;
                                    subcontrol-position: center right;
                                    background-color: transparent;
                                }}
                                #ea_reportmerge_sub2frame QComboBox::down-arrow {{
                                    background-color: transparent;
                                    image: url(src/econ_automation/ea_scripts/gui_files/icons/dropdown_arrow_icon.png);
                                }}
                                #ea_reportmerge_sub2frame QComboBox QAbstractItemView {{
                                    border: 1px solid {dark_navy};
                                    selection-background-color: {light_blue};
                                    background-color: white;
                                    color: {dark_navy};
                                }}
                                """.format(
            **{key: value for key, value in color_dict.items()}
        )

        self.ea_MainWindow.resize(550, 600)
        self.ea_MainWindow.setWindowIcon(QIcon(icon_dict["starfire_icon"]))
        self.ea_MainWindow.setWindowTitle("StarFire")
        self.ea_CentralWidget = QWidget(self.ea_MainWindow)
        self.ea_CentralWidget.setStyleSheet(ea_CentralWidget_style)
        self.ea_CentralWidget.setObjectName("ea_CentralWidget")
        self.ea_CentralWidget_GLayout = QGridLayout(self.ea_CentralWidget)
        self.ea_CentralWidget_GLayout.setObjectName("ea_CentralWidget_GLayout")
        self.ea_CentralWidget_GLayout.setContentsMargins(0, 0, 0, 0)
        self.ea_CentralWidget_frame = QFrame(self.ea_CentralWidget)
        self.ea_CentralWidget_frame.setObjectName("ea_CentralWidget_frame")
        self.ea_CentralWidget_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.ea_CentralWidget_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.ea_CentralWidgetframe_GLayout = QGridLayout(self.ea_CentralWidget_frame)
        self.ea_CentralWidgetframe_GLayout.setObjectName("ea_CentralWidget_GLayout")
        self.ea_CentralWidgetframe_GLayout.setHorizontalSpacing(5)
        self.ea_CentralWidgetframe_GLayout.setVerticalSpacing(5)
        self.ea_CentralWidgetframe_GLayout.setContentsMargins(8, 8, 8, 8)
        self.ea_CentralWidgetframe_GLayout.setColumnStretch(0, 1)
        self.ea_CentralWidgetframe_GLayout.setColumnStretch(1, 0)
        self.ea_CentralWidgetframe_GLayout.setColumnStretch(2, 3)
        self.ea_setupcase_frame = QFrame(self.ea_CentralWidget_frame)
        self.ea_setupcase_frame.setObjectName("ea_setupcase_frame")
        self.ea_setupcase_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.ea_setupcase_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.ea_setupcase_frame.setStyleSheet(ea_subframe_style)
        self.ea_setupfile_GLayout = QGridLayout(self.ea_setupcase_frame)
        self.ea_setupfile_GLayout.setObjectName("ea_setupfile_GLayout")
        self.ea_setupfile_GLayout.setHorizontalSpacing(5)
        self.ea_setupfile_GLayout.setVerticalSpacing(0)
        self.ea_setupcase_label = QLabel(self.ea_setupcase_frame)
        self.ea_setupcase_label.setObjectName("ea_setupcase_label")
        self.ea_setupcase_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.ea_setupfile_GLayout.addWidget(self.ea_setupcase_label, 0, 0, 1, 3)

        self.ea_setupcase_sub2frame = QFrame(self.ea_setupcase_frame)
        self.ea_setupcase_sub2frame.setObjectName("ea_setupcase_sub2frame")
        self.ea_setupcase_sub2frame.setFrameShape(QFrame.Shape.NoFrame)
        self.ea_setupcase_sub2frame.setFrameShadow(QFrame.Shadow.Raised)
        self.ea_setupfile_sub2frame_GLayout = QGridLayout(self.ea_setupcase_sub2frame)
        self.ea_setupfile_sub2frame_GLayout.setObjectName(
            "ea_setupfile_sub2frame_GLayout"
        )
        self.ea_setupcase_OFFSelect_button = QPushButton(self.ea_setupcase_sub2frame)
        self.ea_setupcase_OFFSelect_button.setObjectName(
            "ea_setupcase_OFFSelect_button"
        )
        self.ea_setupcase_OFFSelect_button.setIcon(QIcon(icon_dict["add_note_icon"]))

        self.ea_setupfile_sub2frame_GLayout.addWidget(
            self.ea_setupcase_OFFSelect_button, 0, 3, 1, 1
        )

        self.ea_setupcase_selectedOFF_label = QLabel(self.ea_setupcase_sub2frame)
        self.ea_setupcase_selectedOFF_label.setObjectName(
            "ea_setupcase_selectedOFF_label"
        )
        self.ea_setupcase_selectedOFF_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.ea_setupfile_sub2frame_GLayout.addWidget(
            self.ea_setupcase_selectedOFF_label, 0, 0, 1, 2
        )

        self.ea_setupfile_GLayout.addWidget(self.ea_setupcase_sub2frame, 1, 0, 1, 3)

        self.ea_setupcase_createcase_button = QPushButton(self.ea_setupcase_frame)
        self.ea_setupcase_createcase_button.setObjectName(
            "ea_setupcase_createcase_button"
        )
        self.ea_setupfile_GLayout.addItem(horizontal_spacer, 2, 0, 1, 1)
        self.ea_setupfile_GLayout.addWidget(
            self.ea_setupcase_createcase_button, 2, 1, 1, 1
        )
        self.ea_setupfile_GLayout.addItem(horizontal_spacer, 2, 2, 1, 1)

        self.ea_setupfile_GLayout.setRowStretch(0, 1)
        self.ea_setupfile_GLayout.setRowStretch(1, 10)

        self.ea_CentralWidgetframe_GLayout.addWidget(
            self.ea_setupcase_frame, 1, 0, 1, 3
        )

        self.ea_reportmerge_frame = QFrame(self.ea_CentralWidget_frame)
        self.ea_reportmerge_frame.setObjectName("ea_reportmerge_frame")
        self.ea_reportmerge_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.ea_reportmerge_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.ea_reportmerge_frame.setStyleSheet(ea_subframe_style)
        self.ea_reportmerge_GLayout = QGridLayout(self.ea_reportmerge_frame)
        self.ea_reportmerge_GLayout.setObjectName("ea_reportmerge_GLayout")
        self.ea_reportmerge_GLayout.setHorizontalSpacing(0)
        self.ea_reportmerge_GLayout.setVerticalSpacing(5)
        self.ea_reportmerge_sub2frame = QFrame(self.ea_reportmerge_frame)
        self.ea_reportmerge_sub2frame.setObjectName("ea_reportmerge_sub2frame")
        self.ea_reportmerge_sub2frame.setFrameShape(QFrame.Shape.NoFrame)
        self.ea_reportmerge_sub2frame.setFrameShadow(QFrame.Shadow.Raised)
        self.ea_reportmerge_sub2frame_GLayout = QGridLayout(
            self.ea_reportmerge_sub2frame
        )
        self.ea_reportmerge_sub2frame_GLayout.setHorizontalSpacing(3)
        self.ea_reportmerge_sub2frame_GLayout.setObjectName(
            "ea_reportmerge_sub2frame_GLayout"
        )
        self.ea_reportmerge_sub2frame_GLayout.setColumnStretch(0, 2)
        self.ea_reportmerge_sub2frame_GLayout.setColumnStretch(1, 2)
        self.frame_4 = QFrame(self.ea_reportmerge_sub2frame)
        self.frame_4.setObjectName("frame_4")
        self.frame_4.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_4)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_4.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )
        self.label_4 = QLabel(self.frame_4)
        self.label_4.setObjectName("label_4")

        self.gridLayout_4.addWidget(self.label_4, 0, 0, 1, 1)

        self.checkBox_4 = QCheckBox(self.frame_4)
        self.checkBox_4.setObjectName("checkBox_4")

        self.gridLayout_4.addWidget(self.checkBox_4, 1, 0, 1, 1)

        self.ea_reportmerge_sub2frame_GLayout.addWidget(self.frame_4, 1, 1, 1, 1)

        self.ea_reportmerge_referencetype_sub3frame = QFrame(
            self.ea_reportmerge_sub2frame
        )
        self.ea_reportmerge_referencetype_sub3frame.setObjectName(
            "ea_reportmerge_referencetype_sub3frame"
        )
        self.ea_reportmerge_referencetype_sub3frame.setFrameShape(QFrame.Shape.NoFrame)
        self.ea_reportmerge_referencetype_sub3frame.setFrameShadow(QFrame.Shadow.Raised)
        self.ea_reportmerge_referencetype_GLayout = QGridLayout(
            self.ea_reportmerge_referencetype_sub3frame
        )
        self.ea_reportmerge_referencetype_GLayout.setObjectName(
            "ea_reportmerge_referencetype_GLayout"
        )
        self.ea_reportmerge_referencetype_label = QLabel(
            self.ea_reportmerge_referencetype_sub3frame
        )
        self.ea_reportmerge_referencetype_label.setObjectName(
            "ea_reportmerge_referencetype_label"
        )

        self.ea_reportmerge_referencetype_GLayout.addWidget(
            self.ea_reportmerge_referencetype_label, 0, 0, 1, 1
        )
        self.ea_reportmerge_referencetype_GLayout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )

        self.ea_reportmerge_referencetype_combobox = QComboBox(
            self.ea_reportmerge_referencetype_sub3frame
        )
        self.ea_reportmerge_referencetype_combobox.setObjectName(
            "ea_reportmerge_referencetype_combobox"
        )

        self.ea_reportmerge_referencetype_GLayout.addWidget(
            self.ea_reportmerge_referencetype_combobox, 1, 0, 1, 1
        )

        self.ea_reportmerge_sub2frame_GLayout.addWidget(
            self.ea_reportmerge_referencetype_sub3frame, 1, 0, 1, 1
        )

        self.frame_6 = QFrame(self.ea_reportmerge_sub2frame)
        self.frame_6.setObjectName("frame_6")
        self.frame_6.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_6)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.gridLayout_6.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )
        self.checkBox_6 = QCheckBox(self.frame_6)
        self.checkBox_6.setObjectName("checkBox_6")

        self.gridLayout_6.addWidget(self.checkBox_6, 1, 0, 1, 1)

        self.label_6 = QLabel(self.frame_6)
        self.label_6.setObjectName("label_6")

        self.gridLayout_6.addWidget(self.label_6, 0, 0, 1, 1)

        self.ea_reportmerge_sub2frame_GLayout.addWidget(self.frame_6, 2, 1, 1, 1)

        self.ea_reportmerge_bases_sub3frame = QFrame(self.ea_reportmerge_sub2frame)
        self.ea_reportmerge_bases_sub3frame.setObjectName(
            "ea_reportmerge_bases_sub3frame"
        )
        self.ea_reportmerge_bases_sub3frame.setFrameShape(QFrame.Shape.NoFrame)
        self.ea_reportmerge_bases_sub3frame.setFrameShadow(QFrame.Shadow.Raised)
        self.ea_reportmerge_bases_GLayout = QGridLayout(
            self.ea_reportmerge_bases_sub3frame
        )
        self.ea_reportmerge_bases_GLayout.setSpacing(8)
        self.ea_reportmerge_bases_GLayout.setObjectName("ea_reportmerge_bases_GLayout")
        self.ea_reportmerge_bases_GLayout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )
        self.ea_reportmerge_credit2_checkbox = QCheckBox(self.ea_reportmerge_bases_sub3frame)
        self.ea_reportmerge_credit2_checkbox.setObjectName("checkBox_9")

        self.ea_reportmerge_bases_GLayout.addWidget(self.ea_reportmerge_credit2_checkbox, 2, 1, 1, 1)

        self.ea_reportmerge_base1_checkbox = QCheckBox(
            self.ea_reportmerge_bases_sub3frame
        )
        self.ea_reportmerge_base1_checkbox.setObjectName(
            "ea_reportmerge_base1_checkbox"
        )

        self.ea_reportmerge_bases_GLayout.addWidget(
            self.ea_reportmerge_base1_checkbox, 1, 0, 1, 1
        )

        self.ea_reportmerge_credit3_checkbox = QCheckBox(self.ea_reportmerge_bases_sub3frame)
        self.ea_reportmerge_credit3_checkbox.setObjectName("checkBox_10")

        self.ea_reportmerge_bases_GLayout.addWidget(self.ea_reportmerge_credit3_checkbox, 3, 1, 1, 1)

        self.ea_reportmerge_bases_label = QLabel(self.ea_reportmerge_bases_sub3frame)
        self.ea_reportmerge_bases_label.setObjectName("ea_reportmerge_bases_label")

        self.ea_reportmerge_bases_GLayout.addWidget(
            self.ea_reportmerge_bases_label, 0, 0, 1, 1
        )

        self.ea_reportmerge_base2_checkbox = QCheckBox(self.ea_reportmerge_bases_sub3frame)
        self.ea_reportmerge_base2_checkbox.setObjectName("checkBox")

        self.ea_reportmerge_bases_GLayout.addWidget(self.ea_reportmerge_base2_checkbox, 2, 0, 1, 1)

        self.ea_reportmerge_base3_checkbox = QCheckBox(self.ea_reportmerge_bases_sub3frame)
        self.ea_reportmerge_base3_checkbox.setObjectName("checkBox_2")

        self.ea_reportmerge_bases_GLayout.addWidget(self.ea_reportmerge_base3_checkbox, 3, 0, 1, 1)

        self.ea_reportmerge_credit1_checkbox = QCheckBox(self.ea_reportmerge_bases_sub3frame)
        self.ea_reportmerge_credit1_checkbox.setObjectName("checkBox_3")

        self.ea_reportmerge_bases_GLayout.addWidget(self.ea_reportmerge_credit1_checkbox, 1, 1, 1, 1)

        self.ea_reportmerge_meals_checkbox = QCheckBox(self.ea_reportmerge_bases_sub3frame)
        self.ea_reportmerge_meals_checkbox.setObjectName("checkBox_11")

        self.ea_reportmerge_bases_GLayout.addWidget(self.ea_reportmerge_meals_checkbox, 4, 0, 1, 1)

        self.checkBox_12 = QCheckBox(self.ea_reportmerge_bases_sub3frame)
        self.checkBox_12.setObjectName("checkBox_12")

        self.ea_reportmerge_bases_GLayout.addWidget(self.checkBox_12, 4, 1, 1, 1)

        self.ea_reportmerge_sub2frame_GLayout.addWidget(
            self.ea_reportmerge_bases_sub3frame, 2, 0, 1, 1
        )

        self.ea_reportmerge_reporttypes_sub3frame = QFrame(
            self.ea_reportmerge_sub2frame
        )
        self.ea_reportmerge_reporttypes_sub3frame.setObjectName(
            "ea_reportmerge_reporttypes_sub3frame"
        )
        self.ea_reportmerge_reporttypes_sub3frame.setFrameShape(QFrame.Shape.NoFrame)
        self.ea_reportmerge_reporttypes_sub3frame.setFrameShadow(QFrame.Shadow.Raised)
        self.ea_reportmerge_reporttypes_GLayout = QGridLayout(
            self.ea_reportmerge_reporttypes_sub3frame
        )
        self.ea_reportmerge_reporttypes_GLayout.setObjectName(
            "ea_reportmerge_reporttypes_GLayout"
        )
        self.ea_reportmerge_reporttypes_GLayout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )
        self.ea_reportmerge_reporttypes_PVLCP_checkbox = QCheckBox(
            self.ea_reportmerge_reporttypes_sub3frame
        )
        self.ea_reportmerge_reporttypes_PVLCP_checkbox.setObjectName(
            "ea_reportmerge_reporttypes_PVLCP_checkbox"
        )

        self.ea_reportmerge_reporttypes_GLayout.addWidget(
            self.ea_reportmerge_reporttypes_PVLCP_checkbox, 1, 0, 1, 1
        )

        self.ea_reportmerge_reporttypes_label = QLabel(self.ea_reportmerge_reporttypes_sub3frame)
        self.ea_reportmerge_reporttypes_label.setObjectName("label_2")

        self.ea_reportmerge_reporttypes_GLayout.addWidget(self.ea_reportmerge_reporttypes_label, 0, 0, 1, 1)

        self.ea_reportmerge_reporttypes_PVearnings_checkbox = QCheckBox(
            self.ea_reportmerge_reporttypes_sub3frame
        )
        self.ea_reportmerge_reporttypes_PVearnings_checkbox.setObjectName(
            "ea_reportmerge_reporttypes_PVearnings_checkbox"
        )

        self.ea_reportmerge_reporttypes_GLayout.addWidget(
            self.ea_reportmerge_reporttypes_PVearnings_checkbox, 2, 0, 1, 1
        )

        self.ea_reportmerge_sub2frame_GLayout.addWidget(
            self.ea_reportmerge_reporttypes_sub3frame, 0, 1, 1, 1
        )

        self.ea_reportmerge_taxstatus_sub3frame = QFrame(self.ea_reportmerge_sub2frame)
        self.ea_reportmerge_taxstatus_sub3frame.setObjectName(
            "ea_reportmerge_taxstatus_sub3frame"
        )
        self.ea_reportmerge_taxstatus_sub3frame.setFrameShape(QFrame.Shape.NoFrame)
        self.ea_reportmerge_taxstatus_sub3frame.setFrameShadow(QFrame.Shadow.Raised)
        self.ea_reportmerge_taxstatus_GLayout = QGridLayout(
            self.ea_reportmerge_taxstatus_sub3frame
        )
        self.ea_reportmerge_taxstatus_GLayout.setObjectName(
            "ea_reportmerge_taxstatus_GLayout"
        )
        self.ea_reportmerge_taxstatus_GLayout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )
        self.ea_reportmerge_taxstatus_checkbox = QCheckBox(
            self.ea_reportmerge_taxstatus_sub3frame
        )
        self.ea_reportmerge_taxstatus_checkbox.setObjectName(
            "ea_reportmerge_taxstatus_checkbox"
        )

        self.ea_reportmerge_taxstatus_GLayout.addWidget(
            self.ea_reportmerge_taxstatus_checkbox, 1, 0, 1, 1
        )

        self.ea_reportmerge_taxstatus_label = QLabel(
            self.ea_reportmerge_taxstatus_sub3frame
        )
        self.ea_reportmerge_taxstatus_label.setObjectName(
            "ea_reportmerge_taxstatus_label"
        )

        self.ea_reportmerge_taxstatus_GLayout.addWidget(
            self.ea_reportmerge_taxstatus_label, 0, 0, 1, 1
        )

        self.ea_reportmerge_sub2frame_GLayout.addWidget(
            self.ea_reportmerge_taxstatus_sub3frame, 3, 0, 1, 1
        )

        self.ea_reportmerge_projectiontype_sub3frame = QFrame(
            self.ea_reportmerge_sub2frame
        )
        self.ea_reportmerge_projectiontype_sub3frame.setObjectName(
            "ea_reportmerge_projectiontype_sub3frame"
        )
        self.ea_reportmerge_projectiontype_sub3frame.setFrameShape(QFrame.Shape.NoFrame)
        self.ea_reportmerge_projectiontype_sub3frame.setFrameShadow(
            QFrame.Shadow.Raised
        )
        self.ea_reportmerge_projectiontype_GLayout = QGridLayout(
            self.ea_reportmerge_projectiontype_sub3frame
        )
        self.ea_reportmerge_projectiontype_GLayout.setObjectName(
            "ea_reportmerge_projectiontype_GLayout"
        )
        self.ea_reportmerge_projectiontype_label = QLabel(
            self.ea_reportmerge_projectiontype_sub3frame
        )
        self.ea_reportmerge_projectiontype_label.setObjectName(
            "ea_reportmerge_projectiontype_label"
        )
        self.ea_reportmerge_projectiontype_GLayout.addWidget(
            self.ea_reportmerge_projectiontype_label, 0, 0, 1, 1
        )

        self.ea_reportmerge_projectiontype_combobox = QComboBox(
            self.ea_reportmerge_projectiontype_sub3frame
        )
        self.ea_reportmerge_projectiontype_combobox.setObjectName(
            "ea_reportmerge_projectiontype_combobox"
        )

        self.ea_reportmerge_projectiontype_GLayout.addWidget(
            self.ea_reportmerge_projectiontype_combobox, 1, 0, 1, 1
        )
        self.ea_reportmerge_projectiontype_GLayout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )

        self.ea_reportmerge_sub2frame_GLayout.addWidget(
            self.ea_reportmerge_projectiontype_sub3frame, 0, 0, 1, 1
        )

        self.frame_8 = QFrame(self.ea_reportmerge_sub2frame)
        self.frame_8.setObjectName("frame_8")
        self.frame_8.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_8 = QGridLayout(self.frame_8)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.checkBox_8 = QCheckBox(self.frame_8)
        self.checkBox_8.setObjectName("checkBox_8")
        self.checkBox_8.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self.gridLayout_8.addWidget(self.checkBox_8, 1, 0, 1, 1)

        self.label_8 = QLabel(self.frame_8)
        self.label_8.setObjectName("label_8")

        self.gridLayout_8.addWidget(self.label_8, 0, 0, 1, 1)

        self.ea_reportmerge_sub2frame_GLayout.addWidget(self.frame_8, 3, 1, 1, 1)

        self.ea_reportmerge_GLayout.addWidget(self.ea_reportmerge_sub2frame, 1, 0, 1, 1)

        self.ea_reportmerge_label = QLabel(self.ea_reportmerge_frame)
        self.ea_reportmerge_label.setObjectName("ea_reportmerge_label")
        self.ea_reportmerge_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.ea_reportmerge_GLayout.addWidget(self.ea_reportmerge_label, 0, 0, 1, 1)

        self.ea_reportmerge_button = QPushButton(self.ea_reportmerge_frame)
        self.ea_reportmerge_button.setObjectName("ea_reportmerge_button")

        self.ea_reportmerge_GLayout.addWidget(self.ea_reportmerge_button, 2, 0, 1, 1)

        self.ea_reportmerge_GLayout.setRowStretch(0, 1)
        self.ea_reportmerge_GLayout.setRowStretch(1, 10)

        self.ea_CentralWidgetframe_GLayout.addWidget(
            self.ea_reportmerge_frame, 2, 0, 1, 3
        )

        self.ea_CentralWidget_label_frame = QFrame(self.ea_CentralWidget_frame)
        self.ea_CentralWidget_label_frame.setObjectName("ea_CentralWidget_label_frame")
        self.ea_CentralWidget_label_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.ea_CentralWidget_label_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.ea_CentralWidget_label_frame.setStyleSheet(ea_subframe_style)
        self.ea_CentralWidget_label_VLayout = QVBoxLayout(
            self.ea_CentralWidget_label_frame
        )
        self.ea_CentralWidget_label_VLayout.setSpacing(0)
        self.ea_CentralWidget_label_VLayout.setObjectName(
            "ea_CentralWidget_label_VLayout"
        )
        self.ea_CentralWidget_label_VLayout.setContentsMargins(3, 3, 3, 3)
        self.ea_CentralWidget_label = QLabel(self.ea_CentralWidget_label_frame)
        self.ea_CentralWidget_label.setObjectName("ea_CentralWidget_label")
        self.ea_CentralWidget_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.ea_CentralWidget_label_VLayout.addWidget(self.ea_CentralWidget_label)

        self.ea_CentralWidgetframe_GLayout.addWidget(
            self.ea_CentralWidget_label_frame, 0, 0, 1, 3
        )

        self.ea_CentralWidgetframe_GLayout.setColumnStretch(0, 1)

        self.ea_CentralWidget_GLayout.addWidget(self.ea_CentralWidget_frame)

        self.ea_MainWindow.setCentralWidget(self.ea_CentralWidget)

        self.retranslateUi()

        QMetaObject.connectSlotsByName(self.ea_MainWindow)

    # setupUi

    def retranslateUi(self):
        self.ea_MainWindow.setWindowTitle(
            QCoreApplication.translate("ea_MainWindow", "StarFire", None)
        )
        self.ea_setupcase_label.setText(
            QCoreApplication.translate("ea_MainWindow", "New Case Set Up", None)
        )
        self.ea_setupcase_OFFSelect_button.setText(
            QCoreApplication.translate("ea_MainWindow", "", None)
        )
        self.ea_setupcase_selectedOFF_label.setText(
            QCoreApplication.translate("ea_MainWindow", "No OFF selected", None)
        )
        self.ea_setupcase_createcase_button.setText(
            QCoreApplication.translate("ea_MainWindow", "Create New Case", None)
        )
        self.label_4.setText(
            QCoreApplication.translate("ea_MainWindow", "Placeholder", None)
        )
        self.checkBox_4.setText(
            QCoreApplication.translate("ea_MainWindow", "Placeholder", None)
        )
        self.ea_reportmerge_referencetype_label.setText(
            QCoreApplication.translate("ea_MainWindow", "Reference Type:", None)
        )
        self.checkBox_6.setText(
            QCoreApplication.translate("ea_MainWindow", "Placeholder", None)
        )
        self.label_6.setText(
            QCoreApplication.translate("ea_MainWindow", "Placeholder", None)
        )
        self.ea_reportmerge_credit2_checkbox.setText(
            QCoreApplication.translate("ea_MainWindow", "Credit 2", None)
        )
        self.ea_reportmerge_base1_checkbox.setText(
            QCoreApplication.translate("ea_MainWindow", "Base 1", None)
        )
        self.ea_reportmerge_credit3_checkbox.setText(
            QCoreApplication.translate("ea_MainWindow", "Credit 3", None)
        )
        self.ea_reportmerge_bases_label.setText(
            QCoreApplication.translate(
                "ea_MainWindow", "Relevant Base(s) & Credits:", None
            )
        )
        self.ea_reportmerge_base2_checkbox.setText(
            QCoreApplication.translate("ea_MainWindow", "Base 2", None)
        )
        self.ea_reportmerge_base3_checkbox.setText(
            QCoreApplication.translate("ea_MainWindow", "Base 3", None)
        )
        self.ea_reportmerge_credit1_checkbox.setText(
            QCoreApplication.translate("ea_MainWindow", "Credit 1", None)
        )
        self.ea_reportmerge_meals_checkbox.setText(
            QCoreApplication.translate("ea_MainWindow", "Meals", None)
        )
        self.checkBox_12.setText(
            QCoreApplication.translate("ea_MainWindow", "Placeholder", None)
        )
        self.ea_reportmerge_reporttypes_PVLCP_checkbox.setText(
            QCoreApplication.translate("ea_MainWindow", "PVLCP", None)
        )
        self.ea_reportmerge_reporttypes_label.setText(
            QCoreApplication.translate("ea_MainWindow", "Report Type(s):", None)
        )
        self.ea_reportmerge_reporttypes_PVearnings_checkbox.setText(
            QCoreApplication.translate("ea_MainWindow", "PV Earnings", None)
        )
        self.ea_reportmerge_taxstatus_checkbox.setText(
            QCoreApplication.translate("ea_MainWindow", "Taxed", None)
        )
        self.ea_reportmerge_taxstatus_label.setText(
            QCoreApplication.translate("ea_MainWindow", "Tax Status:", None)
        )
        self.ea_reportmerge_projectiontype_label.setText(
            QCoreApplication.translate("ea_MainWindow", "Earnings Projection:", None)
        )
        self.checkBox_8.setText(
            QCoreApplication.translate("ea_MainWindow", "Placeholder", None)
        )
        self.label_8.setText(
            QCoreApplication.translate("ea_MainWindow", "Placeholder", None)
        )
        self.ea_reportmerge_label.setText(
            QCoreApplication.translate("ea_MainWindow", "Report Merge", None)
        )
        self.ea_reportmerge_button.setText(
            QCoreApplication.translate("ea_MainWindow", "Merge", None)
        )
        self.ea_CentralWidget_label.setText(
            QCoreApplication.translate("ea_MainWindow", "StarFire", None)
        )

    # retranslateUi
