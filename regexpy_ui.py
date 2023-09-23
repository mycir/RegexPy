# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'regexpy.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QPlainTextEdit, QSizePolicy,
    QSpacerItem, QSplitter, QTextEdit, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(800, 600)
        Form.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(-1, -1, -1, 7)
        self.horizontalLayoutStatus = QHBoxLayout()
        self.horizontalLayoutStatus.setObjectName(u"horizontalLayoutStatus")
        self.labelMatches = QLabel(Form)
        self.labelMatches.setObjectName(u"labelMatches")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelMatches.sizePolicy().hasHeightForWidth())
        self.labelMatches.setSizePolicy(sizePolicy)
        self.labelMatches.setMaximumSize(QSize(65, 20))

        self.horizontalLayoutStatus.addWidget(self.labelMatches)

        self.labelMatchesCount = QLabel(Form)
        self.labelMatchesCount.setObjectName(u"labelMatchesCount")
        sizePolicy.setHeightForWidth(self.labelMatchesCount.sizePolicy().hasHeightForWidth())
        self.labelMatchesCount.setSizePolicy(sizePolicy)

        self.horizontalLayoutStatus.addWidget(self.labelMatchesCount)

        self.labelMatch = QLabel(Form)
        self.labelMatch.setObjectName(u"labelMatch")

        self.horizontalLayoutStatus.addWidget(self.labelMatch)

        self.labelGroups = QLabel(Form)
        self.labelGroups.setObjectName(u"labelGroups")
        sizePolicy.setHeightForWidth(self.labelGroups.sizePolicy().hasHeightForWidth())
        self.labelGroups.setSizePolicy(sizePolicy)
        self.labelGroups.setMinimumSize(QSize(0, 0))
        self.labelGroups.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayoutStatus.addWidget(self.labelGroups)

        self.labelGroupsIndex = QLabel(Form)
        self.labelGroupsIndex.setObjectName(u"labelGroupsIndex")
        sizePolicy.setHeightForWidth(self.labelGroupsIndex.sizePolicy().hasHeightForWidth())
        self.labelGroupsIndex.setSizePolicy(sizePolicy)

        self.horizontalLayoutStatus.addWidget(self.labelGroupsIndex, 0, Qt.AlignLeft)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.horizontalLayoutStatus.addItem(self.horizontalSpacer)

        self.frameButtons = QFrame(Form)
        self.frameButtons.setObjectName(u"frameButtons")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frameButtons.sizePolicy().hasHeightForWidth())
        self.frameButtons.setSizePolicy(sizePolicy1)
        self.frameButtons.setMaximumSize(QSize(120, 16777215))
        self.frameButtons.setFrameShape(QFrame.NoFrame)
        self.frameButtons.setFrameShadow(QFrame.Raised)

        self.horizontalLayoutStatus.addWidget(self.frameButtons)


        self.gridLayout.addLayout(self.horizontalLayoutStatus, 1, 0, 1, 1)

        self.splitter = QSplitter(Form)
        self.splitter.setObjectName(u"splitter")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy2)
        self.splitter.setOrientation(Qt.Vertical)
        self.plainTextEditRegex = QPlainTextEdit(self.splitter)
        self.plainTextEditRegex.setObjectName(u"plainTextEditRegex")
        sizePolicy2.setHeightForWidth(self.plainTextEditRegex.sizePolicy().hasHeightForWidth())
        self.plainTextEditRegex.setSizePolicy(sizePolicy2)
        self.plainTextEditRegex.setMinimumSize(QSize(0, 50))
        self.plainTextEditRegex.setMaximumSize(QSize(16777215, 16777215))
        self.plainTextEditRegex.setBaseSize(QSize(0, 80))
        self.plainTextEditRegex.setTabChangesFocus(True)
        self.splitter.addWidget(self.plainTextEditRegex)
        self.frameOptions = QFrame(self.splitter)
        self.frameOptions.setObjectName(u"frameOptions")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.frameOptions.sizePolicy().hasHeightForWidth())
        self.frameOptions.setSizePolicy(sizePolicy3)
        self.frameOptions.setMinimumSize(QSize(0, 42))
        self.frameOptions.setMaximumSize(QSize(16777215, 42))
        self.frameOptions.setFrameShape(QFrame.StyledPanel)
        self.frameOptions.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frameOptions)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayoutOptions = QHBoxLayout()
