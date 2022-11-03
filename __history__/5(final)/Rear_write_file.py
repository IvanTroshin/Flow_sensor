import sys
import time
from datetime import datetime
import os



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