import sys
import propar

import time
# import My_Processing
import Find_com_port as f_c

import gc   # Очистка пямяти
from memory_profiler import profile

from PyQt5 import QtCore, QtGui, QtWidgets
from gui.qt_io import Ui_MainWindow
import pyqtgraph as pg
import numpy as np
# from pyqtgraph import PlotWidget, plot
from datetime import datetime
from PyQt5.QtCore import QObject, QThread, pyqtSignal
import random
import os

pg.setConfigOption('background', 'w')


class Worker(QObject):
    test_signal_worker = pyqtSignal()
    finished = pyqtSignal()
    progress = pyqtSignal()
    graph_signal = pyqtSignal()

    q = 1.0 # Тест

    # x_t_plot = np.array([])                 # Для координат
    # x_t_plot_name = np.array([])            # Для название координат (поставить время)
    # y_main_plot = np.array([[]])            # Для расхода газа
    x_t_plot = list([])                     # Для координат
    x_t_plot_name = list([])                # Для название координат (поставить время)
    y_main_plot = list([])                  # Для расхода газа
    y_buff = 0                              # Для записи

    # time_size = 30                          # шприна по X
    time_size = 3  # шприна по X

    time_start_pro = 0      # Для определения разности времён
    time_stop_pro = 0
    X_time_1 = [0, 0]       # Время изменения

    time_start_pro = datetime.now()
    time_stop_pro = datetime.now()

    def checking_connection(self, comN):

        self.el_flow = propar.instrument(comN)  # Подключение к расходомеру

        print("Worker")
        print(self.el_flow)

        # self.read_data_flow()

        # self.el_flow = propar.instrument('COM12')

    def run_worker(self):
        while 1:
            self.q = random.random()
            self.button_test_grah()
            self.progress.emit()
            time.sleep(1)

    
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

            self.y_buff = 100 * self.q  # Новая точка

            self.y_main_plot.append(self.y_buff)  # В конец масива

            self.x_t_plot.append(self.X_time_1[0])  # В конец масива
            self.x_t_plot_name.append(self.X_time_1[1])  # В конец масива

            # if len(self.x_t_plot_name) <= self.time_size:
            #     self.a_f = 0
            #     self.a_l = len(self.x_t_plot_name)
            # else:
            #     self.a_f = len(self.x_t_plot_name) - self.time_size
            #     self.a_l = len(self.x_t_plot_name)

            self.ticks = [list(zip(range(len(self.x_t_plot)), self.x_t_plot))]

            # self.graph_signal.emit()

            # print(" ")
            # print(self.ticks)
            # print(self.x_t_plot)
            # print(self.x_t_plot_name)
            # print(self.y_main_plot)


            # if len(self.x_t_plot_name) > 3600:  # Ограничение по времени
            if len(self.x_t_plot_name) > 6:  # Ограничение по времени
                del self.x_t_plot_name[0]
                del self.x_t_plot[0]
                del self.y_main_plot[0]
                del self.ticks
                gc.collect()

            # if len(self.x_t_plot_name) > 36:  # Ограничение по времени
            #     self.x_t_plot_name.pop(0)
            #     self.x_t_plot.pop(0)
            #     self.y_main_plot.pop(0)
            #     gc.collect()

            self.time_stop_pro = datetime.now()
    '''
            self.y_main_plot = np.append(self.y_main_plot, self.y_buff)  # В конец масива

            self.x_t_plot = np.append(self.x_t_plot, self.X_time_1[0])  # В конец масива
            self.x_t_plot_name = np.append(self.x_t_plot_name, self.X_time_1[1])  # В конец масива

            if len(self.x_t_plot_name) <= self.time_size:
                self.a_f = 0
                self.a_l = len(self.x_t_plot_name)
            else:
                self.a_f = len(self.x_t_plot_name) - self.time_size
                self.a_l = len(self.x_t_plot_name)

            self.ticks = [list(zip(range(len(self.x_t_plot)), self.x_t_plot))]

            self.graph_signal.emit()

            # if len(self.x_t_plot_name) > 3600:  # Ограничение по времени
            if len(self.x_t_plot_name) > 36:  # Ограничение по времени
                np.delete(self.x_t_plot_name, self.x_t_plot_name[0])
                np.delete(self.x_t_plot, self.x_t_plot_name[0])
                np.delete(self.y_main_plot, self.x_t_plot_name[0])

            self.time_stop_pro = datetime.now()
    '''

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


