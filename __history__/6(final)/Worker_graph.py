from pyqtgraph import PlotWidget
from PyQt5.QtCore import QObject, pyqtSignal, QWaitCondition, QMutex, pyqtBoundSignal, pyqtSlot

import numpy as np
import time
from datetime import datetime
import gc  # Очистка пямяти
import os

bool_thread_garph = False  # Запущен поток для графика?

'''
def thread_garph(self):
    # ---------------- Запуск потоков ------------------------
    # Step 2: Create a QThread object
    self.Thread_G = QThread()
    # Step 3: Create a worker object
    self.worker_G = w_g.Flow_worker_class_garph()
    # Step 4: Move worker to the thread
    self.worker_G.moveToThread(self.Thread_G)
    # Step 5: Connect signals and slots
    # self.thread.started.connect(self.worker.run)
    self.worker_G.finished.connect(self.Thread_G.quit)
    self.worker_G.finished.connect(self.worker_G.deleteLater)
    self.Thread_G.finished.connect(self.Thread_G.deleteLater)
    # Step 6: Start the Thread_F_MEASURE
    # self.Thread_F_MEASURE.start()

    # ------------ Сигналы и слоты ---------------------------
    self.ui_main_window.pushButton_prob_1.pressed.connect(self.worker_G.run_worker)
    # self.worker_G.read_F_MEASURE_signal.connect(self.read_F_MEASURE)
    # self.worker_G.data_all_signal.connect(self.data_to_thread)

    # --------------------------------------------------------
    self.Thread_G.started.connect(lambda: self.worker_G.run_master(self.ui_main_window.graphicsView_FS_1))
    self.Thread_G.start()
'''


