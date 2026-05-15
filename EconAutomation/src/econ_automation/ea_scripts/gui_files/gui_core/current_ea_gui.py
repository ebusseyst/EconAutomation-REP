# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'econ_automation_ui.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
from pathlib import Path

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)
from econ_automation.ea_scripts.gui_files.gui_core import ea_fontset1
from econ_automation.ea_scripts.gui_files.gui_core import ea_iconset1

# Get the folder where this script lives
basedir = Path(__file__).resolve().parent.parent

# Build the full path to the icon
icon_path = str(basedir / "icons/bolt_boost_icon.png")

class Ui_ea_MainWindow(object):
    def __init__(self, ea_MainWindow):
        self.ea_MainWindow = ea_MainWindow
        
    def setupUi(self):
        if not self.ea_MainWindow.objectName():
            self.ea_MainWindow.setObjectName(u"ea_MainWindow")
        
        # 1. Load the font file
        font_dict = {
            "DM Sans Regular": QFontDatabase.addApplicationFont(":/fonts/DMSans-Regular-VariableFont.ttf"),
            "DM Sans Italic": QFontDatabase.addApplicationFont(":/fonts/DMSans-Italic-VariableFont.tff"),
            "Figtree Regular": QFontDatabase.addApplicationFont(":/fonts/Figtree-Regular-VariableFont.ttf"),
            "Figtree Italic": QFontDatabase.addApplicationFont(":/fonts/Figtree-Italic-VariableFont.ttf"),
            "IBM Plex Mono Regular": QFontDatabase.addApplicationFont(":/fonts/IBMPlexMono-Regular.ttf"),
            "IBM Plex Mono Italic": QFontDatabase.addApplicationFont(":/fonts/IBMPlexMono-Italic.ttf"),
        }

        for font_name, font_id in font_dict.items():
            if font_id != -1:
                font_families = QFontDatabase.applicationFontFamilies(font_id)
                # DEBUGGING
                print("=================================================")
                print("Font Name: ", font_name)
                print("Font ID: ", font_id)
                print("Font Families: ", font_families)
                print("=================================================")
                if font_families:
                    custom_font = QFont(font_families[0])
                    setattr(self.ea_MainWindow, font_name, custom_font)
        
        color_dict = {
            "off_white": "#ECECEC",
            "dark_navy": "#011F5B",
            "light_blue": "#ADD8E6",
            "dark_light_blue": "#7EB8CB",
            "gold": "#AD9915",
            "light_gold": "#D0BC34",
            "dark_gold": "#8D7B00",
            "gold_border": "rgba(141,123,0,0.4)"
        }
        
        self.ea_MainWindow.resize(1000, 600)
        self.ea_MainWindow.setWindowIcon(QIcon(icon_path))
        self.ea_MainWindow.setWindowTitle("EconLightning")
        self.ea_CentralWidget = QWidget(self.ea_MainWindow)
        ea_CentralWidget_style ="""
                                QLabel {{
                                    background-color: {light_gold};
                                    border: 2px solid {gold_border};
                                    border-radius: 4px;
                                    font-family: DM Sans Regular;
                                    font-size: 18pt;
                                    font-weight: 600;
                                    color: {dark_navy};
                                }}
                                QPushButton {{
                                    border: 1px solid {dark_navy};
                                    border-radius: 4px;
                                    background-color: {off_white};
                                    font-family: Figtree Regular;
                                    font-size: 12pt;
                                    font-weight: 500;
                                    color: {dark_navy};
                                }}
                                QPushButton:hover {{
                                    font-family: Figtree Regular;
                                    font-size: 12pt;
                                    font-weight: 500;
                                    color: {dark_navy};
                                }}
                                QFrame {{
                                    border: 0px;
                                    border-radius: 10px;
                                    background-color: {dark_gold};
                                }}
                                #ea_CentralWidget_frame {{
                                    border: none;
                                    border-radius: 0px;
                                    background-color: {dark_navy};
                                }}
                                #ea_CentralWidget_label_frame {{
                                    border: 2px solid {gold_border};
                                }}
                                """.format(
                                    light_gold=color_dict['light_gold'],
                                    gold_border=color_dict['gold_border'],
                                    off_white=color_dict['off_white'],
                                    dark_navy=color_dict['dark_navy'],
                                    dark_gold=color_dict['dark_gold'],
                                )
        self.ea_CentralWidget.setStyleSheet(ea_CentralWidget_style)
        self.ea_CentralWidget.setObjectName(u"ea_CentralWidget")
        self.ea_CentralWidget_HLayout = QHBoxLayout(self.ea_CentralWidget)
        self.ea_CentralWidget_HLayout.setObjectName(u"ea_CentralWidget_HLayout")
        self.ea_CentralWidget_HLayout.setContentsMargins(0, 0, 0, 0)
        self.ea_CentralWidget_frame = QFrame(self.ea_CentralWidget)
        self.ea_CentralWidget_frame.setObjectName(u"ea_CentralWidget_frame")
        self.ea_CentralWidget_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.ea_CentralWidget_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.ea_CentralWidget_GLayout = QGridLayout(self.ea_CentralWidget_frame)
        self.ea_CentralWidget_GLayout.setObjectName(u"ea_CentralWidget_GLayout")
        self.ea_CentralWidget_GLayout.setHorizontalSpacing(8)
        self.ea_CentralWidget_GLayout.setVerticalSpacing(12)
        self.ea_setupcase_frame = QFrame(self.ea_CentralWidget_frame)
        self.ea_setupcase_frame.setObjectName(u"ea_setupcase_frame")
        self.ea_setupcase_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.ea_setupcase_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.ea_setupfile_GLayout = QGridLayout(self.ea_setupcase_frame)
        self.ea_setupfile_GLayout.setObjectName(u"ea_setupfile_GLayout")
        self.ea_setupfile_GLayout.setHorizontalSpacing(5)
        self.ea_setupfile_GLayout.setVerticalSpacing(0)
        self.ea_setupcase_label = QLabel(self.ea_setupcase_frame)
        self.ea_setupcase_label.setObjectName(u"ea_setupcase_label")
        self.ea_setupcase_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.ea_setupfile_GLayout.addWidget(self.ea_setupcase_label, 0, 0, 1, 1)

        self.ea_setupcase_sub2frame = QFrame(self.ea_setupcase_frame)
        self.ea_setupcase_sub2frame.setObjectName(u"ea_setupcase_sub2frame")
        self.ea_setupcase_sub2frame.setFrameShape(QFrame.Shape.NoFrame)
        self.ea_setupcase_sub2frame.setFrameShadow(QFrame.Shadow.Raised)
        self.ea_setupfile_sub2frame_GLayout = QGridLayout(self.ea_setupcase_sub2frame)
        self.ea_setupfile_sub2frame_GLayout.setObjectName(u"ea_setupfile_sub2frame_GLayout")
        self.ea_setupcase_OFFSelect_button = QPushButton(self.ea_setupcase_sub2frame)
        self.ea_setupcase_OFFSelect_button.setObjectName(u"ea_setupcase_OFFSelect_button")
        self.ea_setupcase_OFFSelect_button.setIcon(QIcon(":/icons/add_new_profile_icon.png"))

        self.ea_setupfile_sub2frame_GLayout.addWidget(self.ea_setupcase_OFFSelect_button, 0, 1, 1, 1)

        self.ea_setupcase_selectedOFF_label = QLabel(self.ea_setupcase_sub2frame)
        self.ea_setupcase_selectedOFF_label.setObjectName(u"ea_setupcase_selectedOFF_label")

        self.ea_setupfile_sub2frame_GLayout.addWidget(self.ea_setupcase_selectedOFF_label, 0, 0, 1, 1)


        self.ea_setupfile_GLayout.addWidget(self.ea_setupcase_sub2frame, 1, 0, 1, 1)

        self.ea_setupcase_createcase_button = QPushButton(self.ea_setupcase_frame)
        self.ea_setupcase_createcase_button.setObjectName(u"ea_setupcase_createcase_button")

        self.ea_setupfile_GLayout.addWidget(self.ea_setupcase_createcase_button, 2, 0, 1, 1)

        self.ea_setupfile_GLayout.setRowStretch(0, 1)
        self.ea_setupfile_GLayout.setRowStretch(1, 10)

        self.ea_CentralWidget_GLayout.addWidget(self.ea_setupcase_frame, 1, 0, 1, 1)

        self.ea_reportmerge_frame = QFrame(self.ea_CentralWidget_frame)
        self.ea_reportmerge_frame.setObjectName(u"ea_reportmerge_frame")
        self.ea_reportmerge_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.ea_reportmerge_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.ea_reportmerge_GLayout = QGridLayout(self.ea_reportmerge_frame)
        self.ea_reportmerge_GLayout.setObjectName(u"ea_reportmerge_GLayout")
        self.ea_reportmerge_GLayout.setHorizontalSpacing(0)
        self.ea_reportmerge_GLayout.setVerticalSpacing(5)
        self.ea_reportmerge_sub2frame = QFrame(self.ea_reportmerge_frame)
        self.ea_reportmerge_sub2frame.setObjectName(u"ea_reportmerge_sub2frame")
        self.ea_reportmerge_sub2frame.setFrameShape(QFrame.Shape.NoFrame)
        self.ea_reportmerge_sub2frame.setFrameShadow(QFrame.Shadow.Raised)
        self.ea_reportmerge_sub2frame_GLayout = QGridLayout(self.ea_reportmerge_sub2frame)
        self.ea_reportmerge_sub2frame_GLayout.setSpacing(5)
        self.ea_reportmerge_sub2frame_GLayout.setObjectName(u"ea_reportmerge_sub2frame_GLayout")
        self.frame_4 = QFrame(self.ea_reportmerge_sub2frame)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_4 = QLabel(self.frame_4)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_4.addWidget(self.label_4, 0, 0, 1, 1)

        self.checkBox_4 = QCheckBox(self.frame_4)
        self.checkBox_4.setObjectName(u"checkBox_4")

        self.gridLayout_4.addWidget(self.checkBox_4, 1, 0, 1, 1)


        self.ea_reportmerge_sub2frame_GLayout.addWidget(self.frame_4, 1, 1, 1, 1)

        self.ea_reportmerge_referencetype_sub3frame = QFrame(self.ea_reportmerge_sub2frame)
        self.ea_reportmerge_referencetype_sub3frame.setObjectName(u"ea_reportmerge_referencetype_sub3frame")
        self.ea_reportmerge_referencetype_sub3frame.setFrameShape(QFrame.Shape.NoFrame)
        self.ea_reportmerge_referencetype_sub3frame.setFrameShadow(QFrame.Shadow.Raised)
        self.ea_reportmerge_referencetype_GLayout = QGridLayout(self.ea_reportmerge_referencetype_sub3frame)
        self.ea_reportmerge_referencetype_GLayout.setObjectName(u"ea_reportmerge_referencetype_GLayout")
        self.ea_reportmerge_referencetype_label = QLabel(self.ea_reportmerge_referencetype_sub3frame)
        self.ea_reportmerge_referencetype_label.setObjectName(u"ea_reportmerge_referencetype_label")

        self.ea_reportmerge_referencetype_GLayout.addWidget(self.ea_reportmerge_referencetype_label, 0, 0, 1, 1)

        self.ea_reportmerge_referencetype_combobox = QComboBox(self.ea_reportmerge_referencetype_sub3frame)
        self.ea_reportmerge_referencetype_combobox.setObjectName(u"ea_reportmerge_referencetype_combobox")

        self.ea_reportmerge_referencetype_GLayout.addWidget(self.ea_reportmerge_referencetype_combobox, 1, 0, 1, 1)


        self.ea_reportmerge_sub2frame_GLayout.addWidget(self.ea_reportmerge_referencetype_sub3frame, 1, 0, 1, 1)

        self.frame_6 = QFrame(self.ea_reportmerge_sub2frame)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_6)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.checkBox_6 = QCheckBox(self.frame_6)
        self.checkBox_6.setObjectName(u"checkBox_6")

        self.gridLayout_6.addWidget(self.checkBox_6, 1, 0, 1, 1)

        self.label_6 = QLabel(self.frame_6)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_6.addWidget(self.label_6, 0, 0, 1, 1)


        self.ea_reportmerge_sub2frame_GLayout.addWidget(self.frame_6, 2, 1, 1, 1)

        self.ea_reportmerge_bases_sub3frame = QFrame(self.ea_reportmerge_sub2frame)
        self.ea_reportmerge_bases_sub3frame.setObjectName(u"ea_reportmerge_bases_sub3frame")
        self.ea_reportmerge_bases_sub3frame.setFrameShape(QFrame.Shape.NoFrame)
        self.ea_reportmerge_bases_sub3frame.setFrameShadow(QFrame.Shadow.Raised)
        self.ea_reportmerge_bases_GLayout = QGridLayout(self.ea_reportmerge_bases_sub3frame)
        self.ea_reportmerge_bases_GLayout.setSpacing(8)
        self.ea_reportmerge_bases_GLayout.setObjectName(u"ea_reportmerge_bases_GLayout")
        self.checkBox_9 = QCheckBox(self.ea_reportmerge_bases_sub3frame)
        self.checkBox_9.setObjectName(u"checkBox_9")

        self.ea_reportmerge_bases_GLayout.addWidget(self.checkBox_9, 2, 1, 1, 1)

        self.ea_reportmerge_base1_checkbox = QCheckBox(self.ea_reportmerge_bases_sub3frame)
        self.ea_reportmerge_base1_checkbox.setObjectName(u"ea_reportmerge_base1_checkbox")

        self.ea_reportmerge_bases_GLayout.addWidget(self.ea_reportmerge_base1_checkbox, 1, 0, 1, 1)

        self.checkBox_10 = QCheckBox(self.ea_reportmerge_bases_sub3frame)
        self.checkBox_10.setObjectName(u"checkBox_10")

        self.ea_reportmerge_bases_GLayout.addWidget(self.checkBox_10, 3, 1, 1, 1)

        self.ea_reportmerge_bases_label = QLabel(self.ea_reportmerge_bases_sub3frame)
        self.ea_reportmerge_bases_label.setObjectName(u"ea_reportmerge_bases_label")

        self.ea_reportmerge_bases_GLayout.addWidget(self.ea_reportmerge_bases_label, 0, 0, 1, 1)

        self.checkBox = QCheckBox(self.ea_reportmerge_bases_sub3frame)
        self.checkBox.setObjectName(u"checkBox")

        self.ea_reportmerge_bases_GLayout.addWidget(self.checkBox, 2, 0, 1, 1)

        self.checkBox_2 = QCheckBox(self.ea_reportmerge_bases_sub3frame)
        self.checkBox_2.setObjectName(u"checkBox_2")

        self.ea_reportmerge_bases_GLayout.addWidget(self.checkBox_2, 3, 0, 1, 1)

        self.checkBox_3 = QCheckBox(self.ea_reportmerge_bases_sub3frame)
        self.checkBox_3.setObjectName(u"checkBox_3")

        self.ea_reportmerge_bases_GLayout.addWidget(self.checkBox_3, 1, 1, 1, 1)

        self.checkBox_11 = QCheckBox(self.ea_reportmerge_bases_sub3frame)
        self.checkBox_11.setObjectName(u"checkBox_11")

        self.ea_reportmerge_bases_GLayout.addWidget(self.checkBox_11, 4, 0, 1, 1)

        self.checkBox_12 = QCheckBox(self.ea_reportmerge_bases_sub3frame)
        self.checkBox_12.setObjectName(u"checkBox_12")

        self.ea_reportmerge_bases_GLayout.addWidget(self.checkBox_12, 4, 1, 1, 1)


        self.ea_reportmerge_sub2frame_GLayout.addWidget(self.ea_reportmerge_bases_sub3frame, 2, 0, 1, 1)

        self.ea_reportmerge_reporttypes_sub3frame = QFrame(self.ea_reportmerge_sub2frame)
        self.ea_reportmerge_reporttypes_sub3frame.setObjectName(u"ea_reportmerge_reporttypes_sub3frame")
        self.ea_reportmerge_reporttypes_sub3frame.setFrameShape(QFrame.Shape.NoFrame)
        self.ea_reportmerge_reporttypes_sub3frame.setFrameShadow(QFrame.Shadow.Raised)
        self.ea_reportmerge_reporttypes_GLayout = QGridLayout(self.ea_reportmerge_reporttypes_sub3frame)
        self.ea_reportmerge_reporttypes_GLayout.setObjectName(u"ea_reportmerge_reporttypes_GLayout")
        self.ea_reportmerge_reporttypes_PVLCP_checkbox = QCheckBox(self.ea_reportmerge_reporttypes_sub3frame)
        self.ea_reportmerge_reporttypes_PVLCP_checkbox.setObjectName(u"ea_reportmerge_reporttypes_PVLCP_checkbox")

        self.ea_reportmerge_reporttypes_GLayout.addWidget(self.ea_reportmerge_reporttypes_PVLCP_checkbox, 1, 0, 1, 1)

        self.label_2 = QLabel(self.ea_reportmerge_reporttypes_sub3frame)
        self.label_2.setObjectName(u"label_2")

        self.ea_reportmerge_reporttypes_GLayout.addWidget(self.label_2, 0, 0, 1, 1)

        self.ea_reportmerge_reporttypes_PVearnings_checkbox = QCheckBox(self.ea_reportmerge_reporttypes_sub3frame)
        self.ea_reportmerge_reporttypes_PVearnings_checkbox.setObjectName(u"ea_reportmerge_reporttypes_PVearnings_checkbox")

        self.ea_reportmerge_reporttypes_GLayout.addWidget(self.ea_reportmerge_reporttypes_PVearnings_checkbox, 2, 0, 1, 1)


        self.ea_reportmerge_sub2frame_GLayout.addWidget(self.ea_reportmerge_reporttypes_sub3frame, 0, 1, 1, 1)

        self.ea_reportmerge_taxstatus_sub3frame = QFrame(self.ea_reportmerge_sub2frame)
        self.ea_reportmerge_taxstatus_sub3frame.setObjectName(u"ea_reportmerge_taxstatus_sub3frame")
        self.ea_reportmerge_taxstatus_sub3frame.setFrameShape(QFrame.Shape.NoFrame)
        self.ea_reportmerge_taxstatus_sub3frame.setFrameShadow(QFrame.Shadow.Raised)
        self.ea_reportmerge_taxstatus_GLayout = QGridLayout(self.ea_reportmerge_taxstatus_sub3frame)
        self.ea_reportmerge_taxstatus_GLayout.setObjectName(u"ea_reportmerge_taxstatus_GLayout")
        self.ea_reportmerge_taxstatus_checkbox = QCheckBox(self.ea_reportmerge_taxstatus_sub3frame)
        self.ea_reportmerge_taxstatus_checkbox.setObjectName(u"ea_reportmerge_taxstatus_checkbox")

        self.ea_reportmerge_taxstatus_GLayout.addWidget(self.ea_reportmerge_taxstatus_checkbox, 1, 0, 1, 1)

        self.ea_reportmerge_taxstatus_label = QLabel(self.ea_reportmerge_taxstatus_sub3frame)
        self.ea_reportmerge_taxstatus_label.setObjectName(u"ea_reportmerge_taxstatus_label")

        self.ea_reportmerge_taxstatus_GLayout.addWidget(self.ea_reportmerge_taxstatus_label, 0, 0, 1, 1)


        self.ea_reportmerge_sub2frame_GLayout.addWidget(self.ea_reportmerge_taxstatus_sub3frame, 3, 0, 1, 1)

        self.ea_reportmerge_projectiontype_sub3frame = QFrame(self.ea_reportmerge_sub2frame)
        self.ea_reportmerge_projectiontype_sub3frame.setObjectName(u"ea_reportmerge_projectiontype_sub3frame")
        self.ea_reportmerge_projectiontype_sub3frame.setFrameShape(QFrame.Shape.NoFrame)
        self.ea_reportmerge_projectiontype_sub3frame.setFrameShadow(QFrame.Shadow.Raised)
        self.ea_reportmerge_projectiontype_GLayout = QGridLayout(self.ea_reportmerge_projectiontype_sub3frame)
        self.ea_reportmerge_projectiontype_GLayout.setObjectName(u"ea_reportmerge_projectiontype_GLayout")
        self.ea_reportmerge_projectiontype_label = QLabel(self.ea_reportmerge_projectiontype_sub3frame)
        self.ea_reportmerge_projectiontype_label.setObjectName(u"ea_reportmerge_projectiontype_label")
        self.ea_reportmerge_projectiontype_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.ea_reportmerge_projectiontype_GLayout.addWidget(self.ea_reportmerge_projectiontype_label, 0, 0, 1, 1)

        self.ea_reportmerge_projectiontype_combobox = QComboBox(self.ea_reportmerge_projectiontype_sub3frame)
        self.ea_reportmerge_projectiontype_combobox.setObjectName(u"ea_reportmerge_projectiontype_combobox")

        self.ea_reportmerge_projectiontype_GLayout.addWidget(self.ea_reportmerge_projectiontype_combobox, 1, 0, 1, 1)


        self.ea_reportmerge_sub2frame_GLayout.addWidget(self.ea_reportmerge_projectiontype_sub3frame, 0, 0, 1, 1)

        self.frame_8 = QFrame(self.ea_reportmerge_sub2frame)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_8 = QGridLayout(self.frame_8)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.checkBox_8 = QCheckBox(self.frame_8)
        self.checkBox_8.setObjectName(u"checkBox_8")
        self.checkBox_8.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self.gridLayout_8.addWidget(self.checkBox_8, 1, 0, 1, 1)

        self.label_8 = QLabel(self.frame_8)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_8.addWidget(self.label_8, 0, 0, 1, 1)


        self.ea_reportmerge_sub2frame_GLayout.addWidget(self.frame_8, 3, 1, 1, 1)


        self.ea_reportmerge_GLayout.addWidget(self.ea_reportmerge_sub2frame, 1, 0, 1, 1)

        self.ea_reportmerge_label = QLabel(self.ea_reportmerge_frame)
        self.ea_reportmerge_label.setObjectName(u"ea_reportmerge_label")
        self.ea_reportmerge_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.ea_reportmerge_GLayout.addWidget(self.ea_reportmerge_label, 0, 0, 1, 1)

        self.ea_reportmerge_button = QPushButton(self.ea_reportmerge_frame)
        self.ea_reportmerge_button.setObjectName(u"ea_reportmerge_button")

        self.ea_reportmerge_GLayout.addWidget(self.ea_reportmerge_button, 2, 0, 1, 1)

        self.ea_reportmerge_GLayout.setRowStretch(0, 1)
        self.ea_reportmerge_GLayout.setRowStretch(1, 10)

        self.ea_CentralWidget_GLayout.addWidget(self.ea_reportmerge_frame, 1, 2, 1, 1)

        self.ea_CentralWidget_label_frame = QFrame(self.ea_CentralWidget_frame)
        self.ea_CentralWidget_label_frame.setObjectName(u"ea_CentralWidget_label_frame")
        self.ea_CentralWidget_label_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.ea_CentralWidget_label_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.ea_CentralWidget_label_VLayout = QVBoxLayout(self.ea_CentralWidget_label_frame)
        self.ea_CentralWidget_label_VLayout.setSpacing(0)
        self.ea_CentralWidget_label_VLayout.setObjectName(u"ea_CentralWidget_label_VLayout")
        self.ea_CentralWidget_label = QLabel(self.ea_CentralWidget_label_frame)
        self.ea_CentralWidget_label.setObjectName(u"ea_CentralWidget_label")
        self.ea_CentralWidget_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.ea_CentralWidget_label_VLayout.addWidget(self.ea_CentralWidget_label)


        self.ea_CentralWidget_GLayout.addWidget(self.ea_CentralWidget_label_frame, 0, 0, 1, 3)

        self.ea_CentralWidget_GLayout.setColumnStretch(0, 1)

        self.ea_CentralWidget_HLayout.addWidget(self.ea_CentralWidget_frame)

        self.ea_MainWindow.setCentralWidget(self.ea_CentralWidget)

        self.retranslateUi()

        QMetaObject.connectSlotsByName(self.ea_MainWindow)
    # setupUi

    def retranslateUi(self):
        self.ea_MainWindow.setWindowTitle(QCoreApplication.translate("ea_MainWindow", u"EconLightning", None))
        self.ea_setupcase_label.setText(QCoreApplication.translate("ea_MainWindow", u"New Case Set Up", None))
        self.ea_setupcase_OFFSelect_button.setText(QCoreApplication.translate("ea_MainWindow", u"", None))
        self.ea_setupcase_selectedOFF_label.setText(QCoreApplication.translate("ea_MainWindow", u"TextLabel", None))
        self.ea_setupcase_createcase_button.setText(QCoreApplication.translate("ea_MainWindow", u"Create New Case", None))
        self.label_4.setText(QCoreApplication.translate("ea_MainWindow", u"TextLabel", None))
        self.checkBox_4.setText(QCoreApplication.translate("ea_MainWindow", u"CheckBox", None))
        self.ea_reportmerge_referencetype_label.setText(QCoreApplication.translate("ea_MainWindow", u"Reference Date", None))
        self.checkBox_6.setText(QCoreApplication.translate("ea_MainWindow", u"CheckBox", None))
        self.label_6.setText(QCoreApplication.translate("ea_MainWindow", u"TextLabel", None))
        self.checkBox_9.setText(QCoreApplication.translate("ea_MainWindow", u"Credit 2", None))
        self.ea_reportmerge_base1_checkbox.setText(QCoreApplication.translate("ea_MainWindow", u"Base 1", None))
        self.checkBox_10.setText(QCoreApplication.translate("ea_MainWindow", u"Credit 3", None))
        self.ea_reportmerge_bases_label.setText(QCoreApplication.translate("ea_MainWindow", u"Relevant Base(s) & Credits", None))
        self.checkBox.setText(QCoreApplication.translate("ea_MainWindow", u"Base 2", None))
        self.checkBox_2.setText(QCoreApplication.translate("ea_MainWindow", u"Base 3", None))
        self.checkBox_3.setText(QCoreApplication.translate("ea_MainWindow", u"Credit 1", None))
        self.checkBox_11.setText(QCoreApplication.translate("ea_MainWindow", u"Meals", None))
        self.checkBox_12.setText(QCoreApplication.translate("ea_MainWindow", u"CheckBox", None))
        self.ea_reportmerge_reporttypes_PVLCP_checkbox.setText(QCoreApplication.translate("ea_MainWindow", u"PVLCP", None))
        self.label_2.setText(QCoreApplication.translate("ea_MainWindow", u"Selected Templates", None))
        self.ea_reportmerge_reporttypes_PVearnings_checkbox.setText(QCoreApplication.translate("ea_MainWindow", u"PV Earnings", None))
        self.ea_reportmerge_taxstatus_checkbox.setText(QCoreApplication.translate("ea_MainWindow", u"Taxed", None))
        self.ea_reportmerge_taxstatus_label.setText(QCoreApplication.translate("ea_MainWindow", u"Tax Status", None))
        self.ea_reportmerge_projectiontype_label.setText(QCoreApplication.translate("ea_MainWindow", u"Earnings Projection", None))
        self.checkBox_8.setText(QCoreApplication.translate("ea_MainWindow", u"CheckBox", None))
        self.label_8.setText(QCoreApplication.translate("ea_MainWindow", u"TextLabel", None))
        self.ea_reportmerge_label.setText(QCoreApplication.translate("ea_MainWindow", u"Report Merge", None))
        self.ea_reportmerge_button.setText(QCoreApplication.translate("ea_MainWindow", u"Merge", None))
        self.ea_CentralWidget_label.setText(QCoreApplication.translate("ea_MainWindow", u"EconLightning", None))
    # retranslateUi

