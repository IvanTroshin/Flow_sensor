# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt_io.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1207, 891)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setMinimumSize(QtCore.QSize(69, 0))
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout.addWidget(self.comboBox)
        self.pushButton_Start_1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Start_1.setObjectName("pushButton_Start_1")
        self.horizontalLayout.addWidget(self.pushButton_Start_1)
        self.pushButton_stop_1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_stop_1.setEnabled(False)
        self.pushButton_stop_1.setObjectName("pushButton_stop_1")
        self.horizontalLayout.addWidget(self.pushButton_stop_1)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.horizontalLayout_4.addLayout(self.verticalLayout_5)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_2.sizePolicy().hasHeightForWidth())
        self.comboBox_2.setSizePolicy(sizePolicy)
        self.comboBox_2.setMinimumSize(QtCore.QSize(69, 0))
        self.comboBox_2.setCurrentText("")
        self.comboBox_2.setObjectName("comboBox_2")
        self.horizontalLayout_3.addWidget(self.comboBox_2)
        self.pushButton_Start_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Start_2.setObjectName("pushButton_Start_2")
        self.horizontalLayout_3.addWidget(self.pushButton_Start_2)
        self.pushButton_stop_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_stop_2.setEnabled(False)
        self.pushButton_stop_2.setObjectName("pushButton_stop_2")
        self.horizontalLayout_3.addWidget(self.pushButton_stop_2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4.addLayout(self.verticalLayout_4)
        self.verticalLayout_6.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.lineEdit_temperature_Mix = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_temperature_Mix.sizePolicy().hasHeightForWidth())
        self.lineEdit_temperature_Mix.setSizePolicy(sizePolicy)
        self.lineEdit_temperature_Mix.setFrame(False)
        self.lineEdit_temperature_Mix.setReadOnly(True)
        self.lineEdit_temperature_Mix.setObjectName("lineEdit_temperature_Mix")
        self.horizontalLayout_10.addWidget(self.lineEdit_temperature_Mix)
        self.verticalSlider_Mix = QtWidgets.QSlider(self.centralwidget)
        self.verticalSlider_Mix.setEnabled(False)
        self.verticalSlider_Mix.setMaximum(100000)
        self.verticalSlider_Mix.setOrientation(QtCore.Qt.Horizontal)
        self.verticalSlider_Mix.setObjectName("verticalSlider_Mix")
        self.horizontalLayout_10.addWidget(self.verticalSlider_Mix)
        self.doubleSpinBox_value_Mix = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox_value_Mix.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.doubleSpinBox_value_Mix.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_value_Mix.setSizePolicy(sizePolicy)
        self.doubleSpinBox_value_Mix.setMinimumSize(QtCore.QSize(50, 0))
        self.doubleSpinBox_value_Mix.setDecimals(0)
        self.doubleSpinBox_value_Mix.setMaximum(100.0)
        self.doubleSpinBox_value_Mix.setSingleStep(1.0)
        self.doubleSpinBox_value_Mix.setObjectName("doubleSpinBox_value_Mix")
        self.horizontalLayout_10.addWidget(self.doubleSpinBox_value_Mix)
        self.lineEdit_value_ln_h_5 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_value_ln_h_5.setMaximumSize(QtCore.QSize(30, 16777215))
        self.lineEdit_value_ln_h_5.setFrame(False)
        self.lineEdit_value_ln_h_5.setReadOnly(True)
        self.lineEdit_value_ln_h_5.setObjectName("lineEdit_value_ln_h_5")
        self.horizontalLayout_10.addWidget(self.lineEdit_value_ln_h_5)
        self.verticalLayout_6.addLayout(self.horizontalLayout_10)
        self.verticalLayout_7.addLayout(self.verticalLayout_6)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lineEdit_gas_1 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_gas_1.setFrame(False)
        self.lineEdit_gas_1.setReadOnly(True)
        self.lineEdit_gas_1.setObjectName("lineEdit_gas_1")
        self.verticalLayout_2.addWidget(self.lineEdit_gas_1)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalSlider_1 = QtWidgets.QSlider(self.centralwidget)
        self.verticalSlider_1.setEnabled(False)
        self.verticalSlider_1.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.verticalSlider_1.setStyleSheet("QSlider::handle:vertical\n"
" {\n"
"    height: 10px;\n"
"    background: rgb(255, 69, 0);\n"
"    margin: 0 -4px; /* expand outside the groove */\n"
"}\n"
"")
        self.verticalSlider_1.setMaximum(32000)
        self.verticalSlider_1.setProperty("value", 0)
        self.verticalSlider_1.setSliderPosition(0)
        self.verticalSlider_1.setTracking(False)
        self.verticalSlider_1.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_1.setTickPosition(QtWidgets.QSlider.NoTicks)
        self.verticalSlider_1.setTickInterval(0)
        self.verticalSlider_1.setObjectName("verticalSlider_1")
        self.horizontalLayout_6.addWidget(self.verticalSlider_1)
        self.progressBar_1 = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar_1.setMinimumSize(QtCore.QSize(30, 0))
        self.progressBar_1.setStyleSheet("QProgressBar\n"
"{\n"
"    border-radius : 8px;\n"
"    background-color: rgb(150, 150, 150);\n"
"}\n"
"\n"
"QProgressBar::chunk\n"
"{\n"
"    border-radius : 8px;\n"
"    background-color: rgb(255, 69, 0);\n"
"}")
        self.progressBar_1.setProperty("value", 0)
        self.progressBar_1.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar_1.setTextVisible(True)
        self.progressBar_1.setOrientation(QtCore.Qt.Vertical)
        self.progressBar_1.setInvertedAppearance(False)
        self.progressBar_1.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.progressBar_1.setObjectName("progressBar_1")
        self.horizontalLayout_6.addWidget(self.progressBar_1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.doubleSpinBox_persent_1 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox_persent_1.setEnabled(False)
        self.doubleSpinBox_persent_1.setDecimals(2)
        self.doubleSpinBox_persent_1.setMaximum(100.0)
        self.doubleSpinBox_persent_1.setSingleStep(0.1)
        self.doubleSpinBox_persent_1.setObjectName("doubleSpinBox_persent_1")
        self.horizontalLayout_8.addWidget(self.doubleSpinBox_persent_1)
        self.lineEdit_persent_1 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_persent_1.setEnabled(True)
        self.lineEdit_persent_1.setMaximumSize(QtCore.QSize(20, 16777215))
        self.lineEdit_persent_1.setMaxLength(10)
        self.lineEdit_persent_1.setFrame(False)
        self.lineEdit_persent_1.setReadOnly(True)
        self.lineEdit_persent_1.setObjectName("lineEdit_persent_1")
        self.horizontalLayout_8.addWidget(self.lineEdit_persent_1)
        self.doubleSpinBox_value_1 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox_value_1.setEnabled(False)
        self.doubleSpinBox_value_1.setDecimals(3)
        self.doubleSpinBox_value_1.setSingleStep(0.1)
        self.doubleSpinBox_value_1.setObjectName("doubleSpinBox_value_1")
        self.horizontalLayout_8.addWidget(self.doubleSpinBox_value_1)
        self.lineEdit_value_ln_h_1 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_value_ln_h_1.setEnabled(True)
        self.lineEdit_value_ln_h_1.setMaximumSize(QtCore.QSize(30, 16777215))
        self.lineEdit_value_ln_h_1.setFrame(False)
        self.lineEdit_value_ln_h_1.setReadOnly(True)
        self.lineEdit_value_ln_h_1.setObjectName("lineEdit_value_ln_h_1")
        self.horizontalLayout_8.addWidget(self.lineEdit_value_ln_h_1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.lineEdit_temperature_1 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_temperature_1.setEnabled(True)
        self.lineEdit_temperature_1.setFrame(False)
        self.lineEdit_temperature_1.setReadOnly(True)
        self.lineEdit_temperature_1.setObjectName("lineEdit_temperature_1")
        self.horizontalLayout_12.addWidget(self.lineEdit_temperature_1)
        self.lineEdit_value_1 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_value_1.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_value_1.sizePolicy().hasHeightForWidth())
        self.lineEdit_value_1.setSizePolicy(sizePolicy)
        self.lineEdit_value_1.setMaximumSize(QtCore.QSize(60, 16777215))
        self.lineEdit_value_1.setFrame(False)
        self.lineEdit_value_1.setReadOnly(True)
        self.lineEdit_value_1.setObjectName("lineEdit_value_1")
        self.horizontalLayout_12.addWidget(self.lineEdit_value_1)
        self.lineEdit_value_ln_h_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_value_ln_h_3.setEnabled(True)
        self.lineEdit_value_ln_h_3.setMaximumSize(QtCore.QSize(30, 16777215))
        self.lineEdit_value_ln_h_3.setFrame(False)
        self.lineEdit_value_ln_h_3.setReadOnly(True)
        self.lineEdit_value_ln_h_3.setObjectName("lineEdit_value_ln_h_3")
        self.horizontalLayout_12.addWidget(self.lineEdit_value_ln_h_3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_12)
        self.textEdit_1 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_1.setObjectName("textEdit_1")
        self.verticalLayout_2.addWidget(self.textEdit_1)
        self.horizontalLayout_14.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.lineEdit_gas_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_gas_2.setFrame(False)
        self.lineEdit_gas_2.setReadOnly(True)
        self.lineEdit_gas_2.setObjectName("lineEdit_gas_2")
        self.verticalLayout.addWidget(self.lineEdit_gas_2)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalSlider_2 = QtWidgets.QSlider(self.centralwidget)
        self.verticalSlider_2.setEnabled(False)
        self.verticalSlider_2.setStyleSheet("QSlider::handle:vertical\n"
" {\n"
"    height: 10px;\n"
"    background: rgb(0, 102, 255);\n"
"    margin: 0 -4px; /* expand outside the groove */\n"
"}\n"
"")
        self.verticalSlider_2.setMaximum(32000)
        self.verticalSlider_2.setProperty("value", 0)
        self.verticalSlider_2.setTracking(False)
        self.verticalSlider_2.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_2.setObjectName("verticalSlider_2")
        self.horizontalLayout_7.addWidget(self.verticalSlider_2)
        self.progressBar_2 = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar_2.setMinimumSize(QtCore.QSize(30, 0))
        self.progressBar_2.setStyleSheet("QProgressBar\n"
"{\n"
"    border-radius : 8px;\n"
"    background-color: rgb(150, 150, 150);\n"
"}\n"
"\n"
"QProgressBar::chunk\n"
"{\n"
"    border-radius : 8px;\n"
"    background-color: rgb(0, 102, 255);\n"
"}\n"
"")
        self.progressBar_2.setProperty("value", 0)
        self.progressBar_2.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar_2.setTextVisible(True)
        self.progressBar_2.setOrientation(QtCore.Qt.Vertical)
        self.progressBar_2.setInvertedAppearance(False)
        self.progressBar_2.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.progressBar_2.setObjectName("progressBar_2")
        self.horizontalLayout_7.addWidget(self.progressBar_2)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.doubleSpinBox_persent_2 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox_persent_2.setEnabled(False)
        self.doubleSpinBox_persent_2.setDecimals(2)
        self.doubleSpinBox_persent_2.setMaximum(100.0)
        self.doubleSpinBox_persent_2.setSingleStep(0.1)
        self.doubleSpinBox_persent_2.setObjectName("doubleSpinBox_persent_2")
        self.horizontalLayout_9.addWidget(self.doubleSpinBox_persent_2)
        self.lineEdit_persent_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_persent_2.setMaximumSize(QtCore.QSize(20, 16777215))
        self.lineEdit_persent_2.setMaxLength(10)
        self.lineEdit_persent_2.setFrame(False)
        self.lineEdit_persent_2.setReadOnly(True)
        self.lineEdit_persent_2.setObjectName("lineEdit_persent_2")
        self.horizontalLayout_9.addWidget(self.lineEdit_persent_2)
        self.doubleSpinBox_value_2 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox_value_2.setEnabled(False)
        self.doubleSpinBox_value_2.setDecimals(3)
        self.doubleSpinBox_value_2.setSingleStep(0.1)
        self.doubleSpinBox_value_2.setObjectName("doubleSpinBox_value_2")
        self.horizontalLayout_9.addWidget(self.doubleSpinBox_value_2)
        self.lineEdit_value_ln_h_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_value_ln_h_2.setMaximumSize(QtCore.QSize(30, 16777215))
        self.lineEdit_value_ln_h_2.setFrame(False)
        self.lineEdit_value_ln_h_2.setReadOnly(True)
        self.lineEdit_value_ln_h_2.setObjectName("lineEdit_value_ln_h_2")
        self.horizontalLayout_9.addWidget(self.lineEdit_value_ln_h_2)
        self.verticalLayout.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.lineEdit_temperature_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_temperature_2.setFrame(False)
        self.lineEdit_temperature_2.setReadOnly(True)
        self.lineEdit_temperature_2.setObjectName("lineEdit_temperature_2")
        self.horizontalLayout_13.addWidget(self.lineEdit_temperature_2)
        self.lineEdit_value_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_value_2.setMaximumSize(QtCore.QSize(60, 16777215))
        self.lineEdit_value_2.setFrame(False)
        self.lineEdit_value_2.setReadOnly(True)
        self.lineEdit_value_2.setObjectName("lineEdit_value_2")
        self.horizontalLayout_13.addWidget(self.lineEdit_value_2)
        self.lineEdit_value_ln_h_4 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_value_ln_h_4.setMaximumSize(QtCore.QSize(30, 16777215))
        self.lineEdit_value_ln_h_4.setFrame(False)
        self.lineEdit_value_ln_h_4.setReadOnly(True)
        self.lineEdit_value_ln_h_4.setObjectName("lineEdit_value_ln_h_4")
        self.horizontalLayout_13.addWidget(self.lineEdit_value_ln_h_4)
        self.verticalLayout.addLayout(self.horizontalLayout_13)
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setObjectName("textEdit_2")
        self.verticalLayout.addWidget(self.textEdit_2)
        self.horizontalLayout_14.addLayout(self.verticalLayout)
        self.verticalLayout_7.addLayout(self.horizontalLayout_14)
        self.horizontalLayout_5.addLayout(self.verticalLayout_7)
        self.graphicsView_FS_1 = PlotWidget(self.centralwidget)
        self.graphicsView_FS_1.setObjectName("graphicsView_FS_1")
        self.horizontalLayout_5.addWidget(self.graphicsView_FS_1)
        self.horizontalLayout_5.setStretch(0, 1)
        self.horizontalLayout_5.setStretch(1, 3)
        self.horizontalLayout_15.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_15.setStretch(0, 6)
        self.verticalLayout_3.addLayout(self.horizontalLayout_15)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pushButton_rerun_flow = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_rerun_flow.setEnabled(False)
        self.pushButton_rerun_flow.setObjectName("pushButton_rerun_flow")
        self.horizontalLayout_2.addWidget(self.pushButton_rerun_flow)
        self.pushButton_Close = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Close.setObjectName("pushButton_Close")
        self.horizontalLayout_2.addWidget(self.pushButton_Close)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1207, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionFind_com_port = QtWidgets.QAction(MainWindow)
        self.actionFind_com_port.setObjectName("actionFind_com_port")
        self.menuFile.addAction(self.actionFind_com_port)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_Start_1.setText(_translate("MainWindow", "Connect"))
        self.pushButton_stop_1.setText(_translate("MainWindow", "Disconnect"))
        self.pushButton_Start_2.setText(_translate("MainWindow", "Connect"))
        self.pushButton_stop_2.setText(_translate("MainWindow", "Disconnect"))
        self.lineEdit_temperature_Mix.setText(_translate("MainWindow", "   Ar 94% and CO2 6%"))
        self.lineEdit_value_ln_h_5.setText(_translate("MainWindow", "l/h"))
        self.progressBar_1.setFormat(_translate("MainWindow", "%p%"))
        self.lineEdit_persent_1.setText(_translate("MainWindow", "%"))
        self.lineEdit_value_ln_h_1.setText(_translate("MainWindow", "l/h"))
        self.lineEdit_value_1.setText(_translate("MainWindow", "505"))
        self.lineEdit_value_ln_h_3.setText(_translate("MainWindow", "l/h"))
        self.progressBar_2.setFormat(_translate("MainWindow", "%p%"))
        self.lineEdit_persent_2.setText(_translate("MainWindow", "%"))
        self.lineEdit_value_ln_h_2.setText(_translate("MainWindow", "l/h"))
        self.lineEdit_value_2.setText(_translate("MainWindow", "505"))
        self.lineEdit_value_ln_h_4.setText(_translate("MainWindow", "l/h"))
        self.pushButton_rerun_flow.setText(_translate("MainWindow", "ReRun"))
        self.pushButton_Close.setText(_translate("MainWindow", "Exit"))
        self.menuFile.setTitle(_translate("MainWindow", "Options "))
        self.actionFind_com_port.setText(_translate("MainWindow", "Find COM port"))
from pyqtgraph import PlotWidget