class Flow_worker_class_garph(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal()

    graph_signal = pyqtSignal(list, list, list, int, list)

    gas_consumption_signal_1 = pyqtSignal(float)  # Перезапуск расходомера, выключение включение
    gas_consumption_signal_2 = pyqtSignal(float)  # Перезапуск расходомера, выключение включение

    # pyqtBoundSignal
    read_point_here_signal_f1 = pyqtSignal()  # Для точки из другого потока
    read_point_here_signal_f2 = pyqtSignal()  # Для точки из другого потока

    reload_signal_1 = pyqtSignal()  # Перезапуск расходомера, выключение включение
    reload_signal_2 = pyqtSignal()  # Перезапуск расходомера, выключение включение

    X_time_1 = [0, 0]  # Время изменения
    time_size = 60  # шприна по X

    exit_worker = False  # Остановить поток

    time_start_pro = datetime.now()  # Для определения разности времён
    time_stop_pro = datetime.now()

    x_t_plot = list([])  # Для координат
    x_t_plot_name = list([])  # Для название координат (поставить время)
    y_main_plot_m1 = list([])  # Для расхода газа
    y_main_plot_m2 = list([])  # Для расхода газа
    value_program_m1 = list([]) # Для выставленного значения в программе
    value_program_m2 = list([]) # Для выставленного значения в программе

    y_buff = 0  # Для записи

    gas_consumption_m1 = 0  # Общий расход газа первого
    gas_consumption_m2 = 0  # Общий расход газа второго

    def run_master(self):
        t = 1

    def run_worker(self):
        while 1:
            self.paint_grah()
            self.progress.emit()
            time.sleep(0.1)
            if self.exit_worker:
                self.finished.emit()
                return

    def paint_grah(self):
        bool_write = False
        self.time_start_pro = datetime.now()
        tdelta = self.time_start_pro - self.time_stop_pro

        time_gap = 2  # Каждые 2 секунд
        if tdelta.total_seconds() > time_gap:
            self.X_time_1[1] += 1
            if self.X_time_1[1] % 6 == 0:
                self.X_time_1[0] = datetime.now().strftime("%X")
                bool_write = True
            else:
                self.X_time_1[0] = ""

            # ----------------------------------------------------------------

            self.y_buff_1 = None
            # self.y_buff_1 = F_MEASURE_here  # Новая точка
            self.read_point_here_signal_f1.emit()
            time.sleep(0.1)
            for i in range(3):
                time.sleep(0.1)
                self.read_point_here_signal_f1.emit()
                if self.y_buff_1 is not None:
                    break
                if i == 1 or i == 2:
                    self.reload_signal_1.emit()  # Перезапуск расходомера
                    time.sleep(0.1)

            if self.y_buff_1 is not None:
                self.y_main_plot_m1.append(self.y_buff_1)  # В конец масива
                self.gas_consumption_m1 = self.gas_consumption_m1 + self.y_buff_1 / 3600 * time_gap  # Расход газа
                self.gas_consumption_signal_1.emit(self.gas_consumption_m1)
            else:
                problem = 1  # Проблема, поставить красные точки если Nan
                self.y_main_plot_m1.append(0)  # В конец масива
                self.gas_consumption_m1 = self.gas_consumption_m1 + 0 / 3600 * time_gap  # Расход газа
                self.gas_consumption_signal_1.emit(self.gas_consumption_m1)

            # ----------------------------------------------------------------

            self.y_buff_2 = None
            # self.y_buff_2 = F_MEASURE_here  # Новая точка
            self.read_point_here_signal_f2.emit()

            time.sleep(0.1)
            for i in range(3):
                time.sleep(0.1)
                self.read_point_here_signal_f2.emit()
                if self.y_buff_1 is not None:
                    break
                if i == 1 or i == 2:
                    self.reload_signal_2.emit()  # Перезапуск расходомера
                    time.sleep(0.1)

            if self.y_buff_2 is not None:
                self.y_main_plot_m2.append(self.y_buff_2)  # В конец масива
                self.gas_consumption_m2 = self.gas_consumption_m2 + self.y_buff_2 / 3600 * time_gap  # Расход
                self.gas_consumption_signal_2.emit(self.gas_consumption_m2)
            else:
                problem = 1  # Проблема, поставить красные точки если Nan
                self.y_main_plot_m2.append(0)  # В конец масива
                self.gas_consumption_m2 = self.gas_consumption_m2 + 0 / 3600 * time_gap  # Расход
                self.gas_consumption_signal_2.emit(self.gas_consumption_m2)

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

            self.graph_signal.emit(self.x_t_plot_name,
                                   self.y_main_plot_m1, self.y_main_plot_m2,
                                   self.time_size, self.ticks)

            if bool_write:
                self.Write_data() # Запись в файл

            self.time_stop_pro = datetime.now()

    def setAnswer_1(self, value, name, value_p, tempr):
        self.y_buff_1 = value
        self.name_1 = name
        self.value_program_m1.append(value_p)
        self.temperature_f1 = tempr
        if len(self.value_program_m1) > 6:  # Ограничение по времени
            del self.value_program_m1[0]

    def setAnswer_2(self, value, name, value_p, tempr):
        self.y_buff_2 = value
        self.name_2 = name
        self.value_program_m2.append(value_p)
        self.temperature_f2 = tempr
        if len(self.value_program_m2) > 6:  # Ограничение по времени
            del self.value_program_m2[0]

    def Write_data_first(self):
        dt = datetime.now()
        dt_test = dt.strftime("%d_%m_%Y")
        filename = os.getcwd() + "\\Data"
        if os.path.exists(filename):
            my_file = open(filename + "\\A_time_" + dt_test + ".txt", "a")
        else:
            os.mkdir("Data")
            my_file = open(filename + "\\A_time_" + dt_test + ".txt", "a")

        my_file.write(f"Time\t" 
                f"value_on_device_(l/h)_{self.name_1}\tvalue_in_program_(l/h)_{self.name_1}\t" +
                f"Gas_consumption_(l/h)_{self.name_1}\tTemperature_(C)_{self.name_1}\t" +
                f"value_on_device_(l/h)_{self.name_2}\tvalue_in_program_(l/h)_{self.name_2}\t" +
                f"Gas_consumption_(l/h)_{self.name_2}\tTemperature_(C)_{self.name_2}_C\n")
        my_file.close()

    def Write_data(self):
        dt = datetime.now()
        dt_test = dt.strftime("%d_%m_%Y")
        filename = os.getcwd() + "\\Data"
        if os.path.exists(filename):
            if os.path.exists(filename + "\\A_time_" + dt_test + ".txt"):
                my_file = open(filename + "\\A_time_" + dt_test + ".txt", "a")
            else:
                self.Write_data_first()
                my_file = open(filename + "\\A_time_" + dt_test + ".txt", "a")
        else:
            os.mkdir("Data")
            my_file = open(filename + "\\A_time_" + dt_test + ".txt", "a")

        value_dev_f1 = sum(self.y_main_plot_m1[-5:]) / 5
        value_prog_f1 = sum(self.value_program_m1[-5:]) / 5

        value_dev_f2 = sum(self.y_main_plot_m2[-5:]) / 5
        value_prog_f2 = sum(self.value_program_m2[-5:]) / 5

        buff_time = datetime.now().strftime("%X")

        my_file.write(f"{buff_time}\t"
                      f"{round(value_dev_f1, 3)}\t{round(value_prog_f1, 3)}\t" +
                      f"{round(self.gas_consumption_m1, 3)}\t{round(self.temperature_f1, 3)}\t" +
                      f"{round(value_dev_f2, 3)}\t{round(value_prog_f2, 3)}\t" +
                      f"{round(self.gas_consumption_m2, 3)}\t{round(self.temperature_f2, 3)}\n")

        # my_file.write("hello!")
        my_file.close()

    def __init__(self):
        super(Flow_worker_class_garph, self).__init__()
        self.temperature_f1 = None
        self.temperature_f2 = None
        self.name_2 = None
        self.name_1 = None
        self.ticks = None
        self.y_buff_2 = None
        self.y_buff_1 = None
