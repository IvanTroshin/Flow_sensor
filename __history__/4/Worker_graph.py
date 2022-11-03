from pyqtgraph import PlotWidget
from PyQt5.QtCore import QObject, pyqtSignal

import numpy as np
import time
from datetime import datetime
import gc   # Очистка пямяти

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

    graph_signal = pyqtSignal(list, list, list, int, list, bool, bool)
    read_point_f1_signal = pyqtSignal() # Для точки из другого потока
    read_point_f2_signal = pyqtSignal() # Для точки из другого потока

    time_start_pro = 0      # Для определения разности времён
    time_stop_pro = 0
    X_time_1 = [0, 0]       # Время изменения

    exit_worker = False # Остановить поток

    time_start_pro = datetime.now()
    time_stop_pro = datetime.now()

    x_t_plot = list([])         # Для координат
    x_t_plot_name = list([])    # Для название координат (поставить время)
    y_main_plot_m1 = list([])   # Для расхода газа
    y_main_plot_m2 = list([])   # Для расхода газа
    y_buff = 0                  # Для записи

    gas_consumption_m1 = 0      # Общий расход газа первого
    gas_consumption_m2 = 0      # Общий расход газа второго


    def run_master(self):
        t = 1


    def run_worker(self):
        while 1:
            self.paint_grah()
            self.progress.emit()
            time.sleep(0.5)
            if self.exit_worker:
                self.finished.emit()
                return

    def paint_grah(self):
        self.time_start_pro = datetime.now()
        tdelta = self.time_start_pro - self.time_stop_pro

        time_gap = 2 # Каждые 2 секунд
        if tdelta.total_seconds() > time_gap:
            self.X_time_1[1] += 1
            if self.X_time_1[1] % 6 == 0:
                self.X_time_1[0] = datetime.now().strftime("%X")
            else:
                self.X_time_1[0] = ""

            self.y_buff = F_MEASURE_here  # Новая точка
            time.sleep(0.5)
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

            self.time_stop_pro = datetime.now()



    def __init__(self):
        super(Flow_worker_class_garph, self).__init__()