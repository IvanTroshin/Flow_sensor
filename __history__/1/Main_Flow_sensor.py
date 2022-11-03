import sys
import propar

import time
import Find_com_port as f_c
import My_Processing as mp  # Класс для потока
import Rear_write_file as rw_f # Функции для зафиси в файл

from PyQt5 import QtCore, QtGui, QtWidgets
from gui.qt_io import Ui_MainWindow
import pyqtgraph as pg
import numpy as np
# from pyqtgraph import PlotWidget, plot
from datetime import datetime
from PyQt5.QtCore import QObject, QThread, pyqtSignal
import random


pg.setConfigOption('background', 'w')

class testapp(QObject):

    def launch(self):
        # инициация и демонстрация интерфейса
        self.main_window = QtWidgets.QMainWindow()
        self.ui_main_window = Ui_MainWindow()
        self.ui_main_window.setupUi(self.main_window)
        self.main_window.show()

        # ----------------- Кнопки ------------------------------

        self.ui_main_window.actionFind_com_port.triggered.connect(self.find_com_port_foo)  # Поиск активных COM порт и записывает в ComboBox
        self.ui_main_window.pushButton_Close.pressed.connect(self.exit_prog)

        # Старое подключение
        # self.ui_main_window.pushButton_connect.pressed.connect(self.connect_com_run) # Подключение к первому
        # self.ui_main_window.pushButton_connect_2.pressed.connect(self.connect_com_run_2) # Подключение ко второму

        # self.ui_main_window.pushButton_connect.pressed.connect(self.start_master_1) # Подключение к первому
        # self.ui_main_window.pushButton_connect_2.pressed.connect(self.start_master_2) # Подключение ко второму

        self.ui_main_window.Test.pressed.connect(self.start_observed_flow)
        self.ui_main_window.pushButton_Start_monitoring.pressed.connect(self.foo_start_QThread)
        self.ui_main_window.pushButton_Stop_monitoring.pressed.connect(self.foo_stop_QThread)

        self.ui_main_window.verticalSlider_1.valueChanged.connect(self.Change_Slider_and_ProgressBar_1)  # Скрол бары
        self.ui_main_window.verticalSlider_2.valueChanged.connect(self.Change_Slider_and_ProgressBar_2)  # Скрол бары

        # self.ui_main_window.pushButton_start_test.pressed.connect(self.start_master)
        # self.ui_main_window.pushButton_prob.pressed.connect(self.Write_SetPoint)
        # self.ui_main_window.pushButton_ex_prob.pressed.connect(self.test_change_point)



        self.ui_main_window.pushButton_Start_1.pressed.connect(self.start_master_1)
        self.ui_main_window.pushButton_stop_1.pressed.connect(self.stop_master_1)
        # self.ui_main_window.pushButton_up_1.pressed.connect(self.ex_master_up_1)
        # self.ui_main_window.pushButton_down_1.pressed.connect(self.ex_master_down_1)

        self.ui_main_window.pushButton_Start_2.pressed.connect(self.start_master_2)
        self.ui_main_window.pushButton_stop_2.pressed.connect(self.stop_master_2)
        # self.ui_main_window.pushButton_up_2.pressed.connect(self.ex_master_up_2)
        # self.ui_main_window.pushButton_down_2.pressed.connect(self.ex_master_down_2)

        # ---------------- Запуск потоков ------------------------

        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = mp.Worker_class()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        # self.thread.started.connect(self.worker.run_worker)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        # self.worker.progress.connect(self.reportProgress)
        # Step 6: Start the thread
        # self.thread.start()

        # ------------ Сигналы и слоты ---------------------------

        self.worker.graph_signal.connect(self.paint_graph_in_canvas)
        self.worker.new_point_m1_signal.connect(self.change_point_worker_1)  # Изменение точки на графике
        self.worker.new_point_m2_signal.connect(self.change_point_worker_2)  # Изменение точки на графике
        self.worker.if_nan_point_signal.connect(self.point_nun_cry)
        # self.worker.test_signal_worker.connect(self.func22)

        # ---------------- Вспомогательные ------------------------

        self.find_com_port_foo() # Поиск активных COM порт и записывает в ComboBox

        # ---------------- Логика программы ------------------------

        self.ui_main_window.graphicsView_FS_1.setLabel('bottom', 'Time', color='g', **{'font-size':'12pt'})   # Название осей
        self.ui_main_window.graphicsView_FS_1.getAxis('bottom').setPen(pg.mkPen(color=(128, 128, 128), width=3))

        self.ui_main_window.graphicsView_FS_1.setLabel('left', 'Gas Flow', units='l/h', color='r', **{'font-size': '12pt'})
        self.ui_main_window.graphicsView_FS_1.getAxis('left').setPen(pg.mkPen(color=(0, 100, 0), width=3))
        # self.ui_main_window.graphicsView_FS_1.setTitle('The first')        # Название графика


    def Change_Slider_and_ProgressBar_1(self):
        buff = self.ui_main_window.verticalSlider_1.value()
        self.ui_main_window.progressBar_1.setValue(buff)

        COM_port = self.ui_main_window.comboBox.currentText()
        self.Chenger_setpoint(COM_port, self.ui_main_window.textEdit_1, 1, self.master_1, buff)

    def Change_Slider_and_ProgressBar_2(self):
        buff = self.ui_main_window.verticalSlider_2.value()
        self.ui_main_window.progressBar_2.setValue(buff)

        COM_port = self.ui_main_window.comboBox.currentText()
        self.Chenger_setpoint(COM_port, self.ui_main_window.textEdit_2, 2, self.master_2, buff)


    def Chenger_setpoint(self, COM_port, textEdit_here, number_flow, master_two, val_chang):

        SetPoin = [{'proc_nr': 1, 'parm_nr': 1, 'parm_type': propar.PP_TYPE_INT16, 'data': 32000}]  # SETPOINT

        # Номер узла self.nodes[0]['address'] не знаю зачем он
        values = master_two.write(self.nodes[0]['address'], 1, 1, propar.PP_TYPE_INT16, val_chang*320)
        print(values)
        # values = self.master.read(self.nodes[0]['address'], SetPoin[0]['proc_nr'], SetPoin[0]['parm_nr'],
        #                           SetPoin[0]['parm_type'])

        user_tag = master_two.read(self.nodes[0]['address'], 1, 1, propar.PP_TYPE_INT16)
        print(f"SETPOINT {user_tag}")
        textEdit_here.insertPlainText(f"SETPOINT {user_tag}")
        textEdit_here.insertPlainText("\n")

    def foo_start_QThread(self):

        # ---------------- Запуск потоков ------------------------
        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = mp.Worker_class()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        # self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        # self.worker.progress.connect(self.reportProgress)
        # Step 6: Start the thread
        # self.thread.start()

        # ------------ Сигналы и слоты ---------------------------
        self.worker.graph_signal.connect(self.paint_graph_in_canvas)
        # self.worker.test_signal_worker.connect(self.func22)

        self.worker.exit_worker = False

    def foo_stop_QThread(self):
        self.worker.exit_worker = True
        self.worker.stop_QTheath_in_worker()


    def exit_prog(self):
        sys.exit(app.exec_())

    def connect_com_run(self):
        COM_port = self.ui_main_window.comboBox.currentText()
        self.connect_com(COM_port, self.ui_main_window.textEdit_1, 1)

    def connect_com_run_2(self):
        COM_port = self.ui_main_window.comboBox_2.currentText()
        self.connect_com(COM_port, self.ui_main_window.textEdit_2, 2)

    def connect_com(self, COM_port, textEdit_here, number_flow):
        q=1
     # Версия без использования мастера, почему-то не работает изменение параметров     ''' '''

        self.worker.checking_connection(COM_port, number_flow) # Подключение к расходомеру

        if number_flow == 1:
            el_foo = self.worker.el_flow_1

        if number_flow == 2:
            el_foo = self.worker.el_flow_2

        print(el_foo.measure)

        if el_foo.measure != None:
            # self.ui_main_window.comboBox.setEnabled(False) # Зажим кнопки
            textEdit_here.insertPlainText("Successful connection")
            textEdit_here.insertPlainText("\n")
        else:
            textEdit_here.insertPlainText("Not successful connection")
            textEdit_here.insertPlainText("\n")
            return

        name = el_foo.read_parameters([{'proc_nr': 1, 'parm_nr': 17, 'parm_type': propar.PP_TYPE_STRING}])  # Что за газ
        textEdit_here.insertPlainText(f'It is %s' %(name[0]['data']))
        textEdit_here.insertPlainText("\n")


        params = [{'proc_nr': 33, 'parm_nr': 0, 'parm_type': propar.PP_TYPE_FLOAT},     # Расход по формуле
                  {'proc_nr': 33, 'parm_nr': 3, 'parm_type': propar.PP_TYPE_FLOAT},     # Заданное значение
                  {'proc_nr': 33, 'parm_nr': 7, 'parm_type': propar.PP_TYPE_FLOAT},     # Температура
                  {'proc_nr': 1, 'parm_nr': 17, 'parm_type': propar.PP_TYPE_STRING},    # FLUID NAME
                  {'proc_nr': 1, 'parm_nr': 13, 'parm_type': propar.PP_TYPE_FLOAT},     # CAPACITY 100%
                  {'proc_nr': 33, 'parm_nr': 22, 'parm_type': propar.PP_TYPE_FLOAT},    # CAPACITY 0%
                  {'proc_nr': 114, 'parm_nr': 1, 'parm_type': propar.PP_TYPE_INT32},    # Valve output
                  {'proc_nr': 115, 'parm_nr': 23, 'parm_type': propar.PP_TYPE_INT8}     # SETPOINT MONITOR MODE
                  ]

        # params = [{'proc_nr': 33, 'parm_nr': 0, 'parm_type': propar.PP_TYPE_FLOAT},
        #           {'proc_nr': 33, 'parm_nr': 3, 'parm_type': propar.PP_TYPE_FLOAT},
        #           {'proc_nr': 33, 'parm_nr': 7, 'parm_type': propar.PP_TYPE_FLOAT},
        #           {'proc_nr': 114, 'parm_nr': 1, 'parm_type': propar.PP_TYPE_INT32}]

        values = el_foo.read_parameters(params)


        textEdit_here.insertPlainText("\n")
        for value in values:
            print(value)
            print(value['data'])
            textEdit_here.insertPlainText(f'{ value["data"] }')
            textEdit_here.insertPlainText("\n")

        print(values[3]['data'])


    def Write_SetPoint(self):
        COM_port = self.ui_main_window.comboBox.currentText()
        number_flow = 1

        self.worker.checking_connection(COM_port, number_flow) # Подключение к расходомеру

        if number_flow == 1:
            el_foo = self.worker.el_flow_1

        if number_flow == 2:
            el_foo = self.worker.el_flow_2

        SetPoin = [{'proc_nr': 1, 'parm_nr': 1, 'parm_type': propar.PP_TYPE_INT16, 'data': 32000}]  # SETPOINT

        ProbAdd = ([
            {'proc_nr': 1, 'parm_nr': 4, 'parm_type': propar.PP_TYPE_INT8, 'parm_chained': True, 'data': 0}
            # {'proc_nr': 1, 'parm_nr': 1, 'parm_type': propar.PP_TYPE_INT16, 'data': 100}
        ])

        status = el_foo.write_parameters(ProbAdd)
        print(status)

        ProbAdd_read = el_foo.read_parameters(ProbAdd)
        print(ProbAdd_read)

        print("  ")
        el_foo.setpoint = 16000
        print(el_foo.measure)
        el_foo.setpoint = 0

        params = [{'proc_nr': 33, 'parm_nr': 0, 'parm_type': propar.PP_TYPE_FLOAT},     # Расход по формуле
                  {'proc_nr': 33, 'parm_nr': 3, 'parm_type': propar.PP_TYPE_FLOAT},     # Заданное значение
                  {'proc_nr': 33, 'parm_nr': 7, 'parm_type': propar.PP_TYPE_FLOAT},     # Температура
                  {'proc_nr': 1, 'parm_nr': 17, 'parm_type': propar.PP_TYPE_STRING},    # FLUID NAME
                  {'proc_nr': 1, 'parm_nr': 13, 'parm_type': propar.PP_TYPE_FLOAT},     # CAPACITY 100%
                  {'proc_nr': 33, 'parm_nr': 22, 'parm_type': propar.PP_TYPE_FLOAT},    # CAPACITY 0%
                  {'proc_nr': 114, 'parm_nr': 1, 'parm_type': propar.PP_TYPE_INT32},    # Valve output
                  {'proc_nr': 115, 'parm_nr': 23, 'parm_type': propar.PP_TYPE_INT8}     # SETPOINT MONITOR MODE
                  ]

        values = el_foo.read_parameters(params)


        self.ui_main_window.textEdit_1.insertPlainText("\n")
        for value in values:
            self.ui_main_window.textEdit_1.insertPlainText(f'{ value["data"] }')
            self.ui_main_window.textEdit_1.insertPlainText("\n")

