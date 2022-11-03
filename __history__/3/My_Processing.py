from pyqtgraph import PlotWidget
import numpy as np
import random
import propar
from gui.qt_io import Ui_MainWindow
from PyQt5.QtCore import QObject, QThread, pyqtSignal
import time
from datetime import datetime
import gc   # Очистка пямяти

class Worker_class(QObject):
    test_signal_worker = pyqtSignal()
    finished = pyqtSignal()
    progress = pyqtSignal()
    graph_signal = pyqtSignal()
    new_point_m1_signal = pyqtSignal()
    new_point_m2_signal = pyqtSignal()
    if_nan_point_signal_m1 = pyqtSignal()
    if_nan_point_signal_m2 = pyqtSignal()

    exit_worker = False

    new_point_m1 = 0    # Точка на графике
    new_point_m2 = 0    # Точка на графике

    x_t_plot = list([])         # Для координат
    x_t_plot_name = list([])    # Для название координат (поставить время)
    y_main_plot_m1 = list([])   # Для расхода газа
    y_main_plot_m2 = list([])   # Для расхода газа
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

    def checking_connection(self, comN, number_flow):
        if number_flow == 1:
            self.el_flow_1 = propar.instrument(comN)  # Подключение к расходомеру
            print("Worker")
            print(self.el_flow_1)

        if number_flow == 2:
            self.el_flow_2 = propar.instrument(comN)  # Подключение к расходомеру
            print("Worker")
            print(self.el_flow_2)


    def run_worker(self):
        while 1:
            # self.new_point = random.random()
            self.button_test_grah()
            self.progress.emit()
            time.sleep(1)
            if self.exit_worker:
                self.finished.emit()
                return

    def button_test_grah(self):
        self.ui_main_window = Ui_MainWindow()
        self.time_start_pro = datetime.now()
        tdelta = self.time_start_pro - self.time_stop_pro

        if tdelta.total_seconds() > 1.0:  # Каждую 1 секунду
            self.X_time_1[1] += 1
            if self.X_time_1[1] % 6 == 0:
                self.X_time_1[0] = datetime.now().strftime("%X")
            else:
                self.X_time_1[0] = ""


            self.new_point_m1_signal.emit()
            time.sleep(0.1)
            self.y_buff = self.new_point_m1  # Новая точка
            if self.y_buff != None:
                self.y_main_plot_m1.append(self.y_buff)  # В конец масива
                self.gas_consumption_m1 = self.gas_consumption_m1 + self.y_buff / 3600 # Расход газа
            else:
                problem = 1 # Проблема, поставить красные точки если Nan
                self.if_nan_point_signal_m1.emit()
                self.y_main_plot_m1.append(self.y_main_plot_m1[-1])  # В конец масива
                self.gas_consumption_m1 = self.gas_consumption_m1 + self.y_main_plot_m1[-1] / 3600


            self.new_point_m2_signal.emit()
            time.sleep(0.1)
            self.y_buff = self.new_point_m2  # Новая точка
            if self.y_buff != None:
                self.y_main_plot_m2.append(self.y_buff)  # В конец масива
                self.gas_consumption_m2 = self.gas_consumption_m2 + self.y_buff / 3600 # Расход газа
            else:
                problem = 1 # Проблема, поставить красные точки если Nan
                self.if_nan_point_signal_m2.emit()
                self.y_main_plot_m2.append(self.y_main_plot_m2[-1])  # В конец масива
                self.gas_consumption_m2 = self.gas_consumption_m2 + self.y_main_plot_m2[-1] / 3600

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
                del self.y_main_plot_m2[0]
                gc.collect()

            self.graph_signal.emit()

            self.time_stop_pro = datetime.now()

    def change_point_in_worker(self, new_data):
        self.new_point = new_data

    def stop_QTheath_in_worker(self):
        self.finished.emit()


    def read_data_flow(self):
        params = [{'proc_nr': 33, 'parm_nr': 0, 'parm_type': propar.PP_TYPE_FLOAT},     # Расход по формуле
                  {'proc_nr': 33, 'parm_nr': 3, 'parm_type': propar.PP_TYPE_FLOAT},     # Заданное значение
                  {'proc_nr': 33, 'parm_nr': 7, 'parm_type': propar.PP_TYPE_FLOAT},     # Температура
                  {'proc_nr': 1, 'parm_nr': 17, 'parm_type': propar.PP_TYPE_INT8},      # FLUID NAME
                  {'proc_nr': 1, 'parm_nr': 13, 'parm_type': propar.PP_TYPE_FLOAT},     # CAPACITY 100%
                  {'proc_nr': 33, 'parm_nr': 22, 'parm_type': propar.PP_TYPE_FLOAT},    # CAPACITY 100%
                  {'proc_nr': 114, 'parm_nr': 1, 'parm_type': propar.PP_TYPE_INT32}]    # Valve output

        values = self.el_flow.read_parameters(params)

        for value in values:
            print(value)
            print("Q")




