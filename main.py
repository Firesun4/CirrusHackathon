from startup_script import *
import threading
import time
import matplotlib.pyplot as plt
import numpy as np


global currentValues
global timeValues
global timeStart
timeStart= time.time()
timeValues = [0]
currentValues = [[0],[0],[0],[0]]
currentTemp = [[c2c_board.get_resistor_temp_setting(1)],[c2c_board.get_resistor_temp_setting(2)],[c2c_board.get_resistor_temp_setting(3)],[c2c_board.get_resistor_temp_setting(4)]]

def main2():
    while True:
        x  = c2c_board.read_all_temps()
        maxTemp = max(x[1],x[2],x[3],x[4])
        fanOn = maxTemp > 99.65
        print(c2c_board.read_all_temps())
        if fanOn:
            c2c_board.set_all_fan_speeds(greaterThan100((maxTemp-99.65)*10))
        else:
            c2c_board.set_all_fan_speeds(0)
        currentValues1 = [0,0,0,0]
        currentTemp1 = [0,0,0,0]
       # currentFanPower1 = 0
        for p in range(1,5):
            if x[p] < 98.6:
                difference = 98.6-x[p]
                if p==1:
                    difference += 1

                if fanOn:
                    c2c_board.set_resistor_temp_setting(p,greaterThan100(20*difference))
                    currentValues1[p - 1] = c2c_board.get_resistor_temp_setting(p)
                    print("Increase by 20", c2c_board.read_all_temps())
                    currentTemp1[p-1] = c2c_board.read_temp(p)

                else:
                    c2c_board.set_resistor_temp_setting(p,greaterThan100(15*difference))
                    print("Increase by 10", c2c_board.read_all_temps())
                    currentValues1[p - 1] = c2c_board.get_resistor_temp_setting(p)
                    currentTemp1[p - 1] = c2c_board.read_temp(p)
            else:
                c2c_board.set_resistor_temp_setting(p,0)
                print("res to 0", c2c_board.read_all_temps())
                currentValues1[p - 1] = c2c_board.get_resistor_temp_setting(p)
                currentTemp1[p - 1] = c2c_board.read_temp(p)
        for p in range(4):
            currentValues[p].append(currentValues1[p])
            currentTemp[p].append(currentTemp1[p])
        timeValues.append(time.time()-timeStart)


def greaterThan100(x):
    if x>100:
        return 100
    else:
        return x


def graphingCurrent():
    plt.ion()
    while True:
        if timeValues:

            # Plot currentValues against timeValues
            plt.subplot(1, 2, 1)
            plt.xlabel("Time")
            plt.ylabel("Current")
            plt.plot(timeValues, currentValues[0], label="Resistor 1")
            plt.plot(timeValues, currentValues[1], label="Resistor 2")
            plt.plot(timeValues, currentValues[2], label="Resistor 3")
            plt.plot(timeValues, currentValues[3], label="Resistor 4")
            plt.title("Current vs time")
            plt.legend()

            plt.subplot(1, 2, 2)
            plt.xlabel("Time(s)")
            plt.ylabel("Temperature(F)")

            plt.plot(timeValues, currentTemp[0], label="Resistor 1")
            plt.plot(timeValues, currentTemp[1], label="Resistor 2")
            plt.plot(timeValues, currentTemp[2], label="Resistor 3")
            plt.plot(timeValues, currentTemp[3], label="Resistor 4")
            plt.title("Temperature vs time")
            plt.legend()

            plt.draw()
            plt.pause(0.01)
            plt.clf()
        else:
            # No data to plot, sleep for a while
            time.sleep(1)



t1 = threading.Thread(target = main2)
t2 = threading.Thread(target = graphingCurrent)

t1.start()
t2.start()


t1.join()
t2.join()
