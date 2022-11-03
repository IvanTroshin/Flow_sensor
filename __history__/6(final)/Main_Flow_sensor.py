import sys

import Find_com_port as f_c
import Worker_connect as w_c  # Класс для потока
import Worker_graph as w_g

from gui.qt_io import Ui_MainWindow
import pyqtgraph as pg
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtCore import *

pg.setConfigOption('background', 'w')


class testapp(QObject):

    def __init__(self, parent=None):
        super(testapp, self).__init__(parent)
        self.ui_main_window = None
        self.main_window = None

    F1_CAPACITY_100 = 0  # Максимальное значение вервого расходомера
    F1_CAPACITY_000 = 0  # Минимальное значение вервого расходомера

    F2_CAPACITY_100 = 0  # Максимальное значение вервого расходомера
    F2_CAPACITY_000 = 0  # Минимальное значение вервого расходомера

    value_scrolbar_1 = 0  # сохраниет значение расхода от 0 до 32000
    value_scrolbar_2 = 0  # сохраниет значение расхода от 0 до 32000

    what_change_1 = True  # Нужен чтобы изменялся один раз все параметры
    what_change_2 = True  # Нужен чтобы изменялся один раз все параметры

    F1_bool_MT = False  # Для потока на выходе
    F2_bool_MT = False  # Для потока на выходе

    do_tread_run_1 = True  # Запущен ли поток
    do_tread_run_2 = True  # Запущен ли поток

    come_port_f1 = 0
    come_port_f2 = 0

    def launch(self):
        # инициация и демонстрация интерфейса
        self.main_window = QtWidgets.QMainWindow()
        self.ui_main_window = Ui_MainWindow()
        self.ui_main_window.setupUi(self.main_window)
        self.main_window.show()

        # ----------------- Кнопки ------------------------------

        self.ui_main_window.actionFind_com_port.triggered.connect(
            self.find_com_port_foo)  # Поиск активных COM порт и записывает в ComboBox
        self.ui_main_window.pushButton_Close.pressed.connect(self.exit_prog)

        self.ui_main_window.verticalSlider_1.valueChanged.connect(self.Change_Slider_1)  # Скрол бары
        self.ui_main_window.verticalSlider_2.valueChanged.connect(self.Change_Slider_2)  # Скрол бары

        self.ui_main_window.doubleSpinBox_persent_1.editingFinished.connect(
            self.Change_from_SpinBox_persent_1)  # Проценты
        self.ui_main_window.doubleSpinBox_persent_2.editingFinished.connect(
            self.Change_from_SpinBox_persent_2)  # Проценты

        self.ui_main_window.doubleSpinBox_value_1.editingFinished.connect(self.Change_from_SpinBox_value_1)  # Значения
        self.ui_main_window.doubleSpinBox_value_2.editingFinished.connect(self.Change_from_SpinBox_value_2)  # Значения

        self.ui_main_window.pushButton_Start_1.pressed.connect(self.start_master_1)
        self.ui_main_window.pushButton_stop_1.pressed.connect(self.stop_master_1)

        self.ui_main_window.pushButton_Start_2.pressed.connect(self.start_master_2)
        self.ui_main_window.pushButton_stop_2.pressed.connect(self.stop_master_2)

        # ---------------- Вспомогательные ------------------------

        self.find_com_port_foo()  # Поиск активных COM порт и записывает в ComboBox

        # ---------------- Логика программы ------------------------

        self.ui_main_window.graphicsView_FS_1.setLabel('bottom', 'Time', color='g',
                                                       **{'font-size': '12pt'})  # Название осей
        self.ui_main_window.graphicsView_FS_1.getAxis('bottom').setPen(pg.mkPen(color=(128, 128, 128), width=3))

        self.ui_main_window.graphicsView_FS_1.setLabel('left', 'Gas Flow', units='l/h', color='r',
                                                       **{'font-size': '12pt'})
        self.ui_main_window.graphicsView_FS_1.getAxis('left').setPen(pg.mkPen(color=(0, 100, 0), width=3))
        # self.ui_main_window.graphicsView_FS_1.setTitle('The first')        # Название графика

    def Change_from_SpinBox_value_1(self):
        buff = self.ui_main_window.doubleSpinBox_value_1.value()
        buff = round(32000 * (buff - self.F1_CAPACITY_000) / (self.F1_CAPACITY_100 - self.F1_CAPACITY_000))
        if self.what_change_1:
            self.what_change_1 = False
            self.Change_1_all_things(buff)
            self.what_change_1 = True

    def Change_from_SpinBox_value_2(self):
        buff = self.ui_main_window.doubleSpinBox_value_2.value()
        buff = round(32000 * (buff - self.F2_CAPACITY_000) / (self.F2_CAPACITY_100 - self.F2_CAPACITY_000))
        if self.what_change_2:
            self.what_change_2 = False
            self.Change_2_all_things(buff)
            self.what_change_2 = True

    def Change_from_SpinBox_persent_1(self):
        buff = self.ui_main_window.doubleSpinBox_persent_1.value()
        buff = round(buff * 320)
        if self.what_change_1:
            self.what_change_1 = False
            self.Change_1_all_things(buff)
            self.what_change_1 = True

    def Change_from_SpinBox_persent_2(self):
        buff = self.ui_main_window.doubleSpinBox_persent_2.value()
        buff = round(buff * 320)
        if self.what_change_2:
            self.what_change_2 = False
            self.Change_2_all_things(buff)
            self.what_change_2 = True

    def Change_Slider_1(self):
        buff = self.ui_main_window.verticalSlider_1.value()  # Изменение расхода
        self.flow_worker_f1.chenge_val_signal.emit(buff)
        self.value_scrolbar_1 = buff

        if self.what_change_1:
            self.what_change_1 = False
            self.Change_1_all_things(buff)
            self.what_change_1 = True

    def Change_Slider_2(self):
        buff = self.ui_main_window.verticalSlider_2.value()
        self.flow_worker_f2.chenge_val_signal.emit(buff)
        self.value_scrolbar_2 = buff

        if self.what_change_2:
            self.what_change_2 = False
            self.Change_2_all_things(buff)
            print(buff)
            self.what_change_2 = True

    def Change_1_all_things(self, buff):
        # buff от 0 до 32000
        self.ui_main_window.verticalSlider_1.setValue(buff)
        self.ui_main_window.doubleSpinBox_persent_1.setValue(buff / 320)
        self.ui_main_window.doubleSpinBox_value_1.setValue(buff / 32000 * (self.F1_CAPACITY_100 - self.F1_CAPACITY_000)
                                                           + self.F1_CAPACITY_000)

    def Change_2_all_things(self, buff):
        # buff от 0 до 32000
        self.ui_main_window.verticalSlider_2.setValue(buff)
        self.ui_main_window.doubleSpinBox_persent_2.setValue(buff / 320)
        self.ui_main_window.doubleSpinBox_value_2.setValue(buff / 32000 * (self.F2_CAPACITY_100 - self.F2_CAPACITY_000)
                                                           + self.F2_CAPACITY_000)

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
        self.ui_main_window.pushButton_Start_1.setEnabled(False)
        self.ui_main_window.pushButton_stop_1.setEnabled(True)
        self.ui_main_window.pushButton_rerun_flow.setEnabled(True)
        self.ui_main_window.verticalSlider_1.setEnabled(True)
        self.ui_main_window.doubleSpinBox_persent_1.setEnabled(True)
        self.ui_main_window.doubleSpinBox_value_1.setEnabled(True)

        if self.do_tread_run_1:
            self.tread_and_connect(1)

        self.flow_worker_f1.COM_port_signal.emit(self.ui_main_window.comboBox.currentText(),
                                                 self.ui_main_window.textEdit_1,
                                                 self.ui_main_window.doubleSpinBox_value_1,
                                                 self.ui_main_window.lineEdit_temperature_1,
                                                 self.ui_main_window.verticalSlider_1,
                                                 self.ui_main_window.doubleSpinBox_persent_1,
                                                 self.ui_main_window.progressBar_1,
                                                 self.ui_main_window.lineEdit_value_1,
                                                 self.ui_main_window.lineEdit_gas_1,
                                                 self.ui_main_window.verticalSlider_1.value())

        if not self.bool_thread_garph:
            self.bool_thread_garph = True
            self.thread_garph()

        if not self.do_tread_run_1:
            self.worker_G.read_point_here_signal_f1.connect(self.flow_worker_f1.read_data, Qt.QueuedConnection)
            self.flow_worker_f1.res_signal.connect(self.worker_G.setAnswer_1, Qt.DirectConnection)
            self.worker_G.reload_signal_1.connect(self.flow_worker_f1.close_and_run_master)

    def start_master_2(self):
        self.ui_main_window.pushButton_Start_2.setEnabled(False)
        self.ui_main_window.pushButton_stop_2.setEnabled(True)
        self.ui_main_window.pushButton_rerun_flow.setEnabled(True)
        self.ui_main_window.verticalSlider_2.setEnabled(True)
        self.ui_main_window.doubleSpinBox_persent_2.setEnabled(True)
        self.ui_main_window.doubleSpinBox_value_2.setEnabled(True)

        if self.do_tread_run_2:
            self.tread_and_connect(2)

        self.flow_worker_f2.COM_port_signal.emit(self.ui_main_window.comboBox_2.currentText(),
                                                 self.ui_main_window.textEdit_2,
                                                 self.ui_main_window.doubleSpinBox_value_2,
                                                 self.ui_main_window.lineEdit_temperature_2,
                                                 self.ui_main_window.verticalSlider_2,
                                                 self.ui_main_window.doubleSpinBox_persent_2,
                                                 self.ui_main_window.progressBar_2,
                                                 self.ui_main_window.lineEdit_value_2,
                                                 self.ui_main_window.lineEdit_gas_2,
                                                 self.ui_main_window.verticalSlider_2.value())

        if not self.bool_thread_garph:
            self.bool_thread_garph = True
            self.thread_garph()

        if not self.do_tread_run_2:
            self.worker_G.read_point_here_signal_f2.connect(self.flow_worker_f2.read_data, Qt.QueuedConnection)
            self.flow_worker_f2.res_signal.connect(self.worker_G.setAnswer_2, Qt.DirectConnection)
            self.worker_G.reload_signal_2.connect(self.flow_worker_f2.close_and_run_master)

    def chenge_SpinBox(self, doubleSpinBox_value_here, max, min):
        SpinBox = doubleSpinBox_value_here
        SpinBox.setMaximum(max)
        SpinBox.setMinimum(min)
        SpinBox.setSingleStep((max - min) / 3200)

        if doubleSpinBox_value_here == self.ui_main_window.doubleSpinBox_value_1:
            self.F1_CAPACITY_100 = max
            self.F1_CAPACITY_000 = min

        if doubleSpinBox_value_here == self.ui_main_window.doubleSpinBox_value_1:
            self.F2_CAPACITY_100 = max
            self.F2_CAPACITY_000 = min

    def stop_master_1(self):
        self.ui_main_window.pushButton_Start_1.setEnabled(True)
        self.ui_main_window.pushButton_stop_1.setEnabled(False)
        if not self.do_tread_run_1:
            self.do_tread_run_1 = True
            self.write_textEdit(f"The Master is out" + "\n", self.ui_main_window.textEdit_1)
            self.flow_worker_f1.change_to_zero_signal.emit()
            self.flow_worker_f1.stop_QTheath_in_worker_signal.emit()

    def stop_master_2(self):
        self.ui_main_window.pushButton_Start_2.setEnabled(True)
        self.ui_main_window.pushButton_stop_2.setEnabled(False)
        if not self.do_tread_run_2:
            self.do_tread_run_2 = True
            self.write_textEdit(f"The Master is out" + "\n", self.ui_main_window.textEdit_2)
            self.flow_worker_f2.change_to_zero_signal.emit()
            self.flow_worker_f2.stop_QTheath_in_worker_signal.emit()

    def find_com_port_foo(self):  # Поиск активных COM порт и записывает в ComboBox
        self.ui_main_window.comboBox.clear()
        self.ui_main_window.comboBox_2.clear()
        self.ui_main_window.comboBox.addItems(f_c.serial_ports())
        self.ui_main_window.comboBox.setCurrentIndex(0)
        self.ui_main_window.comboBox_2.addItems(f_c.serial_ports())
        self.ui_main_window.comboBox_2.setCurrentIndex(1)

    bool_thread_garph = False  # Запущен поток для графика?

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
        self.worker_G.graph_signal.connect(self.paint_graph_in_canvas)
        self.worker_G.gas_consumption_signal_1.connect(self.paint_gas_consumption_1)
        self.worker_G.gas_consumption_signal_2.connect(self.paint_gas_consumption_2)
        # self.worker_G.read_F_MEASURE_signal.connect(self.read_F_MEASURE)
        # self.worker_G.data_all_signal.connect(self.data_to_thread)

        # --------------------------------------------------------
        self.Thread_G.started.connect(self.worker_G.run_worker)
        self.Thread_G.start()

    def paint_gas_consumption_1(self, value):
        self.ui_main_window.lineEdit_gas_1.clear()
        self.ui_main_window.lineEdit_gas_1.insert("  Gas_consumption " + str(round(value, 2)) + " liters")

    def paint_gas_consumption_2(self, value):
        self.ui_main_window.lineEdit_gas_2.clear()
        self.ui_main_window.lineEdit_gas_2.insert("  Gas_consumption " + str(round(value, 2)) + " liters")

    def paint_graph_in_canvas(self, x_here,
                              y_m1_here, y_m2_here,
                              time_size_here, ticks_here):

        if len(x_here) <= time_size_here:
            range_there = len(x_here)
        else:
            range_there = time_size_here

        xax = self.ui_main_window.graphicsView_FS_1.getAxis('bottom')
        xax.setTicks([ticks_here[0][-range_there:]])
        max_y_buff = max(self.F1_CAPACITY_100, self.F2_CAPACITY_100)
        self.ui_main_window.graphicsView_FS_1.setYRange(0, max_y_buff)

        # print(x_here)
        if not self.do_tread_run_1:
            self.ui_main_window.graphicsView_FS_1.plot(np.array(x_here[-range_there:]),
                                                       np.array(y_m1_here[-range_there:]),
                                                       pen=pg.mkPen((255, 69, 0), width=2), name="l/h", clear=True)

        if not self.do_tread_run_2:
            self.ui_main_window.graphicsView_FS_1.plot(np.array(x_here[-range_there:]),
                                                       np.array(y_m2_here[-range_there:]),
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

    def write_textEdit_red(self, test, test_Edit):
        test_Edit.setTextColor(QtGui.QColor(255, 0, 0))
        test_Edit.insertPlainText(test)
        test_Edit.verticalScrollBar().setSliderPosition(test_Edit.verticalScrollBar().maximum())
        test_Edit.setTextColor(QtGui.QColor(255, 255, 255))

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
        name.chenge_SpinBox_signal.connect(self.chenge_SpinBox)
        name.change_to_zero_signal.connect(name.change_to_zero)
        name.stop_QTheath_in_worker_signal.connect(name.stop_QTheath_in_worker)
        name.COM_port_signal.connect(name.run_master)
        name.write_textEdit_signal.connect(self.write_textEdit)
        name.lineEdit_temperature_singal.connect(self.lineEdit_temperature_clear_and_write)
        name.chenge_val_signal.connect(name.chenger_setpoint)
        name.chenger_progressBar_lineEdit_value_signal.connect(self.chenger_progressBar_lineEdit_value)
        name.alarm_single.connect(self.write_textEdit_red)

        # ----------------------- Кнопки --------------------------------
        self.ui_main_window.pushButton_rerun_flow.pressed.connect(name.close_and_run_master, Qt.DirectConnection)
        # self.flow_worker.read_F_MEASURE_signal.connect(self.read_F_MEASURE)

        # ---------------------------------------------------------------
        # self.Thread_macter.started.connect(self.flow_worker.run_worker)
        # self.Thread_macter.start()

    def lineEdit_temperature_clear_and_write(self, buff_name, buff_temper, lineEdit_temperature_here):
        lineEdit_temperature_here.clear()
        lineEdit_temperature_here.insert(
            "  " + buff_name + "  " + str(round(buff_temper, 2)) + " °C")

    def chenger_progressBar_lineEdit_value(self, value, max, progressBar_here, lineEdit_value_here):
        progressBar_here.setValue(int(round(value / max * 100)))
        lineEdit_value_here.clear()
        lineEdit_value_here.insert(str(round(value / max * 100, 2)))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    program = testapp()
    program.launch()
    sys.exit(app.exec_())
