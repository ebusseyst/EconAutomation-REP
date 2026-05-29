# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'econ_automation_ui.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
from __future__ import annotations

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
    QGraphicsDropShadowEffect,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)
from econ_automation.ea_scripts.gui_files.gui_core import ea_fontset1  # noqa: F401
from econ_automation.ea_scripts.gui_files.gui_core import ea_iconset1  # noqa: F401

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
    BASE_HEIGHT = 600

    # Central widget hierarchy
    ea_MainWindow: QMainWindow
    ea_CentralWidget: QWidget
    ea_CentralWidget_GLayout: QGridLayout
    ea_CentralWidget_frame: QFrame
    ea_CentralWidgetframe_GLayout: QGridLayout
    ea_CentralWidget_label_frame: QFrame
    ea_CentralWidget_label_VLayout: QVBoxLayout
    ea_CentralWidget_label: QLabel

    # Setup case section
    ea_setupcase_frame: QFrame
    ea_setupfile_GLayout: QGridLayout
    ea_setupcase_label: QLabel
    ea_setupcase_orgsubframe: QFrame
    ea_setupcase_orgsubframe_GLayout: QGridLayout
    ea_setupcase_sub2frame: QFrame
    ea_setupfile_sub2frame_GLayout: QGridLayout
    ea_setupcase_OFFSelect_button: QPushButton
    ea_setupcase_selectedOFF_label: QLabel
    ea_setupcase_createcase_button: QPushButton

    # Report merge section
    ea_reportmerge_frame: QFrame
    ea_reportmerge_GLayout: QGridLayout
    ea_reportmerge_label: QLabel
    ea_reportmerge_button: QPushButton
    ea_reportmerge_claimantdir_subframe: QFrame
    ea_reportmerge_claimantdir_subframe_GLayout: QGridLayout
    ea_reportmerge_claimantdirselect_button: QPushButton
    ea_reportmerge_claimantdir_section_label: QLabel
    ea_reportmerge_selectedclaimantdir_label: QLabel
    reportmerge_orgsubframe: QFrame
    reportmerge_orgsubframe_GLayout: QGridLayout
    ea_reportmerge_sub2frame: QFrame
    ea_reportmerge_sub2frame_GLayout: QGridLayout
    ea_reportmerge_sub2frame_section_label: QLabel

    # Report merge — projection type
    ea_reportmerge_projectiontype_sub3frame: QFrame
    ea_reportmerge_projectiontype_GLayout: QGridLayout
    ea_reportmerge_projectiontype_label: QLabel
    ea_reportmerge_projectiontype_combobox: QComboBox

    # Report merge — report template types
    ea_reportmerge_reporttypes_sub3frame: QFrame
    ea_reportmerge_reporttypes_GLayout: QGridLayout
    ea_reportmerge_reporttypes_label: QLabel
    ea_reportmerge_reporttypes_PVLCP_checkbox: QCheckBox
    ea_reportmerge_reporttypes_PVearnings_checkbox: QCheckBox

    # Report merge — reference reports selection
    ea_reportmerge_referencereports_sub3frame: QFrame
    ea_reportmerge_referencereports_GLayout: QGridLayout
    ea_reportmerge_referencereports_label: QLabel
    ea_reportmerge_referencereports_voc_checkbox: QCheckBox
    ea_reportmerge_referencereports_lcp_checkbox: QCheckBox
    ea_reportmerge_referencereports_mcp_checkbox: QCheckBox

    # Report merge — bases & credits
    ea_reportmerge_bases_sub3frame: QFrame
    ea_reportmerge_bases_GLayout: QGridLayout
    ea_reportmerge_bases_label: QLabel
    ea_reportmerge_base1_checkbox: QCheckBox
    ea_reportmerge_base2_checkbox: QCheckBox
    ea_reportmerge_base3_checkbox: QCheckBox
    ea_reportmerge_credit1_checkbox: QCheckBox
    ea_reportmerge_credit2_checkbox: QCheckBox
    ea_reportmerge_credit3_checkbox: QCheckBox
    ea_reportmerge_meals_checkbox: QCheckBox
    ea_reportmerge_benefits_checkbox: QCheckBox

    # Report merge — tax status
    ea_reportmerge_taxstatus_sub3frame: QFrame
    ea_reportmerge_taxstatus_GLayout: QGridLayout
    ea_reportmerge_taxstatus_label: QLabel
    ea_reportmerge_taxstatus_checkbox: QCheckBox

    # Placeholder frames (to be renamed/replaced)
    frame_4: QFrame
    gridLayout_4: QGridLayout
    label_4: QLabel
    checkBox_4: QCheckBox
    frame_6: QFrame
    gridLayout_6: QGridLayout
    label_6: QLabel
    checkBox_6: QCheckBox
    frame_8: QFrame
    gridLayout_8: QGridLayout
    label_8: QLabel
    checkBox_8: QCheckBox

    def __init__(self, ea_MainWindow: QMainWindow):
        self.ea_MainWindow = ea_MainWindow

    def setupUi(self):
        if not self.ea_MainWindow.objectName():
            self.ea_MainWindow.setObjectName("ea_MainWindow")

        horizontal_spacer_l = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )
        horizontal_spacer_r = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
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
            "dark_navy": "#001542",
            "light_blue": "#ADD8E6",
            "dark_light_blue": "#7EB8CB",
            "dark_gold": "#8D7B00",
            "deep_gold": "#9D8A0A",
            "gold": "#AD9915",
            "warm_gold": "#BEAA24",
            "light_gold": "#D0BC34",
            "gold_border": "rgba(141,123,0,0.4)",
            "gold_highlight": "rgba(255,245,150,0.32)",
            "gold_shadow_border": "rgba(0,0,0,0.32)",
        }

        icon_fmt = {
            **color_dict,
            "checkmark_icon": icon_dict.get("checkmark_icon", "").replace("\\", "/"),
            "dropdown_arrow_icon": icon_dict.get("dropdown_arrow_icon", "").replace(
                "\\", "/"
            ),
        }

        self._color_dict = color_dict
        self._icon_fmt = icon_fmt

        self.ea_MainWindow.resize(550, 600)
        self.ea_MainWindow.setWindowIcon(QIcon(icon_dict["econautomation_icon"]))
        self.ea_MainWindow.setWindowTitle("EconAutomation")

        self.ea_CentralWidget = QWidget(self.ea_MainWindow)
        self.ea_CentralWidget.setObjectName("ea_CentralWidget")
        self.ea_CentralWidget_GLayout = QGridLayout(self.ea_CentralWidget)
        self.ea_CentralWidget_GLayout.setObjectName("ea_CentralWidget_GLayout")
        self.ea_CentralWidget_GLayout.setContentsMargins(0, 0, 0, 0)
        self.ea_CentralWidget_frame = QFrame(self.ea_CentralWidget)
        self.ea_CentralWidget_frame.setObjectName("ea_CentralWidget_frame")
        self.ea_CentralWidget_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.ea_CentralWidget_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.ea_CentralWidgetframe_GLayout = QGridLayout(self.ea_CentralWidget_frame)
        self.ea_CentralWidgetframe_GLayout.setObjectName(
            "ea_CentralWidgetframe_GLayout"
        )
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

        self.ea_setupfile_GLayout = QGridLayout(self.ea_setupcase_frame)
        self.ea_setupfile_GLayout.setObjectName("ea_setupfile_GLayout")
        self.ea_setupfile_GLayout.setHorizontalSpacing(5)
        self.ea_setupfile_GLayout.setVerticalSpacing(0)
        self.ea_setupfile_GLayout.setContentsMargins(5, 5, 5, 5)

        self.ea_setupcase_orgsubframe = QFrame(self.ea_setupcase_frame)
        self.ea_setupcase_orgsubframe.setObjectName("ea_setupcase_orgsubframe")
        self.ea_setupcase_orgsubframe.setFrameShape(QFrame.Shape.NoFrame)
        self.ea_setupcase_orgsubframe.setFrameShadow(QFrame.Shadow.Raised)
        self.ea_setupcase_orgsubframe_GLayout = QGridLayout(
            self.ea_setupcase_orgsubframe
        )
        self.ea_setupcase_orgsubframe_GLayout.setObjectName(
            "ea_setupcase_orgsubframe_GLayout"
        )
        self.ea_setupcase_orgsubframe_GLayout.setContentsMargins(3, 3, 3, 3)

        self.ea_setupcase_label = QLabel(self.ea_setupcase_orgsubframe)
        self.ea_setupcase_label.setObjectName("ea_setupcase_label")
        self.ea_setupcase_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.ea_setupcase_orgsubframe_GLayout.addWidget(
            self.ea_setupcase_label, 0, 0, 1, 3
        )

        self.ea_setupcase_sub2frame = QFrame(self.ea_setupcase_orgsubframe)
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

        self.ea_setupcase_orgsubframe_GLayout.addWidget(
            self.ea_setupcase_sub2frame, 1, 0, 1, 3
        )

        self.ea_setupcase_createcase_button = QPushButton(self.ea_setupcase_orgsubframe)
        self.ea_setupcase_createcase_button.setObjectName(
            "ea_setupcase_createcase_button"
        )

        self.ea_setupcase_orgsubframe_GLayout.addItem(horizontal_spacer_l, 2, 0, 1, 1)
        self.ea_setupcase_orgsubframe_GLayout.addWidget(
            self.ea_setupcase_createcase_button, 2, 1, 1, 1
        )
        self.ea_setupcase_orgsubframe_GLayout.addItem(horizontal_spacer_r, 2, 2, 1, 1)
        self.ea_setupcase_orgsubframe_GLayout.setRowStretch(0, 1)
        self.ea_setupcase_orgsubframe_GLayout.setRowStretch(1, 10)

        self.ea_setupfile_GLayout.addWidget(self.ea_setupcase_orgsubframe, 0, 0, 1, 1)

        self.ea_CentralWidgetframe_GLayout.addWidget(
            self.ea_setupcase_frame, 1, 0, 1, 3
        )

        self.ea_reportmerge_frame = QFrame(self.ea_CentralWidget_frame)
        self.ea_reportmerge_frame.setObjectName("ea_reportmerge_frame")
        self.ea_reportmerge_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.ea_reportmerge_frame.setFrameShadow(QFrame.Shadow.Raised)

        self.ea_reportmerge_GLayout = QGridLayout(self.ea_reportmerge_frame)
        self.ea_reportmerge_GLayout.setObjectName("ea_reportmerge_GLayout")
        self.ea_reportmerge_GLayout.setHorizontalSpacing(0)
        self.ea_reportmerge_GLayout.setVerticalSpacing(3)
        self.ea_reportmerge_GLayout.setContentsMargins(5, 5, 5, 5)

        self.reportmerge_orgsubframe = QFrame(self.ea_reportmerge_frame)
        self.reportmerge_orgsubframe.setObjectName("reportmerge_orgsubframe")
        self.reportmerge_orgsubframe.setFrameShape(QFrame.Shape.StyledPanel)
        self.reportmerge_orgsubframe.setFrameShadow(QFrame.Shadow.Raised)
        self.reportmerge_orgsubframe_GLayout = QGridLayout(self.reportmerge_orgsubframe)
        self.reportmerge_orgsubframe_GLayout.setObjectName(
            "reportmerge_orgsubframe_GLayout"
        )
        self.reportmerge_orgsubframe_GLayout.setContentsMargins(5, 5, 5, 5)
        self.reportmerge_orgsubframe_GLayout.setSpacing(3)

        self.ea_reportmerge_sub2frame = QFrame(self.reportmerge_orgsubframe)
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

        self.ea_reportmerge_sub2frame_section_label = QLabel(
            self.ea_reportmerge_sub2frame
        )
        self.ea_reportmerge_sub2frame_section_label.setObjectName(
            "ea_reportmerge_sub2frame_section_label"
        )
        self.ea_reportmerge_sub2frame_section_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        self.ea_reportmerge_sub2frame_GLayout.addWidget(
            self.ea_reportmerge_sub2frame_section_label, 0, 0, 1, 2
        )

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

        self.ea_reportmerge_sub2frame_GLayout.addWidget(self.frame_4, 3, 1, 1, 1)

        self.ea_reportmerge_referencereports_sub3frame = QFrame(
            self.ea_reportmerge_sub2frame
        )
        self.ea_reportmerge_referencereports_sub3frame.setObjectName(
            "ea_reportmerge_referencereports_sub3frame"
        )
        self.ea_reportmerge_referencereports_sub3frame.setFrameShape(
            QFrame.Shape.NoFrame
        )
        self.ea_reportmerge_referencereports_sub3frame.setFrameShadow(
            QFrame.Shadow.Raised
        )
        self.ea_reportmerge_referencereports_GLayout = QGridLayout(
            self.ea_reportmerge_referencereports_sub3frame
        )
        self.ea_reportmerge_referencereports_GLayout.setObjectName(
            "ea_reportmerge_referencereports_GLayout"
        )
        self.ea_reportmerge_referencereports_label = QLabel(
            self.ea_reportmerge_referencereports_sub3frame
        )
        self.ea_reportmerge_referencereports_label.setObjectName(
            "ea_reportmerge_referencereports_label"
        )

        self.ea_reportmerge_referencereports_GLayout.addWidget(
            self.ea_reportmerge_referencereports_label, 0, 0, 1, 1
        )
        self.ea_reportmerge_referencereports_GLayout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )

        self.ea_reportmerge_referencereports_lcp_checkbox = QCheckBox(
            self.ea_reportmerge_referencereports_sub3frame
        )
        self.ea_reportmerge_referencereports_lcp_checkbox.setObjectName(
            "ea_reportmerge_referencereports_lcp_checkbox"
        )
        self.ea_reportmerge_referencereports_GLayout.addWidget(
            self.ea_reportmerge_referencereports_lcp_checkbox, 1, 0, 1, 1
        )

        self.ea_reportmerge_referencereports_voc_checkbox = QCheckBox(
            self.ea_reportmerge_referencereports_sub3frame
        )
        self.ea_reportmerge_referencereports_voc_checkbox.setObjectName(
            "ea_reportmerge_referencereports_voc_checkbox"
        )
        self.ea_reportmerge_referencereports_GLayout.addWidget(
            self.ea_reportmerge_referencereports_voc_checkbox, 2, 0, 1, 1
        )

        self.ea_reportmerge_referencereports_mcp_checkbox = QCheckBox(
            self.ea_reportmerge_referencereports_sub3frame
        )
        self.ea_reportmerge_referencereports_mcp_checkbox.setObjectName(
            "ea_reportmerge_referencereports_mcp_checkbox"
        )
        self.ea_reportmerge_referencereports_GLayout.addWidget(
            self.ea_reportmerge_referencereports_mcp_checkbox, 3, 0, 1, 1
        )

        self.ea_reportmerge_sub2frame_GLayout.addWidget(
            self.ea_reportmerge_referencereports_sub3frame, 3, 0, 1, 1
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

        self.ea_reportmerge_sub2frame_GLayout.addWidget(self.frame_6, 4, 1, 1, 1)

        self.ea_reportmerge_bases_sub3frame = QFrame(self.ea_reportmerge_sub2frame)
        self.ea_reportmerge_bases_sub3frame.setObjectName(
            "ea_reportmerge_bases_sub3frame"
        )
        self.ea_reportmerge_bases_sub3frame.setFrameShape(QFrame.Shape.NoFrame)
        self.ea_reportmerge_bases_sub3frame.setFrameShadow(QFrame.Shadow.Raised)

        self.ea_reportmerge_bases_GLayout = QGridLayout(
            self.ea_reportmerge_bases_sub3frame
        )
        self.ea_reportmerge_bases_GLayout.setContentsMargins(0, 0, 0, 0)
        self.ea_reportmerge_bases_GLayout.setHorizontalSpacing(6)
        self.ea_reportmerge_bases_GLayout.setVerticalSpacing(4)
        self.ea_reportmerge_bases_GLayout.setObjectName("ea_reportmerge_bases_GLayout")
        self.ea_reportmerge_bases_GLayout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )
        self.ea_reportmerge_credit2_checkbox = QCheckBox(
            self.ea_reportmerge_bases_sub3frame
        )
        self.ea_reportmerge_credit2_checkbox.setObjectName(
            "ea_reportmerge_credit2_checkbox"
        )

        self.ea_reportmerge_bases_GLayout.addWidget(
            self.ea_reportmerge_credit2_checkbox, 2, 1, 1, 1
        )

        self.ea_reportmerge_base1_checkbox = QCheckBox(
            self.ea_reportmerge_bases_sub3frame
        )
        self.ea_reportmerge_base1_checkbox.setObjectName(
            "ea_reportmerge_base1_checkbox"
        )

        self.ea_reportmerge_bases_GLayout.addWidget(
            self.ea_reportmerge_base1_checkbox, 1, 0, 1, 1
        )

        self.ea_reportmerge_credit3_checkbox = QCheckBox(
            self.ea_reportmerge_bases_sub3frame
        )
        self.ea_reportmerge_credit3_checkbox.setObjectName(
            "ea_reportmerge_credit3_checkbox"
        )

        self.ea_reportmerge_bases_GLayout.addWidget(
            self.ea_reportmerge_credit3_checkbox, 3, 1, 1, 1
        )

        self.ea_reportmerge_bases_label = QLabel(self.ea_reportmerge_bases_sub3frame)
        self.ea_reportmerge_bases_label.setObjectName("ea_reportmerge_bases_label")

        self.ea_reportmerge_bases_GLayout.addWidget(
            self.ea_reportmerge_bases_label, 0, 0, 1, 1
        )

        self.ea_reportmerge_base2_checkbox = QCheckBox(
            self.ea_reportmerge_bases_sub3frame
        )
        self.ea_reportmerge_base2_checkbox.setObjectName(
            "ea_reportmerge_base2_checkbox"
        )

        self.ea_reportmerge_bases_GLayout.addWidget(
            self.ea_reportmerge_base2_checkbox, 2, 0, 1, 1
        )

        self.ea_reportmerge_base3_checkbox = QCheckBox(
            self.ea_reportmerge_bases_sub3frame
        )
        self.ea_reportmerge_base3_checkbox.setObjectName(
            "ea_reportmerge_base3_checkbox"
        )

        self.ea_reportmerge_bases_GLayout.addWidget(
            self.ea_reportmerge_base3_checkbox, 3, 0, 1, 1
        )

        self.ea_reportmerge_credit1_checkbox = QCheckBox(
            self.ea_reportmerge_bases_sub3frame
        )
        self.ea_reportmerge_credit1_checkbox.setObjectName(
            "ea_reportmerge_credit1_checkbox"
        )

        self.ea_reportmerge_bases_GLayout.addWidget(
            self.ea_reportmerge_credit1_checkbox, 1, 1, 1, 1
        )

        self.ea_reportmerge_meals_checkbox = QCheckBox(
            self.ea_reportmerge_bases_sub3frame
        )
        self.ea_reportmerge_meals_checkbox.setObjectName(
            "ea_reportmerge_meals_checkbox"
        )

        self.ea_reportmerge_bases_GLayout.addWidget(
            self.ea_reportmerge_meals_checkbox, 4, 0, 1, 1
        )

        self.ea_reportmerge_benefits_checkbox = QCheckBox(
            self.ea_reportmerge_bases_sub3frame
        )
        self.ea_reportmerge_benefits_checkbox.setObjectName(
            "ea_reportmerge_benefits_checkbox"
        )

        self.ea_reportmerge_bases_GLayout.addWidget(
            self.ea_reportmerge_benefits_checkbox, 4, 1, 1, 1
        )

        self.ea_reportmerge_sub2frame_GLayout.addWidget(
            self.ea_reportmerge_bases_sub3frame, 4, 0, 1, 1
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

        self.ea_reportmerge_reporttypes_label = QLabel(
            self.ea_reportmerge_reporttypes_sub3frame
        )
        self.ea_reportmerge_reporttypes_label.setObjectName(
            "ea_reportmerge_reporttypes_label"
        )

        self.ea_reportmerge_reporttypes_GLayout.addWidget(
            self.ea_reportmerge_reporttypes_label, 0, 0, 1, 1
        )

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
            self.ea_reportmerge_reporttypes_sub3frame, 2, 1, 1, 1
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
            self.ea_reportmerge_taxstatus_sub3frame, 5, 0, 1, 1
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
            self.ea_reportmerge_projectiontype_sub3frame, 2, 0, 1, 1
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

        self.ea_reportmerge_sub2frame_GLayout.addWidget(self.frame_8, 5, 1, 1, 1)

        self.reportmerge_orgsubframe_GLayout.addWidget(
            self.ea_reportmerge_sub2frame, 1, 0, 1, 1
        )

        self.ea_reportmerge_label = QLabel(self.ea_reportmerge_frame)
        self.ea_reportmerge_label.setObjectName("ea_reportmerge_label")
        self.ea_reportmerge_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.ea_reportmerge_GLayout.addWidget(self.ea_reportmerge_label, 0, 0, 1, 1)

        self.ea_reportmerge_claimantdir_subframe = QFrame(self.reportmerge_orgsubframe)
        self.ea_reportmerge_claimantdir_subframe.setObjectName(
            "ea_reportmerge_claimantdir_subframe"
        )
        self.ea_reportmerge_claimantdir_subframe.setFrameShape(QFrame.Shape.NoFrame)
        self.ea_reportmerge_claimantdir_subframe.setFrameShadow(QFrame.Shadow.Raised)
        self.ea_reportmerge_claimantdir_subframe_GLayout = QGridLayout(
            self.ea_reportmerge_claimantdir_subframe
        )
        self.ea_reportmerge_claimantdir_subframe_GLayout.setObjectName(
            "ea_reportmerge_claimantdir_subframe_GLayout"
        )

        self.ea_reportmerge_claimantdir_subframe_GLayout.setContentsMargins(8, 8, 8, 8)
        self.ea_reportmerge_claimantdir_subframe_GLayout.setVerticalSpacing(8)
        self.ea_reportmerge_claimantdir_subframe_GLayout.setHorizontalSpacing(8)

        self.reportmerge_orgsubframe_GLayout.addWidget(
            self.ea_reportmerge_claimantdir_subframe, 0, 0, 1, 1
        )
        self.ea_reportmerge_GLayout.addWidget(self.reportmerge_orgsubframe, 1, 0, 1, 1)

        self.ea_reportmerge_claimantdir_section_label = QLabel(
            self.ea_reportmerge_claimantdir_subframe
        )
        self.ea_reportmerge_claimantdir_section_label.setObjectName(
            "ea_reportmerge_claimantdir_section_label"
        )
        self.ea_reportmerge_claimantdir_section_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.ea_reportmerge_claimantdir_subframe_GLayout.addWidget(
            self.ea_reportmerge_claimantdir_section_label, 0, 0, 1, 4
        )

        self.ea_reportmerge_claimantdirselect_button = QPushButton(
            self.ea_reportmerge_claimantdir_subframe
        )

        self.ea_reportmerge_claimantdirselect_button.setObjectName(
            "ea_reportmerge_claimantdirselect_button"
        )
        self.ea_reportmerge_claimantdirselect_button.setIcon(
            QIcon(icon_dict["add_note_icon"])
        )

        self.ea_reportmerge_claimantdir_subframe_GLayout.addWidget(
            self.ea_reportmerge_claimantdirselect_button, 1, 3, 1, 1
        )

        self.ea_reportmerge_selectedclaimantdir_label = QLabel(
            self.ea_reportmerge_claimantdir_subframe
        )
        self.ea_reportmerge_selectedclaimantdir_label.setObjectName(
            "ea_reportmerge_selectedclaimantdir_label"
        )
        self.ea_reportmerge_selectedclaimantdir_label.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom
        )

        self.ea_reportmerge_claimantdir_subframe_GLayout.addWidget(
            self.ea_reportmerge_selectedclaimantdir_label, 1, 0, 1, 3
        )

        self.ea_reportmerge_claimantdir_subframe_GLayout.addItem(
            QSpacerItem(
                20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
            ),
            2,
            0,
            1,
            4,
        )

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

        def _frame_shadow():
            effect = QGraphicsDropShadowEffect()
            effect.setBlurRadius(8)
            effect.setXOffset(1)
            effect.setYOffset(2)
            effect.setColor(QColor(0, 0, 0, 60))
            return effect

        self.ea_CentralWidget_label_frame.setGraphicsEffect(_frame_shadow())
        self.ea_setupcase_frame.setGraphicsEffect(_frame_shadow())
        self.ea_reportmerge_frame.setGraphicsEffect(_frame_shadow())

        self.ea_MainWindow.setCentralWidget(self.ea_CentralWidget)

        self._apply_styles(1.0)
        self.retranslateUi()

        QMetaObject.connectSlotsByName(self.ea_MainWindow)

    # setupUi

    def _apply_styles(self, scale: float) -> None:
        fs = {
            "fs_header": max(10, round(18 * scale)),
            "fs_section": max(8, round(13 * scale)),
            "fs_subsection": max(8, round(12.5 * scale)),
            "fs_body": max(7, round(12 * scale)),
            "fs_small": max(7, round(11 * scale)),
            "fs_xs": max(6, round(10 * scale)),
        }
        fmt = {**self._icon_fmt, **fs}

        ea_background_style = """
            #ea_CentralWidget_frame {{
                border: none;
                background-color: {dark_navy};
            }}
        """.format(**fmt)

        ea_header_style = """
            #ea_CentralWidget_label_frame {{
                border-top: 2px solid {gold_highlight};
                border-left: 2px solid {gold_highlight};
                border-bottom: 2px solid {gold_shadow_border};
                border-right: 2px solid {gold_shadow_border};
                border-radius: 8px;
                background-color: {gold};
            }}
            #ea_CentralWidget_label {{
                background-color: {light_gold};
                border-top: 2px solid {gold_highlight};
                border-left: 2px solid {gold_highlight};
                border-bottom: 2px solid {gold_shadow_border};
                border-right: 2px solid {gold_shadow_border};
                border-radius: 4px;
                font-family: DM Sans;
                font-size: {fs_header}pt;
                font-weight: 800;
                font-style: italic;
                color: {dark_navy};
            }}
        """.format(**fmt)

        ea_setupcase_style = """
            #ea_setupcase_frame {{
                border-top: 2px solid {gold_highlight};
                border-left: 2px solid {gold_highlight};
                border-bottom: 2px solid {gold_shadow_border};
                border-right: 2px solid {gold_shadow_border};
                border-radius: 8px;
                background-color: {dark_gold};
            }}
            #ea_setupcase_orgsubframe {{
                background-color: {warm_gold};
                border-top: 2px solid {gold_highlight};
                border-left: 2px solid {gold_highlight};
                border-bottom: 2px solid {gold_shadow_border};
                border-right: 2px solid {gold_shadow_border};
                border-radius: 8px;
            }}
            #ea_setupcase_frame #ea_setupcase_label {{
                background-color: {light_gold};
                border-top: 2px solid {gold_highlight};
                border-left: 2px solid {gold_highlight};
                border-bottom: 2px solid {gold_shadow_border};
                border-right: 2px solid {gold_shadow_border};
                border-radius: 4px;
                font-family: DM Sans;
                font-size: {fs_section}pt;
                font-weight: 600;
                color: {dark_navy};
                padding: 3px;
            }}
            #ea_setupcase_sub2frame {{
                border: none;
                background-color: transparent;
            }}
            #ea_setupcase_sub2frame QLabel {{
                background-color: transparent;
                border: none;
                font-family: Figtree;
                font-size: {fs_small}pt;
                font-weight: 400;
                color: {dark_navy};
            }}
            #ea_setupcase_sub2frame #ea_setupcase_selectedOFF_label {{
                background-color: white;
                border: 1px solid {dark_navy};
                border-radius: 4px;
                font-family: Figtree;
                font-size: {fs_xs}pt;
                font-weight: 300;
                color: {dark_navy};
            }}
            #ea_setupcase_sub2frame #ea_setupcase_OFFSelect_button {{
                border: 1px solid {dark_navy};
                border-radius: 4px;
                background-color: white;
                font-family: Figtree;
                font-size: {fs_body}pt;
                font-weight: 500;
                color: {dark_navy};
            }}
            #ea_setupcase_sub2frame #ea_setupcase_OFFSelect_button:hover {{
                background-color: {off_white};
            }}
            #ea_setupcase_frame #ea_setupcase_createcase_button {{
                border: 1px solid {dark_navy};
                border-radius: 4px;
                background-color: white;
                font-family: Figtree;
                font-size: {fs_xs}pt;
                font-weight: 400;
                color: {dark_navy};
                padding: 3px;
            }}
            #ea_setupcase_frame #ea_setupcase_createcase_button:hover {{
                background-color: {off_white};
            }}
        """.format(**fmt)

        ea_reportmerge_style = """
            #ea_reportmerge_frame {{
                border-top: 2px solid {gold_highlight};
                border-left: 2px solid {gold_highlight};
                border-bottom: 2px solid {gold_shadow_border};
                border-right: 2px solid {gold_shadow_border};
                border-radius: 8px;
                background-color: {dark_gold};
            }}
            #ea_reportmerge_frame #ea_reportmerge_label {{
                background-color: {light_gold};
                border-top: 2px solid {gold_highlight};
                border-left: 2px solid {gold_highlight};
                border-bottom: 2px solid {gold_shadow_border};
                border-right: 2px solid {gold_shadow_border};
                border-radius: 4px;
                font-family: DM Sans;
                font-size: {fs_section}pt;
                font-weight: 600;
                color: {dark_navy};
                padding: 3px;
            }}
            #ea_reportmerge_frame #reportmerge_orgsubframe {{
                background-color: {deep_gold};
                border-top: 2px solid {gold_highlight};
                border-left: 2px solid {gold_highlight};
                border-bottom: 2px solid {gold_shadow_border};
                border-right: 2px solid {gold_shadow_border};
                border-radius: 8px;
            }}
            #ea_reportmerge_frame #ea_reportmerge_sub2frame {{
                border-top: 2px solid {gold_highlight};
                border-left: 2px solid {gold_highlight};
                border-bottom: 2px solid {gold_shadow_border};
                border-right: 2px solid {gold_shadow_border};
                border-radius: 8px;
                background-color: {gold};
            }}
            #ea_reportmerge_sub2frame QFrame {{
                background-color: transparent;
                border: none;
            }}
            #ea_reportmerge_sub2frame QLabel {{
                background-color: transparent;
                border: none;
                font-family: Figtree;
                font-size: {fs_xs}pt;
                font-weight: 400;
                color: {dark_navy};
            }}
            #ea_reportmerge_sub2frame #ea_reportmerge_sub2frame_section_label {{
                background-color: transparent;
                border-color: transparent;
                font-family: DM Sans;
                font-size: {fs_section}pt;
                font-weight: 600;
                color: {dark_navy};
                padding: 3px;
            }}
            #ea_reportmerge_sub2frame QCheckBox {{
                font-family: Figtree;
                font-size: {fs_xs}pt;
                font-weight: 400;
                color: {dark_navy};
            }}
            #ea_reportmerge_sub2frame QCheckBox::indicator {{
                width: 14px;
                height: 14px;
                background-color: white;
                border: 1px solid {dark_navy};
                border-radius: 4px;
            }}
            #ea_reportmerge_sub2frame QCheckBox::indicator:unchecked {{
                background-color: white;
            }}
            #ea_reportmerge_sub2frame QCheckBox::indicator:disabled {{
                background-color: lightgray;
            }}
            #ea_reportmerge_sub2frame QCheckBox::indicator:checked {{
                background-color: white;
                image: url({checkmark_icon});
            }}
            #ea_reportmerge_sub2frame QComboBox {{
                background-color: white;
                border: 1px solid {dark_navy};
                border-radius: 4px;
                font-family: Figtree;
                font-size: {fs_xs}pt;
                color: {dark_navy};
                padding: 3px;
            }}
            #ea_reportmerge_sub2frame QComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: center right;
                background-color: transparent;
                border-color: transparent;
                padding: 3px;
            }}
            #ea_reportmerge_sub2frame QComboBox::down-arrow {{
                background-color: transparent;
                image: url({dropdown_arrow_icon});
            }}
            #ea_reportmerge_sub2frame QComboBox QAbstractItemView {{
                border: 1px solid {dark_navy};
                selection-background-color: {light_blue};
                background-color: white;
                color: {dark_navy};
            }}
            #ea_reportmerge_frame #ea_reportmerge_claimantdir_subframe {{
                border-top: 2px solid {gold_highlight};
                border-left: 2px solid {gold_highlight};
                border-bottom: 2px solid {gold_shadow_border};
                border-right: 2px solid {gold_shadow_border};
                border-radius: 8px;
                background-color: {warm_gold};
            }}
            #ea_reportmerge_frame #ea_reportmerge_claimantdir_subframe #ea_reportmerge_claimantdir_section_label {{
                background-color: transparent;
                border-color: transparent;
                font-family: DM Sans;
                font-size: {fs_body}pt;
                font-weight: 500;
                color: {dark_navy};
                padding: 3px;
            }}
            #ea_reportmerge_frame #ea_reportmerge_claimantdir_subframe #ea_reportmerge_selectedclaimantdir_label {{
                font-family: Figtree;
                font-size: {fs_xs}pt;
                font-weight: 300;
                color: {dark_navy};
                background-color: white;
                border: 1px solid {dark_navy};
                border-radius: 4px;
            }}
            #ea_reportmerge_frame #ea_reportmerge_claimantdir_subframe #ea_reportmerge_claimantdirselect_button {{
                border: 1px solid {dark_navy};
                border-radius: 4px;
                background-color: white;
                font-family: Figtree;
                font-size: {fs_xs}pt;
                font-weight: 400;
                color: {dark_navy};
                padding: 3px;
            }}
            #ea_reportmerge_frame #ea_reportmerge_claimantdir_subframe #ea_reportmerge_claimantdirselect_button:hover {{
                background-color: {off_white};
            }}
            #ea_reportmerge_frame #ea_reportmerge_claimantdir_subframe #ea_reportmerge_claimantdirselect_button:pressed {{
                background-color: gray;
            }}
            #ea_reportmerge_frame #ea_reportmerge_button {{
                border: 1px solid {dark_navy};
                border-radius: 4px;
                background-color: white;
                font-family: Figtree;
                font-size: {fs_body}pt;
                font-weight: 500;
                color: {dark_navy};
            }}
            #ea_reportmerge_frame #ea_reportmerge_button:hover {{
                background-color: {off_white};
            }}
            #ea_reportmerge_frame #ea_reportmerge_button:pressed {{
                background-color: gray;
            }}
        """.format(**fmt)

        self.ea_CentralWidget_frame.setStyleSheet(ea_background_style)
        self.ea_CentralWidget_label_frame.setStyleSheet(ea_header_style)
        self.ea_setupcase_frame.setStyleSheet(ea_setupcase_style)
        self.ea_reportmerge_frame.setStyleSheet(ea_reportmerge_style)

    def retranslateUi(self):
        self.ea_MainWindow.setWindowTitle(
            QCoreApplication.translate("ea_MainWindow", "EconAutomation", None)
        )
        self.ea_setupcase_label.setText(
            QCoreApplication.translate("ea_MainWindow", "New Case Set Up", None)
        )
        self.ea_setupcase_OFFSelect_button.setText(
            QCoreApplication.translate("ea_MainWindow", "", None)
        )
        self.ea_setupcase_selectedOFF_label.setText(
            QCoreApplication.translate(
                "ea_MainWindow", "No claimant OFF selected.", None
            )
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
        self.ea_reportmerge_referencereports_label.setText(
            QCoreApplication.translate("ea_MainWindow", "Reference Report(s):", None)
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
        self.ea_reportmerge_benefits_checkbox.setText(
            QCoreApplication.translate("ea_MainWindow", "Benefits", None)
        )
        self.ea_reportmerge_reporttypes_PVLCP_checkbox.setText(
            QCoreApplication.translate("ea_MainWindow", "PVLCP", None)
        )
        self.ea_reportmerge_reporttypes_label.setText(
            QCoreApplication.translate("ea_MainWindow", "Report Template(s):", None)
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
        self.ea_reportmerge_claimantdir_section_label.setText(
            QCoreApplication.translate(
                "ea_MainWindow", "Choose Econ Claimant Folder", None
            )
        )
        self.ea_reportmerge_selectedclaimantdir_label.setText(
            QCoreApplication.translate(
                "ea_MainWindow", "No Econ claimant folder selected.", None
            )
        )
        self.ea_reportmerge_claimantdirselect_button.setText(
            QCoreApplication.translate("ea_MainWindow", "", None)
        )
        self.ea_reportmerge_sub2frame_section_label.setText(
            QCoreApplication.translate("ea_MainWindow", "Report Options", None)
        )
        self.ea_reportmerge_label.setText(
            QCoreApplication.translate("ea_MainWindow", "Report Merge", None)
        )
        self.ea_reportmerge_button.setText(
            QCoreApplication.translate("ea_MainWindow", "Merge", None)
        )
        self.ea_CentralWidget_label.setText(
            QCoreApplication.translate("ea_MainWindow", "EconAutomation", None)
        )

    # retranslateUi
