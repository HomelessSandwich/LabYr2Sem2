import numpy as np
import matplotlib.pyplot as plt
from physlab import tenmaread
from scipy.optimize import curve_fit 

#Constant Variables
fileName = "10M.sav"
x1, y1, x2, y2 = tenmaread(fileName)
p0 = [0.001, 0.001, np.max(y2), 0.001, 0.002]
t = x2
v = y2

def function(x,tau_c, tau_d, v_s, t_c, t_d):
 out = np.zeros(len(x))
 v_c = v_s*(1-np.exp(-(t_d-t_c)/tau_c))
 for i in range(len(x)):
     if (x[i] <= t_c):
         out[i] = 0.
     elif (x[i] > t_c and x[i] < t_d):
         out[i] = v_s * (1 - np.exp(-(x[i] - t_c) / tau_c))
     else:
         out[i]= v_c * np.exp(-(x[i] - t_d) / tau_d)
 return out

popt, pcov = curve_fit(function, t, v, p0 = p0)
print("tau_C = ", popt[0], " +/- ", np.sqrt(pcov[0, 0]))
print("tau_D = ", popt[1], " +/- ", np.sqrt(pcov[1, 1]))
print("Vs = ", popt[2], " +/- ", np.sqrt(pcov[2, 2]))
print("t_C = ", popt[3], " +/- ", np.sqrt(pcov[3, 3]))
print("t_D = ", popt[4], " +/- ", np.sqrt(pcov[4, 4]))
yfit = function(t, *popt)

#Plotting Data
plt.xlabel("Time (s)")
plt.ylabel("Voltage (V)")
plt.plot(t, v, 'ro', t, yfit, 'b-')
plt.title("Voltage Against Time of a Photocurrent Mode in Series with a 10MΩ Resistor")
plt.show()