# self.ui_main_window.pushButton_Start_1.pressed.connect(self.start_master_1)
# self.ui_main_window.pushButton_stop_1.pressed.connect(self.stop_master_1)
# self.ui_main_window.pushButton_up_1.pressed.connect(self.ex_master_up_1)
# self.ui_main_window.pushButton_down_1.pressed.connect(self.ex_master_down_1)

    def start_master_1(self):
        COM_port = self.ui_main_window.comboBox.currentText()
        self.run_master_two(COM_port, self.ui_main_window.textEdit_1, 1)

    def start_master_2(self):
        COM_port = self.ui_main_window.comboBox_2.currentText()
        self.run_master_two(COM_port, self.ui_main_window.textEdit_2, 2)

    def run_master_two(self, COM_port, textEdit_here, number_flow):
        if number_flow == 1:
            self.master_1 = propar.master(COM_port, 38400)
            master_two = self.master_1

        if number_flow == 2:
            self.master_2 = propar.master(COM_port, 38400)
            master_two = self.master_2

        textEdit_here.insertPlainText(f"The Master runs")
        textEdit_here.insertPlainText("\n")

        # Create the master
        # master_two = propar.master(COM_port, 38400)

        # Get nodes on the network
        self.nodes = master_two.get_nodes()

        # Read the usertag of all nodes
        for node in self.nodes :
            user_tag = master_two.read(node['address'], 113, 6, propar.PP_TYPE_STRING)
            print(node['address'])
            print(user_tag)
            # {'proc_nr': 1, 'parm_nr': 17, 'parm_type': propar.PP_TYPE_STRING},  # FLUID NAME
            user_tag = master_two.read(node['address'], 1, 17, propar.PP_TYPE_STRING)
            print(user_tag)
            textEdit_here.insertPlainText(f"{user_tag}")
            textEdit_here.insertPlainText("\n")

            user_tag = master_two.read(node['address'], 1, 1, propar.PP_TYPE_INT16)
            print(f"SETPOINT {user_tag}")
            textEdit_here.insertPlainText(f"SETPOINT {user_tag}")
            textEdit_here.insertPlainText("\n")

            user_tag = master_two.write(node['address'], 1, 4, propar.PP_TYPE_INT8, 0) # BUS/RS232
            # user_tag = master_two.read(node['address'], 1, 4, propar.PP_TYPE_INT8)  # BUS/RS232
            print(user_tag)
            print(f"SETPOINT {user_tag}")
            textEdit_here.insertPlainText(f"Control mode {user_tag}")
            textEdit_here.insertPlainText("\n")


    def ex_master_up_1(self):
        COM_port = self.ui_main_window.comboBox.currentText()
        self.test_for_up(COM_port, self.ui_main_window.textEdit_1, 1, self.master_1)

    def ex_master_up_2(self):
        COM_port = self.ui_main_window.comboBox_2.currentText()
        self.test_for_up(COM_port, self.ui_main_window.textEdit_2, 2, self.master_2)

    def test_for_up(self, COM_port, textEdit_here, number_flow, master_two):

        SetPoin = [{'proc_nr': 1, 'parm_nr': 1, 'parm_type': propar.PP_TYPE_INT16, 'data': 32000}]  # SETPOINT

        # Номер узла self.nodes[0]['address'] не знаю зачем он
        values = master_two.write(self.nodes[0]['address'], 1, 1, propar.PP_TYPE_INT16, 32000)
        print(values)
        # values = self.master.read(self.nodes[0]['address'], SetPoin[0]['proc_nr'], SetPoin[0]['parm_nr'],
        #                           SetPoin[0]['parm_type'])

        user_tag = master_two.read(self.nodes[0]['address'], 1, 1, propar.PP_TYPE_INT16)
        print(f"SETPOINT {user_tag}")
        textEdit_here.insertPlainText(f"SETPOINT {user_tag}")
        textEdit_here.insertPlainText("\n")

    def ex_master_down_1(self):
        COM_port = self.ui_main_window.comboBox.currentText()
        self.test_for_down(COM_port, self.ui_main_window.textEdit_1, 1, self.master_1)

    def ex_master_down_2(self):
        COM_port = self.ui_main_window.comboBox_2.currentText()
        self.test_for_down(COM_port, self.ui_main_window.textEdit_2, 2, self.master_2)

    def test_for_down(self, COM_port, textEdit_here, number_flow, master_two):

        SetPoin = [{'proc_nr': 1, 'parm_nr': 1, 'parm_type': propar.PP_TYPE_INT16, 'data': 0}]  # SETPOINT

        # Номер узла self.nodes[0]['address'] не знаю зачем он
        values = master_two.write(self.nodes[0]['address'], 1, 1, propar.PP_TYPE_INT16, 0)
        print(values)
        # values = self.master.read(self.nodes[0]['address'], SetPoin[0]['proc_nr'], SetPoin[0]['parm_nr'],
        #                           SetPoin[0]['parm_type'])

        user_tag = master_two.read(self.nodes[0]['address'], 1, 1, propar.PP_TYPE_INT16)
        print(f"SETPOINT {user_tag}")
        textEdit_here.insertPlainText(f"SETPOINT {user_tag}")
        textEdit_here.insertPlainText("\n")


    def stop_master_1(self):
        COM_port = self.ui_main_window.comboBox.currentText()
        self.exit_master_two(COM_port, self.ui_main_window.textEdit_1, 1, self.master_1)

    def stop_master_2(self):
        COM_port = self.ui_main_window.comboBox_2.currentText()
        self.exit_master_two(COM_port, self.ui_main_window.textEdit_2, 2, self.master_2)

    def exit_master_two(self, COM_port, textEdit_here, number_flow, master_two):
        SetPoin = {'proc_nr': 1, 'parm_nr': 1, 'parm_type': propar.PP_TYPE_INT16, 'data': 0}  # SETPOINT
        values = master_two.write(self.nodes[0]['address'], 1, 1, propar.PP_TYPE_INT16, 0)
        print(values)
        master_two.stop()
        textEdit_here.insertPlainText(f"The Master is out")
        textEdit_here.insertPlainText("\n")


    def change_point_worker_1(self):
        temper = self.master_1.read(self.nodes[0]['address'], 33, 7, propar.PP_TYPE_FLOAT)  # Температура
        # time.sleep(0.1)
        # print(f"Temperature {temper}")

        # {'proc_nr': 33, 'parm_nr': 7, 'parm_type': propar.PP_TYPE_FLOAT}
        user_tag = self.master_1.read(self.nodes[0]['address'], 1, 1, propar.PP_TYPE_INT16) # SetPoint


        for k in range(3):
            if user_tag is None:
                user_tag = self.master_1.read(self.nodes[0]['address'], 1, 1, propar.PP_TYPE_INT16)
                print(f"Problem None №{k}")
                time.sleep(0.1)

                self.stop_master_1()
                time.sleep(0.1)
                self.start_master_1()
                time.sleep(0.1)
                self.Change_Slider_and_ProgressBar_1()

            else:
                break

        self.worker.new_point_m1 = user_tag

    def change_point_worker_2(self):
        temper = self.master_2.read(self.nodes[0]['address'], 33, 7, propar.PP_TYPE_FLOAT)  # Температура
        # time.sleep(0.1)
        # print(f"Temperature {temper}")

        # {'proc_nr': 33, 'parm_nr': 7, 'parm_type': propar.PP_TYPE_FLOAT}
        user_tag = self.master_2.read(self.nodes[0]['address'], 1, 1, propar.PP_TYPE_INT16)  # SetPoint

        for k in range(3):
            if user_tag is None:
                user_tag = self.master_2.read(self.nodes[0]['address'], 1, 1, propar.PP_TYPE_INT16)
                print(f"Problem None №{k}")
                time.sleep(0.1)

                self.stop_master_2()
                time.sleep(0.1)
                self.start_master_2()
                time.sleep(0.1)
                self.Change_Slider_and_ProgressBar_2()

            else:
                break


        self.worker.new_point_m2 = user_tag

    def point_nun_cry(self):
        data_point_nan = datetime.now().strftime("%X")
        self.ui_main_window.textEdit_1.insertPlainText(f"Nan point {data_point_nan}")
        self.ui_main_window.textEdit_1.insertPlainText("\n")


    def start_observed_flow(self):
        self.thread.started.connect(self.worker.run_worker)
        self.thread.start()



    def find_com_port_foo(self):    # Поиск активных COM порт и записывает в ComboBox
        self.ui_main_window.comboBox.clear()
        self.ui_main_window.comboBox_2.clear()
        self.ui_main_window.comboBox.addItems(f_c.serial_ports())
        self.ui_main_window.comboBox.setCurrentIndex(1)
        self.ui_main_window.comboBox_2.addItems(f_c.serial_ports())
        self.ui_main_window.comboBox_2.setCurrentIndex(2)


    def paint_graph_in_canvas(self):
        xax = self.ui_main_window.graphicsView_FS_1.getAxis('bottom')
        # print(self.worker.a_f, self.worker.a_l)
        # print(self.worker.ticks[0][self.worker.a_f:self.worker.a_l])

        if len(self.worker.x_t_plot_name) <= self.worker.time_size:
            range_there = len(self.worker.x_t_plot_name)
        else:
            range_there = self.worker.time_size

        xax.setTicks([self.worker.ticks[0][-range_there:]])

        # self.ui_main_window.graphicsView_FS_1.setYRange(0, 100) # Ограницение по Y от 0 до 100
        # self.ui_main_window.graphicsView_FS_1.setYRange(20, 30)
        self.ui_main_window.graphicsView_FS_1.setYRange(0, 32500)

        time.sleep(0.3)
        self.ui_main_window.graphicsView_FS_1.plot(np.array(self.worker.x_t_plot_name[-range_there:]),
                                                   np.array(self.worker.y_main_plot_m1[-range_there:]),
                                                   pen=pg.mkPen((255, 69, 0), width=2), name="l/h", clear=True)

        buff = list([])
        for k in range(range_there):
            buff.append(k)

        # x = np.random.normal(size=1000)
        # y = np.random.normal(size=1000)
        # self.ui_main_window.graphicsView_FS_1.plot(x, y, pen=None, symbol='o')  # Рисует кружки

        self.ui_main_window.graphicsView_FS_1.plot(np.array(self.worker.x_t_plot_name[-range_there:]),
                                                   np.array(self.worker.y_main_plot_m2[-range_there:]),
                                                   pen=pg.mkPen((0, 102, 255), width=2), name="l/h")



    def button_pushed_range(self):
        # Ограничение по y (по времени)
        self.ui_main_window.graphicsView_FS_1.setXRange(0, 100, padding=0, update=True)
        self.ui_main_window.graphicsView_FS_1.setYRange(0, 100, padding=0, update=True)
        # Точка на графике
        x_t = np.arange(100)
        y_t = np.random.normal(size=100)
        self.ui_main_window.graphicsView_FS_1.plot(x_t, y_t, pen=pg.mkPen('r', width=2))






# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    program = testapp()
    program.launch()
    sys.exit(app.exec_())






