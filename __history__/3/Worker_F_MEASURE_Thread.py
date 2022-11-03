import propar
import Main_Flow_sensor as Main
from PyQt5.QtCore import QObject, QThread, pyqtSignal
import time
from datetime import datetime
import os

class Worker_class(QObject):
    finished = pyqtSignal()
    read_F_MEASURE_signal = pyqtSignal()
    data_all_signal = pyqtSignal()

    gas_consumption_m1 = 0      # Общий расход газа первого
    gas_consumption_m2 = 0      # Общий расход газа второго

    name_F1 = 1 # Имя газа
    name_F2 = 2 # Имя газа

    value_f1 = 0 # Расход усреднённый
    value_f2 = 0 # Расход усреднённый

    Gas_consumption_f1 = 0
    Gas_consumption_f2 = 0

    Temperature_f1 = 0
    Temperature_f2 = 0

    exit_worker = False # Выход из run_worker

    ferst = True
    save_fale_bool = False



    def run_worker(self):
        self.time_stop_pro = datetime.now()
        while 1:
            # self.new_point = random.random()
            self.progress_here()
            # self.progress.emit()
            time.sleep(1)

            if self.save_fale_bool:
                self.time_start_pro = datetime.now()
                tdelta = self.time_start_pro - self.time_stop_pro
                if tdelta.total_seconds() > 10.0:  # Каждую 10 секунду
                    if self.ferst:
                        self.Write_data_first()
                        self.ferst = False

                    self.Write_data()
                    self.time_stop_pro = datetime.now()

            if self.exit_worker:
                # self.finished.emit()
                return


    def progress_here(self):
        self.read_F_MEASURE_signal.emit()

    def Write_data_first(self):

        dt = datetime.now()
        dt_test = dt.strftime("%d_%m_%Y")
        filename = os.getcwd() + "\\Data"
        if os.path.exists(filename):
            my_file = open(filename + "\\A_time_" + dt_test + ".txt", "a")
        else:
            os.mkdir("Data")
            my_file = open(filename + "\\A_time_" + dt_test + ".txt", "a")

        my_file.write(f"Time\t"+str(self.name_F1)+"value\t" + str(self.name_F1) +" Gas_consumption\t"+str(self.name_F1)+" Temperature\t"
                               +str(self.name_F2)+"value\t" + str(self.name_F2) +" Gas_consumption\t"+str(self.name_F2)+" Temperature\n")
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

        self.data_all_signal.emit()
        time.sleep(0.5)
        my_file.write(str(datetime.now().strftime("%X")) + "\t" +
                      str(self.value_f1) +"\t"+ str(self.Gas_consumption_f1) +"\t"+ str(self.Temperature_f1) +"\t"+
                      str(self.value_f2) +"\t"+ str(self.Gas_consumption_f2) +"\t"+ str(self.Temperature_f2) +"\n")
        # my_file.write("hello!")
        my_file.close()