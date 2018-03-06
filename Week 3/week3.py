import numpy as np
import matplotlib.pyplot as plt
from physlab import tenmaread
from scipy.optimize import curve_fit 

resistanceR = 10000
B = 3977
temperatureR = 298.2
internalResistance = 1E6

filename = "week3_3.sav"
x1, y1, x2, y2 = tenmaread(filename)

def getTemperature(resistanceR, internalResistance, y1, y2, B):
    Rlower = (resistanceR * internalResistance) / (resistanceR + internalResistance)
    resistanceThermister = ((y1 - y2) / y2) * Rlower
    temperature = 1 / 298.2 + np.log(resistanceThermister / resistanceR) / B
    temperature = 1 / temperature
    return temperature

def getcoolingTemperature(temperatureR, temperatureF, ):
    return false

time = x2
v = y2

def exponentialFunction(x, T_A, T_F, tau_c):
 return T_A + (T_F - T_A) * np.exp((-x) / tau_c)

temperatureF = getTemperature(resistanceR, internalResistance, y1, y2, B)

popt, pcov = curve_fit(exponentialFunction, time, temperatureF)
yfit = exponentialFunction(time, *popt)
plt.xlabel("Time (s)")
plt.ylabel("Temperature (K)")
plt.plot(time, temperatureF, 'ro', time, yfit, 'b-')
plt.show()
    
plt.xlabel("Time (s)")
plt.ylabel("Voltage (V)")
plt.plot(x1,y1,x2,y2)
plt.show()

plt.xlabel("Time (s)")
plt.ylabel("Temperature (K)")
plt.plot(x1, temperatureF)
plt.show()

print()
print("Ta = ", popt[0], " +/- ", np.sqrt(pcov[0, 0]))
print("Tf = ", popt[1], " +/- ", np.sqrt(pcov[1, 1]))
print("tau_c = ", popt[2], " +/- ", np.sqrt(pcov[2, 2]))
