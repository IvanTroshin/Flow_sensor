from pyqtgraph import PlotWidget
import numpy as np
import random
import propar
from gui.qt_io import Ui_MainWindow
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5 import QtWidgets
import time
from datetime import datetime
import gc   # Очистка пямяти

class Flow_worker_class(QObject):

    finished = pyqtSignal()
    progress = pyqtSignal()
    progress_run_worker_signal = pyqtSignal()

    # graph_signal = pyqtSignal(list, list, int, list)
    new_point_m1_signal = pyqtSignal()
    if_nan_point_signal_m1 = pyqtSignal()

    COM_port_signal = pyqtSignal(str, QtWidgets.QTextEdit, QtWidgets.QDoubleSpinBox,
                                 QtWidgets.QLineEdit,
                                 QtWidgets.QSlider, QtWidgets.QDoubleSpinBox)

    name_flow_signal = pyqtSignal(str) # Для имени
    write_textEdit_signal = pyqtSignal(str, QtWidgets.QTextEdit) # Для вывода в приложение
    chenge_SpinBox_signal = pyqtSignal(QtWidgets.QDoubleSpinBox, float, float)  # бины в ввод
    lineEdit_temperature_singal = pyqtSignal(str, float, QtWidgets.QLineEdit) # Запись температуры

    exit_worker = False

    new_point_m1 = 0    # Точка на графике
    new_point_m2 = 0    # Точка на графике

    x_t_plot = list([])         # Для координат
    x_t_plot_name = list([])    # Для название координат (поставить время)
    y_main_plot_m1 = list([])   # Для расхода газа
    y_buff = 0                  # Для записи

    gas_consumption_m1 = 0      # Общий расход газа первого
    gas_consumption_m2 = 0      # Общий расход газа второго

    time_size = 60      # шприна по X
    # time_size = 24      # шприна по X # тест

    time_start_pro = 0      # Для определения разности времён
    time_stop_pro = 0
    X_time_1 = [0, 0]       # Время изменения

    time_start_pro = datetime.now()
    time_stop_pro = datetime.now()


    def run_master(self, COM_port, textEdit_here,
                   doubleSpinBox_value_here,
                   lineEdit_temperature_here, doubleSpinBox_persent_here):
        self.doubleSpinBox_persent_here = doubleSpinBox_value_here
        self.lineEdit_temperature_here = lineEdit_temperature_here
        self.textEdit_here = textEdit_here
        self.doubleSpinBox_persent_here = doubleSpinBox_persent_here

        self.master_flow = propar.master(COM_port, 38400)
        self.write_textEdit_signal.emit(f"The Master runs"+"\n", textEdit_here)

        # Get nodes on the network
        self.nodes = self.master_flow.get_nodes()

        # Read the usertag of all nodes
        for node in self.nodes:
            user_tag = self.master_flow.read(node['address'], 113, 6, propar.PP_TYPE_STRING)
            print(node['address'])
            print(user_tag)
            # {'proc_nr': 1, 'parm_nr': 17, 'parm_type': propar.PP_TYPE_STRING},  # FLUID NAME
            name_fluid = self.master_flow.read(node['address'], 1, 17, propar.PP_TYPE_STRING) # FLUID NAME

            print(name_fluid)
            self.write_textEdit_signal.emit(f"{name_fluid}" + "\n", textEdit_here)

            user_tag = self.master_flow.read(node['address'], 1, 1, propar.PP_TYPE_INT16)
            print(f"SETPOINT {user_tag}")

            user_tag = self.master_flow.write(node['address'], 1, 4, propar.PP_TYPE_INT8, 0) # BUS/RS232
            print(user_tag)
            self.write_textEdit_signal.emit(f"Control mode {user_tag}" + "\n", textEdit_here)

            self.CAPACITY_100 = self.master_flow.read(self.nodes[0]['address'], 1, 13,
                                              propar.PP_TYPE_FLOAT)  # CAPACITY 100%
            self.CAPACITY_000 = self.master_flow.read(self.nodes[0]['address'], 33, 22,
                                              propar.PP_TYPE_FLOAT)  # CAPACITY 0%

            self.chenge_SpinBox_signal.emit(doubleSpinBox_value_here, self.CAPACITY_100, self.CAPACITY_000)



    def run_worker(self):
        while 1:
            # self.new_point = random.random()
            self.button_test_grah()
            self.progress.emit()
            time.sleep(0.25)
            if self.exit_worker:
                self.finished.emit()
                return

    def button_test_grah(self):
        self.time_start_pro = datetime.now()
        tdelta = self.time_start_pro - self.time_stop_pro

        time_gap = 2 # Каждые 2 секунд
        if tdelta.total_seconds() > time_gap:
            self.X_time_1[1] += 1
            if self.X_time_1[1] % 6 == 0:
                self.X_time_1[0] = datetime.now().strftime("%X")
            else:
                self.X_time_1[0] = ""

            temper_f = self.master_flow.read(self.nodes[0]['address'], 33, 7,
                                                propar.PP_TYPE_FLOAT)  # Температура
            name_f = self.master_flow.read(self.nodes[0]['address'], 1, 17, propar.PP_TYPE_STRING)  # FLUID NAME

            self.lineEdit_temperature_singal.emit(name_f, temper_f, self.lineEdit_temperature_here)

            # {'proc_nr': 33, 'parm_nr': 7, 'parm_type': propar.PP_TYPE_FLOAT}
            user_tag = self.master_flow.read(self.nodes[0]['address'], 1, 1, propar.PP_TYPE_INT16)  # SetPoint

            F_MEASURE_here = self.master_flow.read(self.nodes[0]['address'],
                                             33, 0, propar.PP_TYPE_FLOAT)  # F_MEASURE_Thread

            time.sleep(0.1)
            self.y_buff = F_MEASURE_here  # Новая точка
            if self.y_buff != None:
                self.y_main_plot_m1.append(self.y_buff)  # В конец масива
                self.gas_consumption_m1 = self.gas_consumption_m1 + self.y_buff / 3600 * time_gap # Расход газа
            else:
                problem = 1 # Проблема, поставить красные точки если Nan
                self.if_nan_point_signal_m1.emit()
                self.y_main_plot_m1.append(self.y_main_plot_m1[-1])  # В конец масива
                self.gas_consumption_m1 = self.gas_consumption_m1 + self.y_main_plot_m1[-1] / 3600

            size_range_all_data = 3600
            # size_range_all_data = 24  # тест

            if len(self.x_t_plot_name) < size_range_all_data:  # Ограничение по времени
                self.x_t_plot_name.append(self.X_time_1[1])  # В конец масива

            self.x_t_plot.append(self.X_time_1[0])  # В конец масива

            self.ticks = [list(zip(range(len(self.x_t_plot)), self.x_t_plot))]

            if len(self.x_t_plot) > size_range_all_data:  # Ограничение по времени
                # del self.x_t_plot_name[0]
                del self.x_t_plot[0]
                del self.y_main_plot_m1[0]
                gc.collect()

            self.graph_signal.emit(self.x_t_plot_name, self.y_main_plot_m1,
                              self.time_size, self.ticks)

            self.time_stop_pro = datetime.now()

    def read_data(self):
        # Проверки на ошибки
        # for k in range(3):
        #     if user_tag is None:
        #         user_tag = self.master_flow.read(self.nodes[0]['address'], 1, 1, propar.PP_TYPE_INT16)
        #         print(f"Problem None №{k}")
        #         time.sleep(0.1)
        #         self.stop_master_1()
        #         time.sleep(0.2)
        #         self.start_master_1()
        #         time.sleep(0.2)
        #         self.Change_Slider_1()
        #     else:
        #         break
        # if self.value_scrolbar_1 != user_tag:
        #     self.Change_Slider_1()
        #     if self.value_scrolbar_1 != user_tag:
        #         self.stop_master_1()
        #         time.sleep(0.2)
        #         self.start_master_1()
        #         time.sleep(0.2)
        #         self.Change_Slider_1()

        F_MEASURE_here = self.master_flow.read(self.nodes[0]['address'],
                                         33, 0, propar.PP_TYPE_FLOAT)  # F_MEASURE_Thread

        time.sleep(0.1)
        # self.y_buff = F_MEASURE_here  # Новая точка

        self.graph_signal.emit(self.x_t_plot_name, self.y_main_plot_m1,
                          self.time_size, self.ticks)

        temper_f = self.master_flow.read(self.nodes[0]['address'], 33, 7,
                                            propar.PP_TYPE_FLOAT)  # Температура
        name_f = self.master_flow.read(self.nodes[0]['address'],
                                       1, 17, propar.PP_TYPE_STRING)  # FLUID NAME

        self.lineEdit_temperature_singal.emit(name_f, temper_f, self.lineEdit_temperature_here)

        return F_MEASURE_here # Новая точка


    def change_point_in_worker(self, new_data):
        self.new_point = new_data

    def change_to_zero(self):
        values = self.master_flow.write(self.nodes[0]['address'], 1, 1, propar.PP_TYPE_INT16, 0)
        print(values)
        self.master_flow.stop()

    def stop_QTheath_in_worker(self):
        self.change_to_zero()
        self.finished.emit()

    def __init__(self):
        super(Flow_worker_class, self).__init__()