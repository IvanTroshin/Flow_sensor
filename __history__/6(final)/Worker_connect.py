from pyqtgraph import PlotWidget
import numpy as np
import random
import propar
from gui.qt_io import Ui_MainWindow
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtBoundSignal
from PyQt5 import QtWidgets
import time
from datetime import datetime
import gc  # Очистка пямяти


class Flow_worker_class(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal()

    res_signal = pyqtSignal(float, str, float, float)  # Для хранения успешного или неуспешного рез-та точки

    COM_port_signal = pyqtSignal(str, QtWidgets.QTextEdit,
                                 QtWidgets.QDoubleSpinBox,
                                 QtWidgets.QLineEdit,
                                 QtWidgets.QSlider,
                                 QtWidgets.QDoubleSpinBox,
                                 QtWidgets.QProgressBar,
                                 QtWidgets.QLineEdit,
                                 QtWidgets.QLineEdit,
                                 int)

    name_flow_signal = pyqtSignal(str)  # Для имени
    write_textEdit_signal = pyqtSignal(str, QtWidgets.QTextEdit)  # Для вывода в приложение
    chenge_SpinBox_signal = pyqtSignal(QtWidgets.QDoubleSpinBox, float, float)  # бины в ввод
    lineEdit_temperature_singal = pyqtSignal(str, float, QtWidgets.QLineEdit)  # Запись температуры
    chenge_val_signal = pyqtSignal(int)
    chenger_progressBar_lineEdit_value_signal = pyqtSignal(float, float,
                                                           QtWidgets.QProgressBar,
                                                           QtWidgets.QLineEdit)  # Изменение в статус буре и в тексте
    change_to_zero_signal = pyqtSignal()
    stop_QTheath_in_worker_signal = pyqtSignal()
    alarm_single = pyqtSignal(str, QtWidgets.QTextEdit) # Если газ закончился, то есть расход на клапоне другой сем в програме

    def run_master(self, COM_port,
                   textEdit_here,
                   doubleSpinBox_value_here,
                   lineEdit_temperature_here,
                   verticalSlider_here,
                   doubleSpinBox_persent_here,
                   progressBar_here,
                   lineEdit_value_here,
                   lineEdit_gas_here,
                   val_chang):
        self.COM_port = COM_port
        self.doubleSpinBox_value_here = doubleSpinBox_value_here
        self.lineEdit_temperature_here = lineEdit_temperature_here
        self.textEdit_here = textEdit_here
        self.verticalSlider_here = verticalSlider_here
        self.doubleSpinBox_persent_here = doubleSpinBox_persent_here
        self.progressBar_here = progressBar_here
        self.lineEdit_value_here = lineEdit_value_here
        self.lineEdit_gas_here = lineEdit_gas_here
        self.value_scrolbar_here = val_chang # Значение расхода в программе

        self.run_master_progress() # все процесы для запуска расходомера

    def run_master_progress(self):
        self.master_flow = propar.master(self.COM_port, 38400)

        date_now = datetime.now().strftime("%d_%m_%Y")
        self.write_textEdit_signal.emit(f"\nDate {date_now}\n", self.textEdit_here)
        time_now = str(datetime.now().strftime("%X"))
        self.write_textEdit_signal.emit(f"Time {time_now}\n", self.textEdit_here)
        self.write_textEdit_signal.emit(f"The Master runs\n ", self.textEdit_here)

        # Get nodes on the network
        self.nodes = self.master_flow.get_nodes()

        # Read the usertag of all nodes
        for node in self.nodes:
            user_tag = self.master_flow.read(node['address'], 113, 6, propar.PP_TYPE_STRING)
            print(node['address'])
            print(user_tag)
            # {'proc_nr': 1, 'parm_nr': 17, 'parm_type': propar.PP_TYPE_STRING},  # FLUID NAME
            name_fluid = self.master_flow.read(node['address'], 1, 17, propar.PP_TYPE_STRING)  # FLUID NAME

            print(name_fluid)
            self.write_textEdit_signal.emit(f"{name_fluid}" + "\n", self.textEdit_here)

            user_tag = self.master_flow.read(node['address'], 1, 1, propar.PP_TYPE_INT16)
            print(f"SETPOINT {user_tag}")

            user_tag = self.master_flow.write(node['address'], 1, 4, propar.PP_TYPE_INT8, 0)  # BUS/RS232
            print(user_tag)
            self.write_textEdit_signal.emit(f"Control mode {user_tag}" + "\n", self.textEdit_here)

            self.CAPACITY_100 = self.master_flow.read(self.nodes[0]['address'], 1, 13,
                                                      propar.PP_TYPE_FLOAT)  # CAPACITY 100%
            self.CAPACITY_000 = self.master_flow.read(self.nodes[0]['address'], 33, 22,
                                                      propar.PP_TYPE_FLOAT)  # CAPACITY 0%

            self.chenge_SpinBox_signal.emit(self.doubleSpinBox_value_here, self.CAPACITY_100, self.CAPACITY_000)

    def chenger_setpoint(self, val_chang):
        self.value_scrolbar_here = val_chang
        # Номер узла self.nodes[0]['address'] не знаю зачем он
        self.master_flow.write(self.nodes[0]['address'], 1, 1, propar.PP_TYPE_INT16, val_chang)
        user_tag = self.master_flow.read(self.nodes[0]['address'], 1, 1, propar.PP_TYPE_INT16)
        print(f"SETPOINT {user_tag}")

    def read_data(self):

        # Проверки на ошибки
        user_tag = self.master_flow.read(self.nodes[0]['address'], 1, 1, propar.PP_TYPE_INT16)  # SetPoint
        # for k in range(3):
        #     if user_tag is None:
        #         print(f"Problem None №{k}")
        #         self.close_and_run_master()
        #         time.sleep(0.1)
        #         self.chenger_setpoint(self.value_scrolbar_here)
        #     else:
        #         break

        user_tag = self.master_flow.read(self.nodes[0]['address'], 1, 1, propar.PP_TYPE_INT16)  # SetPoint
        if self.value_scrolbar_here != user_tag:
            self.chenger_setpoint(self.value_scrolbar_here)
            if self.value_scrolbar_here != user_tag:
                self.close_and_run_master()
                time.sleep(0.1)
                self.chenger_setpoint(self.value_scrolbar_here)

        F_MEASURE_here = self.master_flow.read(self.nodes[0]['address'], 33, 0,
                                               propar.PP_TYPE_FLOAT)  # F_MEASURE_Thread
        name_f = self.master_flow.read(self.nodes[0]['address'],
                                       1, 17, propar.PP_TYPE_STRING)  # FLUID NAME

        buff_v = self.value_scrolbar_here/32000*(self.CAPACITY_100-self.CAPACITY_000) + self.CAPACITY_000

        temper_f = self.master_flow.read(self.nodes[0]['address'], 33, 7,
                                         propar.PP_TYPE_FLOAT)  # Температура

        self.res_signal.emit(F_MEASURE_here, name_f, buff_v, temper_f)
        # self.y_buff = F_MEASURE_here  # Новая точка



        self.lineEdit_temperature_singal.emit(name_f, temper_f, self.lineEdit_temperature_here)
        self.chenger_progressBar_lineEdit_value_signal.emit(F_MEASURE_here, self.CAPACITY_100,
                                                            self.progressBar_here,
                                                            self.lineEdit_value_here)

        if F_MEASURE_here - (F_MEASURE_here+0.01)/10 > buff_v \
                or F_MEASURE_here + (F_MEASURE_here+0.01)/10 < buff_v:
            self.alarm_single.emit("Gas is running out\n", self.textEdit_here)

    def change_to_zero(self):
        values = self.master_flow.write(self.nodes[0]['address'], 1, 1, propar.PP_TYPE_INT16, 0)
        print(values)
        self.master_flow.stop()

    def close_and_run_master(self):
        print("close_and_run_master")
        self.master_flow.propar.stop()
        self.run_master_progress()

    def stop_QTheath_in_worker(self):
        self.finished.emit()

    def __init__(self):
        super(Flow_worker_class, self).__init__()
        self.value_scrolbar_here = None # расход выставленный в программе
        self.nodes = None
        self.master_flow = None
        self.COM_port = None
        self.doubleSpinBox_value_here = None
        self.lineEdit_temperature_here = None
        self.textEdit_here = None
        self.verticalSlider_here = None
        self.doubleSpinBox_persent_here = None
        self.progressBar_here = None
        self.lineEdit_value_here = None
        self.lineEdit_gas_here = None
        self.CAPACITY_000 = None
        self.CAPACITY_100 = None
