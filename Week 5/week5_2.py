import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit 

x, y = np.loadtxt("polyfit2.dat", usecols=[0,1], unpack=True)

a, cov = np.polyfit(x, y, 1, cov = True)

print("Voltage = ", a[0]," +/- ",np.sqrt(cov[0,0]))
print("Current = ", a[1]," +/- ",np.sqrt(cov[1,1]))

plt.title("Threshold Voltage Against Current")
plt.xlabel("$V_{th}$ (V)")
plt.ylabel("Current (A)")
yfit = a[0]*x + a[1]
plt.plot(x,y,'ro',x,yfit)
plt.show()

xIntercept = (0 - np.sqrt(cov[1,1])) / np.sqrt(cov[0,0])
print("X Intercept: " + str(xIntercept))
