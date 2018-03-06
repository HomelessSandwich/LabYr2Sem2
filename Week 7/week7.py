import numpy as np
import matplotlib.pyplot as plt

#Constant Variables
x1, y1 = np.loadtxt('results1.txt', unpack=True)
x1, y2 = np.loadtxt('results2.txt', unpack=True)

y1 = y1 / 1000

plt.title("Frequency Response of Ultrasonic Transmitter and Receiver")
plt.xlabel("Frequency (Hz)") 
plt.ylabel("Voltage (V)")
plt.plot(x1, y1)
plt.plot(x1, y2) 
plt.show() 
