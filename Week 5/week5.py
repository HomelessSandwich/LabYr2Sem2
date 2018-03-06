import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit 

def isInBoundry(h, errorH):
    if ((h - errorH) < 6.626E-34 and 6.626E-34 < (h + errorH)):
        return True
    else:
        return False

c = 2.998E8
q = 1.602E-19

x, y = np.loadtxt("polyfit.dat", usecols=[0,1], unpack=True)

x = c / x

a, cov = np.polyfit(x, y, 1, cov = True)

print("Frequency = ", a[0]," +/- ",np.sqrt(cov[0,0]))
print("Voltage = ", a[1]," +/- ",np.sqrt(cov[1,1]))

plt.title("$V_{th}$ Against LED Frequency")
plt.xlabel("Frequency (Hz)")
plt.ylabel("$V_{th}$ (V)")
yfit = a[0]*x + a[1]
plt.plot(x,y,'ro',x,yfit)
plt.show()

h = q * a[0]
differenceH = 100 - (6.626E-34 / h) * 100

errorH = h * (np.sqrt(cov[0, 0]) / a[0])

print("\nCalculated Plank's Constant: " + str(h))
print("Error of measured Plank's Constant: " + str(errorH))
print("Error out of accurate value: " + str(differenceH))
print("Error of measured value within accurate value of Plank's Constant: " + str(isInBoundry(h, errorH)))