#ifndef Q_OS_MAC
        self.horizontalLayoutOptions.setSpacing(-1)
#endif
        self.horizontalLayoutOptions.setObjectName(u"horizontalLayoutOptions")
        self.checkBoxAscii = QCheckBox(self.frameOptions)
        self.checkBoxAscii.setObjectName(u"checkBoxAscii")

        self.horizontalLayoutOptions.addWidget(self.checkBoxAscii, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.checkBoxIgnoreCase = QCheckBox(self.frameOptions)
        self.checkBoxIgnoreCase.setObjectName(u"checkBoxIgnoreCase")

        self.horizontalLayoutOptions.addWidget(self.checkBoxIgnoreCase, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.checkBoxMultiline = QCheckBox(self.frameOptions)
        self.checkBoxMultiline.setObjectName(u"checkBoxMultiline")

        self.horizontalLayoutOptions.addWidget(self.checkBoxMultiline, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.checkBoxDotAll = QCheckBox(self.frameOptions)
        self.checkBoxDotAll.setObjectName(u"checkBoxDotAll")

        self.horizontalLayoutOptions.addWidget(self.checkBoxDotAll, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.checkBoxVerbose = QCheckBox(self.frameOptions)
        self.checkBoxVerbose.setObjectName(u"checkBoxVerbose")
        self.checkBoxVerbose.setMinimumSize(QSize(0, 0))

        self.horizontalLayoutOptions.addWidget(self.checkBoxVerbose, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.horizontalLayout_3.addLayout(self.horizontalLayoutOptions)

        self.splitter.addWidget(self.frameOptions)
        self.textEditSample = QTextEdit(self.splitter)
        self.textEditSample.setObjectName(u"textEditSample")
        self.textEditSample.setMinimumSize(QSize(0, 258))
        self.textEditSample.setTabChangesFocus(True)
        self.splitter.addWidget(self.textEditSample)

        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)

        QWidget.setTabOrder(self.plainTextEditRegex, self.checkBoxAscii)
        QWidget.setTabOrder(self.checkBoxAscii, self.checkBoxIgnoreCase)
        QWidget.setTabOrder(self.checkBoxIgnoreCase, self.checkBoxMultiline)
        QWidget.setTabOrder(self.checkBoxMultiline, self.checkBoxDotAll)
        QWidget.setTabOrder(self.checkBoxDotAll, self.checkBoxVerbose)
        QWidget.setTabOrder(self.checkBoxVerbose, self.textEditSample)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"RegexPy", None))
        self.labelMatches.setText(QCoreApplication.translate("Form", u"Matches:", None))
        self.labelMatchesCount.setText(QCoreApplication.translate("Form", u"0", None))
        self.labelMatch.setText(QCoreApplication.translate("Form", u"[0]", None))
        self.labelGroups.setText(QCoreApplication.translate("Form", u"Group:", None))
        self.labelGroupsIndex.setText(QCoreApplication.translate("Form", u"0", None))
        self.plainTextEditRegex.setPlaceholderText(QCoreApplication.translate("Form", u"Enter regular expression here", None))
        self.checkBoxAscii.setText(QCoreApplication.translate("Form", u"ASCII", None))
        self.checkBoxIgnoreCase.setText(QCoreApplication.translate("Form", u"IGNORECASE", None))
        self.checkBoxMultiline.setText(QCoreApplication.translate("Form", u"MULTILINE", None))
        self.checkBoxDotAll.setText(QCoreApplication.translate("Form", u"DOTALL", None))
        self.checkBoxVerbose.setText(QCoreApplication.translate("Form", u"VERBOSE", None))
        self.textEditSample.setPlaceholderText(QCoreApplication.translate("Form", u"Enter or paste sample text here, or load from file", None))
    # retranslateUi

