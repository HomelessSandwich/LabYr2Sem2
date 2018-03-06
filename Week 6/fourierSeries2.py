import numpy as np
import matplotlib.pyplot as plt
from physlab import tenmaread

t, y, x2, y2 = tenmaread('save1.sav')
y = y-np.mean(y)
ft= np.abs(np.fft.rfft(y))*2./len(y)
sample_rate = 1/(t[1]-t[0])
freqs = np.linspace(0.,sample_rate/2,len(ft))

#freqs is an array of the frequencies (x values)
#ft is an array of the (y values)
maxValue = freqs[np.where(ft == max(ft))]
print('Maximum value of sample occurs at frequency: {0}Hz'.format(str(float(maxValue))))
#Gets max value of freq.

plt.subplot(2,1,1)
plt.plot(t,y,label="sine.dat")
plt.xlabel('time [s]')
plt.ylabel('signal ')
plt.subplot(2,1,2)
plt.plot(freqs,ft,label='Fourier Transform')
plt.xlabel('frequency [Hz]')
plt.ylabel('abs(FT)')
plt.savefig('sample{0}.png')
plt.show()

