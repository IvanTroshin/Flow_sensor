import sys
import propar

import time
import Find_com_port as f_c
import Worker_connect as w_c  # Класс для потока
import Worker_F_MEASURE_Thread as mp_f  # Класс для потока
import Worker_graph as w_g
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

    def __init__(self):
        super(testapp, self).__init__()

    F1_CAPACITY_100 = 0 # Максимальное значение вервого расходомера
    F1_CAPACITY_000 = 0 # Минимальное значение вервого расходомера

    F2_CAPACITY_100 = 0 # Максимальное значение вервого расходомера
    F2_CAPACITY_000 = 0 # Минимальное значение вервого расходомера

    value_scrolbar_1 = 0 # сохраниет значение расхода от 0 до 32000
    value_scrolbar_2 = 0 # сохраниет значение расхода от 0 до 32000

    what_change_1 = True # Нужен чтобы изменялся один раз все параметры
    what_change_2 = True # Нужен чтобы изменялся один раз все параметры

    F1_bool_MT = False # Для потока на выходе
    F2_bool_MT = False # Для потока на выходе

    do_tread_run_1 = True # Запущен ли поток
    do_tread_run_2 = True # Запущен ли поток

    come_port_f1 = 0
    come_port_f2 = 0

    def launch(self):
        # инициация и демонстрация интерфейса
        self.main_window = QtWidgets.QMainWindow()
        self.ui_main_window = Ui_MainWindow()
        self.ui_main_window.setupUi(self.main_window)
        self.main_window.show()

        # ----------------- Кнопки ------------------------------

        self.ui_main_window.actionFind_com_port.triggered.connect(self.find_com_port_foo)  # Поиск активных COM порт и записывает в ComboBox
        self.ui_main_window.pushButton_Close.pressed.connect(self.exit_prog)

        self.ui_main_window.pushButton_prob_2.pressed.connect(self.prob_read)


        self.ui_main_window.pushButton_Stop_monitoring.pressed.connect(self.foo_stop_QThread)

        self.ui_main_window.verticalSlider_1.valueChanged.connect(self.Change_Slider_1)  # Скрол бары
        self.ui_main_window.verticalSlider_2.valueChanged.connect(self.Change_Slider_2)  # Скрол бары

        self.ui_main_window.doubleSpinBox_persent_1.editingFinished.connect(self.Change_from_SpinBox_persent_1) # Проценты
        self.ui_main_window.doubleSpinBox_persent_2.editingFinished.connect(self.Change_from_SpinBox_persent_2) # Проценты

        self.ui_main_window.doubleSpinBox_value_1.editingFinished.connect(self.Change_from_SpinBox_value_1) # Значения
        self.ui_main_window.doubleSpinBox_value_2.editingFinished.connect(self.Change_from_SpinBox_value_2) # Значения

        self.ui_main_window.pushButton_start_test.pressed.connect(self.thread_garph)
        self.ui_main_window.pushButton_prob_1.pressed.connect(self.foo_test_t)


        self.ui_main_window.pushButton_Start_1.pressed.connect(self.start_master_1)
        self.ui_main_window.pushButton_stop_1.pressed.connect(self.stop_master_1)

        self.ui_main_window.pushButton_Start_2.pressed.connect(self.start_master_2)
        self.ui_main_window.pushButton_stop_2.pressed.connect(self.stop_master_2)

        self.ui_main_window.pushButton_Save_data.pressed.connect(self.save_fale_bool_foo)

        # self.foo_start_QThread() # запуск потока для графика
        # self.prob_read() # Запуск потока, смотрит выходное значение газа

        # ---------------- Вспомогательные ------------------------

        self.find_com_port_foo() # Поиск активных COM порт и записывает в ComboBox

        # ---------------- Логика программы ------------------------

        self.ui_main_window.graphicsView_FS_1.setLabel('bottom', 'Time', color='g', **{'font-size':'12pt'})   # Название осей
        self.ui_main_window.graphicsView_FS_1.getAxis('bottom').setPen(pg.mkPen(color=(128, 128, 128), width=3))

        self.ui_main_window.graphicsView_FS_1.setLabel('left', 'Gas Flow', units='l/h', color='r', **{'font-size': '12pt'})
        self.ui_main_window.graphicsView_FS_1.getAxis('left').setPen(pg.mkPen(color=(0, 100, 0), width=3))
        # self.ui_main_window.graphicsView_FS_1.setTitle('The first')        # Название графика


    def save_fale_bool_foo(self):
        self.worker_F_M.save_fale_bool = True

    def Change_from_SpinBox_value_1(self):
        buff = self.ui_main_window.doubleSpinBox_value_1.value()
        buff = round(32000*(buff-self.F1_CAPACITY_000)/(self.F1_CAPACITY_100-self.F1_CAPACITY_000))
        if self.what_change_1:
            self.what_change_1 = False
            self.Change_1_all_things(buff)
            self.Chenger_setpoint(self.ui_main_window.textEdit_1, 1, self.master_1, buff)
            self.what_change_1 = True

    def Change_from_SpinBox_value_2(self):
        buff = self.ui_main_window.doubleSpinBox_value_2.value()
        buff = round(32000*(buff-self.F2_CAPACITY_000)/(self.F2_CAPACITY_100-self.F2_CAPACITY_000))
        if self.what_change_2:
            self.what_change_2 = False
            self.Change_2_all_things(buff)
            self.Chenger_setpoint(self.ui_main_window.textEdit_2, 2, self.master_2, buff)
            self.what_change_2 = True


    def Change_from_SpinBox_persent_1(self):
        buff = self.ui_main_window.doubleSpinBox_persent_1.value()
        buff = round(buff*320)
        if self.what_change_1:
            self.what_change_1 = False
            self.Change_1_all_things(buff)
            self.Chenger_setpoint(self.ui_main_window.textEdit_1, 1, self.master_1, buff)
            self.what_change_1 = True

    def Change_from_SpinBox_persent_2(self):
        buff = self.ui_main_window.doubleSpinBox_persent_2.value()
        buff = round(buff*320)

        if self.what_change_2:
            self.what_change_2 = False
            self.Change_2_all_things(buff)
            self.Chenger_setpoint(self.ui_main_window.textEdit_2, 2, self.master_2, buff)
            self.what_change_2 = True

    def Change_Slider_1(self):
        buff = self.ui_main_window.verticalSlider_1.value()
        self.value_scrolbar_1 = buff

        if self.what_change_1:
            self.what_change_1 = False
            self.Change_1_all_things(buff)
            self.Chenger_setpoint(self.ui_main_window.textEdit_1, 1, self.master_1, buff)
            self.what_change_1 = True

    def Change_Slider_2(self):
        buff = self.ui_main_window.verticalSlider_2.value()
        self.value_scrolbar_2 = buff

        if self.what_change_2:
            self.what_change_2 = False
            self.Change_2_all_things(buff)
            self.Chenger_setpoint(self.ui_main_window.textEdit_2, 2, self.master_2, buff)
            self.what_change_2 = True


    def Change_1_all_things(self, buff):
        # buff от 0 до 32000
        self.ui_main_window.verticalSlider_1.setValue(buff)
        # self.ui_main_window.progressBar_1.setValue(int(round(buff/320)))
        self.ui_main_window.doubleSpinBox_persent_1.setValue(buff/320)
        # self.F2_CAPACITY_000 self.F2_CAPACITY_100
        self.ui_main_window.doubleSpinBox_value_1.setValue(buff/32000*(self.F1_CAPACITY_100-self.F1_CAPACITY_000)
                                                           + self.F1_CAPACITY_000)
        # self.ui_main_window.lineEdit_value_1.clear()
        # self.ui_main_window.lineEdit_value_1.insert(str(round(buff/32000*(self.F1_CAPACITY_100-self.F1_CAPACITY_000)
        #                                                    + self.F1_CAPACITY_000, 2)))

    def Change_2_all_things(self, buff):
        # buff от 0 до 32000
        self.ui_main_window.verticalSlider_2.setValue(buff)
        # self.ui_main_window.progressBar_2.setValue(int(round(buff/320)))
        self.ui_main_window.doubleSpinBox_persent_2.setValue(buff/320)
        # self.F2_CAPACITY_000 self.F2_CAPACITY_100
        self.ui_main_window.doubleSpinBox_value_2.setValue(buff/32000*(self.F2_CAPACITY_100-self.F2_CAPACITY_000)
                                                           + self.F2_CAPACITY_000)
        # self.ui_main_window.lineEdit_value_2.clear()
        # self.ui_main_window.lineEdit_value_2.insert(str(round(buff/32000*(self.F2_CAPACITY_100-self.F2_CAPACITY_000)
        #                                                    + self.F2_CAPACITY_000, 2)))


    def Chenger_setpoint(self, textEdit_here, number_flow, master_two, val_chang):

        SetPoin = [{'proc_nr': 1, 'parm_nr': 1, 'parm_type': propar.PP_TYPE_INT16, 'data': 32000}]  # SETPOINT

        # Номер узла self.nodes[0]['address'] не знаю зачем он
        values = master_two.write(self.nodes[0]['address'], 1, 1, propar.PP_TYPE_INT16, val_chang)
        # print(values)

        user_tag = master_two.read(self.nodes[0]['address'], 1, 1, propar.PP_TYPE_INT16)
        print(f"SETPOINT {user_tag}")
        # self.write_textEdit(f"SETPOINT {user_tag}",textEdit_here)
        self.write_textEdit("\n", textEdit_here)



    def foo_stop_QThread(self):
        self.worker.exit_worker = True
        self.worker.stop_QTheath_in_worker()


    def exit_prog(self):
        if not self.do_tread_run_1:
            self.flow_worker_f1.exit_worker = True
            self.write_textEdit(f"The Master is out" + "\n", self.ui_main_window.textEdit_1)
            print(f"The Master is out F1" + "\n")
            self.flow_worker_f1.change_to_zero()

        if not self.do_tread_run_2:
            self.flow_worker_f2.exit_worker = True
            self.write_textEdit(f"The Master is out" + "\n", self.ui_main_window.textEdit_2)
            print(f"The Master is out F2" + "\n")
            self.flow_worker_f2.change_to_zero()

        sys.exit(app.exec_())


    def start_master_1(self):
        if self.do_tread_run_1:
            self.tread_and_connect(1)

        self.flow_worker_f1.COM_port_signal.emit(self.ui_main_window.comboBox.currentText(),
                                                 self.ui_main_window.textEdit_1,
                                                 self.ui_main_window.doubleSpinBox_value_1,
                                                 self.ui_main_window.lineEdit_temperature_1,
                                                 self.ui_main_window.verticalSlider_1,
                                                 self.ui_main_window.doubleSpinBox_persent_1)

        # self.flow_worker_f1.progress_run_worker_signal.emit()

    def start_master_2(self):
        if self.do_tread_run_2:
            self.tread_and_connect(2)

        self.flow_worker_f2.COM_port_signal.emit(self.ui_main_window.comboBox_2.currentText(),
                                                 self.ui_main_window.textEdit_2,
                                                 self.ui_main_window.doubleSpinBox_value_2,
                                                 self.ui_main_window.lineEdit_temperature_2,
                                                 self.ui_main_window.verticalSlider_2,
                                                 self.ui_main_window.doubleSpinBox_persent_2)

        # self.flow_worker_f2.progress_run_worker_signal.emit()





    def chenge_SpinBox(self, doubleSpinBox_value_here, max, min):
        SpinBox = doubleSpinBox_value_here
        SpinBox.setMaximum(max)
        SpinBox.setMinimum(min)
        SpinBox.setSingleStep((max-min)/3200)


    def stop_master_1(self):
        self.do_tread_run_1 = True
        self.write_textEdit(f"The Master is out" + "\n",  self.ui_main_window.textEdit_1)
        self.flow_worker_f1.exit_worker = True
        self.flow_worker_f1.stop_QTheath_in_worker()

    def stop_master_2(self):
        self.do_tread_run_2 = True
        self.write_textEdit(f"The Master is out" + "\n",  self.ui_main_window.textEdit_2)
        self.flow_worker_f2.exit_worker = True
        self.flow_worker_f2.stop_QTheath_in_worker()

    def exit_master_two(self, COM_port, textEdit_here, number_flow, master_two):
        # SetPoin = {'proc_nr': 1, 'parm_nr': 1, 'parm_type': propar.PP_TYPE_INT16, 'data': 0}  # SETPOINT
        values = master_two.write(self.nodes[0]['address'], 1, 1, propar.PP_TYPE_INT16, 0)
        print(values)
        master_two.stop()
        self.write_textEdit(f"The Master is out" + "\n", textEdit_here)


    def change_point_worker_1(self):
        if not self.F1_bool_MT:
            self.worker.new_point_m0 = 0
        else:
            self.temper_f1 = self.master_1.read(self.nodes[0]['address'], 33, 7, propar.PP_TYPE_FLOAT)  # Температура
            name = self.master_1.read(self.nodes[0]['address'], 1, 17, propar.PP_TYPE_STRING)  # FLUID NAME
            self.ui_main_window.lineEdit_temperature_1.clear()
            self.ui_main_window.lineEdit_temperature_1.insert("  " + name + "  " + str(round(self.temper_f1, 2)) + " °C")

            # time.sleep(0.1)
            # print(f"Temperature {temper}")

            # {'proc_nr': 33, 'parm_nr': 7, 'parm_type': propar.PP_TYPE_FLOAT}
            user_tag = self.master_1.read(self.nodes[0]['address'], 1, 1, propar.PP_TYPE_INT16) # SetPoint
            # user_tag = self.master_1.read(self.nodes[0]['address'], 33, 0, propar.PP_TYPE_FLOAT)  # F_MEASURE_Thread


            for k in range(3):
                if user_tag is None:
                    user_tag = self.master_1.read(self.nodes[0]['address'], 1, 1, propar.PP_TYPE_INT16)
                    print(f"Problem None №{k}")
                    time.sleep(0.1)

                    self.stop_master_1()
                    time.sleep(0.2)
                    self.start_master_1()
                    time.sleep(0.2)
                    self.Change_Slider_1()

                else:
                    break

            if self.value_scrolbar_1 != user_tag:
                self.Change_Slider_1()

                if self.value_scrolbar_1 != user_tag:
                    self.stop_master_1()
                    time.sleep(0.2)
                    self.start_master_1()
                    time.sleep(0.2)
                    self.Change_Slider_1()

            # self.worker.new_point_m1 = user_tag/32000*(self.F1_CAPACITY_100-self.F1_CAPACITY_000)+self.F1_CAPACITY_000
            user_tag = self.master_1.read(self.nodes[0]['address'], 33, 0, propar.PP_TYPE_FLOAT)  # F_MEASURE_Thread
            self.worker.new_point_m1 = user_tag

    def change_point_worker_2(self):
        if not self.F2_bool_MT:
            self.worker.new_point_m2 = 0
        else:
            self.temper_f2 = self.master_2.read(self.nodes[0]['address'], 33, 7, propar.PP_TYPE_FLOAT)  # Температура
            name = self.master_2.read(self.nodes[0]['address'], 1, 17, propar.PP_TYPE_STRING)  # FLUID NAME
            self.ui_main_window.lineEdit_temperature_2.clear()
            self.ui_main_window.lineEdit_temperature_2.insert("  " + name + "  " + str(round(self.temper_f2, 2)) + " °C")

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
                    self.Change_Slider_2()

                else:
                    break

            if self.value_scrolbar_2 != user_tag:
                self.Change_Slider_2()

                if self.value_scrolbar_2 != user_tag:
                    self.stop_master_2()
                    time.sleep(0.2)
                    self.start_master_2()
                    time.sleep(0.2)
                    self.Change_Slider_2()

            # self.worker.new_point_m2 = user_tag/32000*(self.F2_CAPACITY_100-self.F2_CAPACITY_000)+self.F2_CAPACITY_000
            user_tag = self.master_2.read(self.nodes[0]['address'], 33, 0, propar.PP_TYPE_FLOAT)  # F_MEASURE_Thread
            self.worker.new_point_m2 = user_tag

    def point_nun_cry_m1(self):
        data_point_nan = datetime.now().strftime("%X")
        self.write_textEdit(f"Nan point {data_point_nan}" + "\n", self.ui_main_window.textEdit_1)

    def point_nun_cry_m2(self):
        data_point_nan = datetime.now().strftime("%X")
        self.write_textEdit(f"Nan point {data_point_nan}" + "\n", self.ui_main_window.textEdit_2)



    def find_com_port_foo(self):    # Поиск активных COM порт и записывает в ComboBox
        self.ui_main_window.comboBox.clear()
        self.ui_main_window.comboBox_2.clear()
        self.ui_main_window.comboBox.addItems(f_c.serial_ports())
        self.ui_main_window.comboBox.setCurrentIndex(1)
        self.ui_main_window.comboBox_2.addItems(f_c.serial_ports())
        self.ui_main_window.comboBox_2.setCurrentIndex(2)

    bool_thread_garph = False # Запущен поток для графика?
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
        self.worker_G.graph_signal.connect(self.paint_graph_in_canvas)
        self.worker_G.read_point_f1_signal.connect(self.paint_graph_in_canvas)
        # self.worker_G.read_F_MEASURE_signal.connect(self.read_F_MEASURE)
        # self.worker_G.data_all_signal.connect(self.data_to_thread)

        # --------------------------------------------------------
        self.Thread_G.started.connect(self.worker_G.run_master)
        self.Thread_G.start()


    def paint_graph_in_canvas(self, x_t_plot_name_here, y_main_plot_m1_here, y_main_plot_m2_here,
                              time_size_here, ticks_here, bool_f1, bool_f2):

        xax = self.ui_main_window.graphicsView_FS_1.getAxis('bottom')

        if len(x_t_plot_name_here) <= time_size_here:
            range_there = len(x_t_plot_name_here)
        else:
            range_there = time_size_here

        xax.setTicks([ticks_here[0][-range_there:]])
        max_y_buff = max(self.F1_CAPACITY_100, self.F2_CAPACITY_100)
        self.ui_main_window.graphicsView_FS_1.setYRange(0, max_y_buff)

        if bool_f1:
            self.ui_main_window.graphicsView_FS_1.plot(np.array(x_t_plot_name_here[-range_there:]),
                                                   np.array(y_main_plot_m1_here[-range_there:]),
                                                   pen=pg.mkPen((255, 69, 0), width=2), name="l/h", clear=True)
        if bool_f2:
            self.ui_main_window.graphicsView_FS_1.plot(np.array(x_t_plot_name_here[-range_there:]),
                                                   np.array(y_main_plot_m2_here[-range_there:]),
                                                   pen=pg.mkPen((0, 102, 255), width=2), name="l/h")

        # x = np.random.normal(size=1000)
        # y = np.random.normal(size=1000)
        # self.ui_main_window.graphicsView_FS_1.plot(x, y, pen=None, symbol='o')  # Рисует кружки



    def button_pushed_range(self):
        # Ограничение по y (по времени)
        self.ui_main_window.graphicsView_FS_1.setXRange(0, 100, padding=0, update=True)
        self.ui_main_window.graphicsView_FS_1.setYRange(0, 100, padding=0, update=True)
        # Точка на графике
        x_t = np.arange(100)
        y_t = np.random.normal(size=100)
        self.ui_main_window.graphicsView_FS_1.plot(x_t, y_t, pen=pg.mkPen('r', width=2))

    def write_textEdit(self, test, test_Edit):
        test_Edit.insertPlainText(test)
        test_Edit.verticalScrollBar().setSliderPosition(test_Edit.verticalScrollBar().maximum())

    def prob_read(self):
        # ---------------- Запуск потоков ------------------------
        # Step 2: Create a QThread object
        self.Thread_F_MEASURE = QThread()
        # Step 3: Create a worker object
        self.worker_F_M = mp_f.Worker_class()
        # Step 4: Move worker to the thread
        self.worker_F_M.moveToThread(self.Thread_F_MEASURE)
        # Step 5: Connect signals and slots
        # self.thread.started.connect(self.worker.run)
        self.worker_F_M.finished.connect(self.Thread_F_MEASURE.quit)
        self.worker_F_M.finished.connect(self.worker_F_M.deleteLater)
        self.Thread_F_MEASURE.finished.connect(self.Thread_F_MEASURE.deleteLater)
        # Step 6: Start the Thread_F_MEASURE
        # self.Thread_F_MEASURE.start()

        # ------------ Сигналы и слоты ---------------------------
        self.worker_F_M.read_F_MEASURE_signal.connect(self.read_F_MEASURE)
        self.worker_F_M.data_all_signal.connect(self.data_to_thread)

        # --------------------------------------------------------
        self.Thread_F_MEASURE.started.connect(self.worker_F_M.run_worker)
        self.Thread_F_MEASURE.start()

        # buff = self.master_1.read(self.nodes[0]['address'], 33, 0, propar.PP_TYPE_FLOAT)  # F_MEASURE_Thread
        # self.write_textEdit(f"Valve output {buff}\n", self.ui_main_window.textEdit_1)

    def data_to_thread(self):
        self.worker_F_M.value_f1 = self.worker.y_main_plot_m1[-10]/10
        self.worker_F_M.value_f2 = self.worker.y_main_plot_m2[-10]/10

        self.worker_F_M.Gas_consumption_f1 = self.worker.gas_consumption_m1
        self.worker_F_M.Gas_consumption_f2 = self.worker.gas_consumption_m2

        self.worker_F_M.Temperature_f1 = self.temper_f1
        self.worker_F_M.Temperature_f2 = self.temper_f2

    def read_F_MEASURE(self):
        if self.F1_bool_MT:
            buff = self.master_1.read(self.nodes[0]['address'], 33, 0, propar.PP_TYPE_FLOAT)  # F_MEASURE_Thread
            # self.write_textEdit(f"Valve output {buff}\n", self.ui_main_window.textEdit_1)
            self.ui_main_window.lineEdit_value_1.clear()
            self.ui_main_window.lineEdit_value_1.insert(str(round(buff, 2)))
            self.ui_main_window.progressBar_1.setValue(int(round(buff/self.F1_CAPACITY_100*100))) # скрол бар

            self.ui_main_window.lineEdit_gas_1.clear()
            self.ui_main_window.lineEdit_gas_1.insert("  Gas_consumption " +
                                                      str(round(self.worker.gas_consumption_m1, 2)) + " liters")

        if self.F2_bool_MT:
            buff = self.master_2.read(self.nodes[0]['address'], 33, 0, propar.PP_TYPE_FLOAT)  # F_MEASURE_Thread
            # self.write_textEdit(f"Valve output {buff}\n", self.ui_main_window.textEdit_1)
            self.ui_main_window.lineEdit_value_2.clear()
            self.ui_main_window.lineEdit_value_2.insert(str(round(buff, 2)))
            self.ui_main_window.progressBar_2.setValue(int(round(buff/self.F2_CAPACITY_100*100))) # скрол бар

            self.ui_main_window.lineEdit_gas_2.clear()
            self.ui_main_window.lineEdit_gas_2.insert("  Gas_consumption " +
                                                      str(round(self.worker.gas_consumption_m2, 2)) + " liters")

    def tread_and_connect(self, name_thread_nubmer):

        if name_thread_nubmer == 1:
            self.do_tread_run_1 = False
            COM_port = self.ui_main_window.comboBox.currentText()
            # ---------------- Запуск потоков ------------------------
            # Step 2: Create a QThread object
            self.Thread_macter_f1 = QThread()
            # Step 3: Create a worker object
            self.flow_worker_f1 = w_c.Flow_worker_class()
            # Step 4: Move worker to the thread
            self.flow_worker_f1.moveToThread(self.Thread_macter_f1)
            # Step 5: Connect signals and slots
            # self.thread.started.connect(self.worker.run)
            self.flow_worker_f1.finished.connect(self.Thread_macter_f1.quit)
            self.flow_worker_f1.finished.connect(self.flow_worker_f1.deleteLater)
            self.Thread_macter_f1.finished.connect(self.Thread_macter_f1.deleteLater)
            # Step 6: Start the Thread_F_MEASURE
            self.Thread_macter_f1.start()
            name = self.flow_worker_f1

        if name_thread_nubmer == 2:
            self.do_tread_run_2 = False
            COM_port = self.ui_main_window.comboBox_2.currentText()
            # ---------------- Запуск потоков ------------------------
            # Step 2: Create a QThread object
            self.Thread_macter_f2 = QThread()
            # Step 3: Create a worker object
            self.flow_worker_f2 = w_c.Flow_worker_class()
            # Step 4: Move worker to the thread
            self.flow_worker_f2.moveToThread(self.Thread_macter_f2)
            # Step 5: Connect signals and slots
            # self.thread.started.connect(self.worker.run)
            self.flow_worker_f2.finished.connect(self.Thread_macter_f2.quit)
            self.flow_worker_f2.finished.connect(self.flow_worker_f2.deleteLater)
            self.Thread_macter_f2.finished.connect(self.Thread_macter_f2.deleteLater)
            # Step 6: Start the Thread_F_MEASURE
            self.Thread_macter_f2.start()
            name = self.flow_worker_f2

        # ------------ Сигналы и слоты потока ---------------------------
        # name.progress_test_2.connect(lambda: name.run_connect_and_master(" da"))
        # name.progress_test.connect(self.write_test_new_tread)
        name.chenge_SpinBox_signal.connect(self.chenge_SpinBox)
        # name.graph_signal.connect(self.paint_graph_in_canvas)
        name.progress_run_worker_signal.connect(name.run_worker)
        # name.name_flow_signal.connect() дописать

        name.COM_port_signal.connect(name.run_master)
        name.write_textEdit_signal.connect(self.write_textEdit)
        name.lineEdit_temperature_singal.connect(self.lineEdit_temperature_clear_and_write)

        # ----------------------- Кнопки --------------------------------
        self.ui_main_window.pushButton_run_test.pressed.connect(name.run_worker)
        # self.flow_worker.read_F_MEASURE_signal.connect(self.read_F_MEASURE)

        # ---------------------------------------------------------------
        # self.Thread_macter.started.connect(self.flow_worker.run_worker)
        # self.Thread_macter.start()


    def write_test_new_tread(self, buff):
        self.write_textEdit(f"Valve output {buff}\n", self.ui_main_window.textEdit_1)

    def lineEdit_temperature_clear_and_write(self, buff_name, buff_temper, lineEdit_temperature_here):
        lineEdit_temperature_here.clear()
        lineEdit_temperature_here.insert(
            "  " + buff_name + "  " + str(round(buff_temper, 2)) + " °C")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    program = testapp()
    program.launch()
    sys.exit(app.exec_())






