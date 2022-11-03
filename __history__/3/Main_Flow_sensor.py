import sys
import propar

import time
import Find_com_port as f_c
import My_Processing as mp  # Класс для потока
import Worker_F_MEASURE_Thread as mp_f  # Класс для потока
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

        self.ui_main_window.pushButton_Start_monitoring.pressed.connect(self.foo_start_QThread)
        self.ui_main_window.pushButton_Stop_monitoring.pressed.connect(self.foo_stop_QThread)

        self.ui_main_window.verticalSlider_1.valueChanged.connect(self.Change_Slider_1)  # Скрол бары
        self.ui_main_window.verticalSlider_2.valueChanged.connect(self.Change_Slider_2)  # Скрол бары

        self.ui_main_window.doubleSpinBox_persent_1.editingFinished.connect(self.Change_from_SpinBox_persent_1) # Проценты
        self.ui_main_window.doubleSpinBox_persent_2.editingFinished.connect(self.Change_from_SpinBox_persent_2) # Проценты

        self.ui_main_window.doubleSpinBox_value_1.editingFinished.connect(self.Change_from_SpinBox_value_1) # Значения
        self.ui_main_window.doubleSpinBox_value_2.editingFinished.connect(self.Change_from_SpinBox_value_2) # Значения

        self.ui_main_window.pushButton_prob_1.pressed.connect(self.foo_new)
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

        self.ui_main_window.pushButton_Save_data.pressed.connect(self.save_fale_bool_foo)

        self.foo_start_QThread() # запуск потока для графика
        self.prob_read() # Запуск потока, смотрит выходное значение газа

        # ---------------- Вспомогательные ------------------------

        self.find_com_port_foo() # Поиск активных COM порт и записывает в ComboBox

        # ---------------- Логика программы ------------------------

        self.ui_main_window.graphicsView_FS_1.setLabel('bottom', 'Time', color='g', **{'font-size':'12pt'})   # Название осей
        self.ui_main_window.graphicsView_FS_1.getAxis('bottom').setPen(pg.mkPen(color=(128, 128, 128), width=3))

        self.ui_main_window.graphicsView_FS_1.setLabel('left', 'Gas Flow', units='l/h', color='r', **{'font-size': '12pt'})
        self.ui_main_window.graphicsView_FS_1.getAxis('left').setPen(pg.mkPen(color=(0, 100, 0), width=3))
        # self.ui_main_window.graphicsView_FS_1.setTitle('The first')        # Название графика

        buff_textE = self.ui_main_window.textEdit_2

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
        self.worker.new_point_m1_signal.connect(self.change_point_worker_1)  # Изменение точки на графике
        self.worker.new_point_m2_signal.connect(self.change_point_worker_2)  # Изменение точки на графике
        self.worker.if_nan_point_signal_m1.connect(self.point_nun_cry_m1)
        self.worker.if_nan_point_signal_m1.connect(self.point_nun_cry_m2)
        # self.worker.test_signal_worker.connect(self.func22)

        self.worker.exit_worker = False

        self.thread.started.connect(self.worker.run_worker)
        self.thread.start()

    def foo_stop_QThread(self):
        self.worker.exit_worker = True
        self.worker.stop_QTheath_in_worker()


    def exit_prog(self):
        if self.F1_bool_MT:
            self.master_1.write(self.nodes[0]['address'], 1, 1, propar.PP_TYPE_INT16, 0)
        if self.F2_bool_MT:
            self.master_2.write(self.nodes[0]['address'], 1, 1, propar.PP_TYPE_INT16, 0)
        time.sleep(0.5)
        sys.exit(app.exec_())

    def connect_com_run(self):
        COM_port = self.ui_main_window.comboBox.currentText()
        self.connect_com(COM_port, self.ui_main_window.textEdit_1, 1)

    def connect_com_run_2(self):
        COM_port = self.ui_main_window.comboBox_2.currentText()
        self.connect_com(COM_port, self.ui_main_window.textEdit_2, 2)

    def connect_com(self, COM_port, textEdit_here, number_flow):
     # Версия без использования мастера, почему-то не работает изменение параметров     ''' '''
        self.worker.checking_connection(COM_port, number_flow) # Подключение к расходомеру
        if number_flow == 1:
            el_foo = self.worker.el_flow_1
        if number_flow == 2:
            el_foo = self.worker.el_flow_2
        print(el_foo.measure)
        if el_foo.measure != None:
            # self.ui_main_window.comboBox.setEnabled(False) # Зажим кнопки
            self.write_textEdit("Successful connection\n", textEdit_here)
        else:
            self.write_textEdit("Not successful connection\n", textEdit_here)
            return
        name = el_foo.read_parameters([{'proc_nr': 1, 'parm_nr': 17, 'parm_type': propar.PP_TYPE_STRING}])  # Что за газ
        self.write_textEdit(f'It is %s' %(name[0]['data'])+"\n", textEdit_here)

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
        self.write_textEdit("\n", textEdit_here)
        for value in values:
            print(value)
            print(value['data'])
            self.write_textEdit(f'{ value["data"] }' + "\n", textEdit_here)
        print(values[3]['data'])


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

        self.write_textEdit(f"The Master runs"+"\n", textEdit_here)

        # Create the master
        # master_two = propar.master(COM_port, 38400)

        # Get nodes on the network
        self.nodes = master_two.get_nodes()

        # Read the usertag of all nodes
        for node in self.nodes:
            if number_flow == 1:
                self.F1_bool_MT = True
            if number_flow == 2:
                self.F2_bool_MT = True

            user_tag = master_two.read(node['address'], 113, 6, propar.PP_TYPE_STRING)
            print(node['address'])
            print(user_tag)
            # {'proc_nr': 1, 'parm_nr': 17, 'parm_type': propar.PP_TYPE_STRING},  # FLUID NAME
            user_tag = master_two.read(node['address'], 1, 17, propar.PP_TYPE_STRING)
            # Костыль
            if number_flow == 1:
                self.worker_F_M.name_F1 = user_tag
            if number_flow == 2:
                self.worker_F_M.name_F2 = user_tag

            print(user_tag)
            self.write_textEdit(f"{user_tag}" + "\n", textEdit_here)

            user_tag = master_two.read(node['address'], 1, 1, propar.PP_TYPE_INT16)
            print(f"SETPOINT {user_tag}")
            # self.write_textEdit(f"SETPOINT {user_tag}" + "\n", textEdit_here)

            user_tag = master_two.write(node['address'], 1, 4, propar.PP_TYPE_INT8, 0) # BUS/RS232
            # user_tag = master_two.read(node['address'], 1, 4, propar.PP_TYPE_INT8)  # BUS/RS232
            print(user_tag)
            self.write_textEdit(f"Control mode {user_tag}" + "\n", textEdit_here)

            if number_flow == 1:
                self.F1_CAPACITY_100 = master_two.read(self.nodes[0]['address'], 1, 13,
                                                  propar.PP_TYPE_FLOAT)  # CAPACITY 100%
                self.F1_CAPACITY_000 = master_two.read(self.nodes[0]['address'], 33, 22,
                                                  propar.PP_TYPE_FLOAT)  # CAPACITY 0%
                self.chenge_SpinBox(number_flow, self.F1_CAPACITY_100, self.F1_CAPACITY_000)

            if number_flow == 2:
                self.F2_CAPACITY_100 = master_two.read(self.nodes[0]['address'], 1, 13,
                                                  propar.PP_TYPE_FLOAT)  # CAPACITY 100%
                self.F2_CAPACITY_000 = master_two.read(self.nodes[0]['address'], 33, 22,
                                                  propar.PP_TYPE_FLOAT)  # CAPACITY 0%
                self.chenge_SpinBox(number_flow, self.F2_CAPACITY_100, self.F2_CAPACITY_000)



    def chenge_SpinBox(self, number_flow, max, min):
        if number_flow == 1:
            SpinBox = self.ui_main_window.doubleSpinBox_value_1

        if number_flow == 2:
            SpinBox = self.ui_main_window.doubleSpinBox_value_2

        SpinBox.setMaximum(max)
        SpinBox.setMinimum(min)
        SpinBox.setSingleStep((max-min)/3200)


    def stop_master_1(self):
        COM_port = self.ui_main_window.comboBox.currentText()
        self.exit_master_two(COM_port, self.ui_main_window.textEdit_1, 1, self.master_1)

    def stop_master_2(self):
        COM_port = self.ui_main_window.comboBox_2.currentText()
        self.exit_master_two(COM_port, self.ui_main_window.textEdit_2, 2, self.master_2)

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


    def paint_graph_in_canvas(self):
        xax = self.ui_main_window.graphicsView_FS_1.getAxis('bottom')
        # print(self.worker.a_f, self.worker.a_l)
        # print(self.worker.ticks[0][self.worker.a_f:self.worker.a_l])

        if len(self.worker.x_t_plot_name) <= self.worker.time_size:
            range_there = len(self.worker.x_t_plot_name)
        else:
            range_there = self.worker.time_size

        xax.setTicks([self.worker.ticks[0][-range_there:]])
        max_y_buff = max(self.F1_CAPACITY_100, self.F2_CAPACITY_100)
        self.ui_main_window.graphicsView_FS_1.setYRange(0, max_y_buff)

        time.sleep(0.3)
        if self.F1_bool_MT:
            self.ui_main_window.graphicsView_FS_1.plot(np.array(self.worker.x_t_plot_name[-range_there:]),
                                                       np.array(self.worker.y_main_plot_m1[-range_there:]),
                                                       pen=pg.mkPen((255, 69, 0), width=2), name="l/h", clear=True)

        buff = list([])
        for k in range(range_there):
            buff.append(k)

        # x = np.random.normal(size=1000)
        # y = np.random.normal(size=1000)
        # self.ui_main_window.graphicsView_FS_1.plot(x, y, pen=None, symbol='o')  # Рисует кружки

        if self.F2_bool_MT:
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

    def foo_new(self):
        self.write_textEdit(f"Valve output {self.F1_CAPACITY_100}\n", self.ui_main_window.textEdit_1)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    program = testapp()
    program.launch()
    sys.exit(app.exec_())