class testapp(QObject):

    def launch(self):
        # инициация и демонстрация интерфейса
        self.main_window = QtWidgets.QMainWindow()
        self.ui_main_window = Ui_MainWindow()
        self.ui_main_window.setupUi(self.main_window)
        self.main_window.show()

        # ----------------- Кнопки ------------------------------

        self.ui_main_window.actionFind_com_port.triggered.connect(self.find_com_port_foo)  # Поиск активных COM порт и записывает в ComboBox
        # self.ui_main_window.pushButton_OK.pressed.connect(proces.test)
        self.ui_main_window.pushButton_Close.pressed.connect(self.exit_prog)
        self.ui_main_window.pushButton_connect.pressed.connect(self.connect_com_run) # Подключение к первому
        self.ui_main_window.pushButton_connect_2.pressed.connect(self.connect_com_run_2) # Подключение ко второму
        self.ui_main_window.Test.pressed.connect(self.start_observed_flow)

        # ---------------- Запуск потоков ------------------------

        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = Worker()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        # self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        # self.worker.progress.connect(self.reportProgress)
        # Step 6: Start the thread
        self.thread.start()

        # ------------ Сигналы и слоты ---------------------------

        self.worker.graph_signal.connect(self.paint_graph_in_canvas)
        self.worker.test_signal_worker.connect(self.func22)

        # ---------------- Вспомогательные ------------------------

        self.find_com_port_foo() # Поиск активных COM порт и записывает в ComboBox

        # ---------------- Логика программы ------------------------

        self.ui_main_window.graphicsView_FS.setLabel('bottom', 'Time', color='g', **{'font-size':'12pt'})   # Название осей
        self.ui_main_window.graphicsView_FS.getAxis('bottom').setPen(pg.mkPen(color=(128, 128, 128), width=3))

        self.ui_main_window.graphicsView_FS.setLabel('left', 'Gas Flow', units='l/h', color='r', **{'font-size': '12pt'})
        self.ui_main_window.graphicsView_FS.getAxis('left').setPen(pg.mkPen(color=(0, 100, 0), width=3))
        # self.ui_main_window.graphicsView_FS.setTitle('The first')        # Название графика

    def get_rand(self):
        self.func22()


    def func22(self):
        self.ui_main_window.textEdit.insertPlainText(str(self.worker.q))
        self.ui_main_window.textEdit.insertPlainText("\n")

    def exit_prog(self):
        sys.exit(app.exec_())

    def connect_com_run(self):
        COM_port = self.ui_main_window.comboBox.currentText()
        self.connect_com(COM_port, self.ui_main_window.textEdit)

    def connect_com_run_2(self):
        COM_port = self.ui_main_window.comboBox_2.currentText()
        self.connect_com(COM_port, self.ui_main_window.textEdit_2)

    def connect_com(self, COM_port, textEdit_here):

        # print(self.ui_main_window.comboBox.currentText()) # combox get
        # COM_port = self.ui_main_window.comboBox.currentText()

        self.worker.checking_connection(COM_port) # Подключение к расходомеру

        # self.worker.checking_connection("COM3")
        print(self.worker.el_flow.measure)

        if self.worker.el_flow.measure != None:
            # self.ui_main_window.comboBox.setEnabled(False) # Зажим кнопки
            textEdit_here.insertPlainText("Successful connection")
            textEdit_here.insertPlainText("\n")
        else:
            textEdit_here.insertPlainText("Not successful connection")
            textEdit_here.insertPlainText("\n")
            return

        name = self.worker.el_flow.read_parameters([{'proc_nr': 1, 'parm_nr': 17, 'parm_type': propar.PP_TYPE_STRING}])
        textEdit_here.insertPlainText(f'It is %s' %(name[0]['data']))
        textEdit_here.insertPlainText("\n")


        params = [{'proc_nr': 33, 'parm_nr': 0, 'parm_type': propar.PP_TYPE_FLOAT},     # Расход по формуле
                  {'proc_nr': 33, 'parm_nr': 3, 'parm_type': propar.PP_TYPE_FLOAT},     # Заданное значение
                  {'proc_nr': 33, 'parm_nr': 7, 'parm_type': propar.PP_TYPE_FLOAT},     # Температура
                  {'proc_nr': 1, 'parm_nr': 17, 'parm_type': propar.PP_TYPE_STRING},    # FLUID NAME
                  {'proc_nr': 1, 'parm_nr': 13, 'parm_type': propar.PP_TYPE_FLOAT},     # CAPACITY 100%
                  {'proc_nr': 33, 'parm_nr': 22, 'parm_type': propar.PP_TYPE_FLOAT},    # CAPACITY 100%
                  {'proc_nr': 114, 'parm_nr': 1, 'parm_type': propar.PP_TYPE_INT32},    # Valve output
                  {'proc_nr': 115, 'parm_nr': 23, 'parm_type': propar.PP_TYPE_INT8}     # SETPOINT MONITOR MODE
                  ]

        # params = [{'proc_nr': 33, 'parm_nr': 0, 'parm_type': propar.PP_TYPE_FLOAT},
        #           {'proc_nr': 33, 'parm_nr': 3, 'parm_type': propar.PP_TYPE_FLOAT},
        #           {'proc_nr': 33, 'parm_nr': 7, 'parm_type': propar.PP_TYPE_FLOAT},
        #           {'proc_nr': 114, 'parm_nr': 1, 'parm_type': propar.PP_TYPE_INT32}]

        values = self.worker.el_flow.read_parameters(params)


        textEdit_here.insertPlainText("\n")
        for value in values:
            print(value)
            print(value['data'])
            textEdit_here.insertPlainText(f'{ value["data"] }')
            textEdit_here.insertPlainText("\n")

        # for i in range(len(values)):
            # print(values[i]['data'])
            # self.ui_main_window.textEdit_2.insertPlainText(values[i]['data'])
            # self.ui_main_window.textEdit_2.insertPlainText("\n")

        print(values[3]['data'])


    def start_observed_flow(self):
        # self.Find_U_I_min_max()
        self.timer = QtCore.QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.worker.run_worker)
        self.timer.start()



    def button_test_print(self):
        self.ui_main_window.textEdit_2.insertPlainText("Test")
        self.ui_main_window.textEdit_2.insertPlainText("\n")
        print(f_c.serial_ports())
        self.ui_main_window.comboBox_2.addItems(f_c.serial_ports())

    def find_com_port_foo(self):    # Поиск активных COM порт и записывает в ComboBox
        self.ui_main_window.comboBox.clear()
        self.ui_main_window.comboBox_2.clear()
        self.ui_main_window.comboBox.addItems(f_c.serial_ports())
        self.ui_main_window.comboBox_2.addItems(f_c.serial_ports())


    def paint_graph_in_canvas(self):
        xax = self.ui_main_window.graphicsView_FS.getAxis('bottom')
        # print(self.worker.a_f, self.worker.a_l)
        # print(self.worker.ticks[0][self.worker.a_f:self.worker.a_l])

        if len(self.worker.x_t_plot_name) <= self.worker.time_size:
            range_there = len(self.worker.x_t_plot_name)
        else:
            range_there = self.worker.time_size


        buff_name = self.worker.ticks[0][-range_there:]

        # xax.setTicks(buff_name)
        # xax.setTicks([self.worker.ticks[0][-range_there:]])
        # xax.setTicks([self.worker.ticks[0][self.worker.a_f:self.worker.a_l]])

        self.ui_main_window.graphicsView_FS.setYRange(0, 100)

        buff_x = np.array(self.worker.x_t_plot_name[-range_there:])
        buff_y = np.array(self.worker.y_main_plot[-range_there:])

        self.ui_main_window.graphicsView_FS.plot(buff_x,
                                                 buff_y,
                                                 pen=pg.mkPen((0, 100, 0), width=2), name="l/h", clear=True)

        # self.ui_main_window.graphicsView_FS.plot(self.worker.x_t_plot_name[self.worker.a_f:self.worker.a_l],
        #                                          self.worker.y_main_plot[self.worker.a_f:self.worker.a_l],
        #                                          pen=pg.mkPen((0, 100, 0), width=2), name="l/h", clear=True)


    def button_pushed_range(self):
        # Ограничение по y (по времени)
        self.ui_main_window.graphicsView_FS.setXRange(0, 100, padding=0, update=True)
        self.ui_main_window.graphicsView_FS.setYRange(0, 100, padding=0, update=True)
        # Точка на графике
        x_t = np.arange(100)
        y_t = np.random.normal(size=100)
        self.ui_main_window.graphicsView_FS.plot(x_t, y_t, pen=pg.mkPen('r', width=2))


    def Write_data_first(self):

        dt = datetime.now()
        dt_test = dt.strftime("%d_%m_%Y")
        filename = os.getcwd() + "\\Data"
        if os.path.exists(filename):
            my_file = open(filename + "\\A_time_" + dt_test + ".txt", "a")
        else:
            os.mkdir("Data")
            my_file = open(filename + "\\A_time_" + dt_test + ".txt", "a")

        my_file.write("Time\t Gas_consumption\n")
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

        my_file.write(str(datetime.now().strftime("%X")) + "\t" +
                      str(self.data[-1]) + "\n")
        # my_file.write("hello!")
        my_file.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    program = testapp()
    program.launch()
    sys.exit(app.exec_())






