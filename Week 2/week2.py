import numpy as np
import matplotlib.pyplot as plt

#------------------------
#Loading and fitting data
#------------------------
x, y = np.loadtxt('file.dat', unpack=True) # Read the two-column text file.
R_C = 33000 # 33k resistor (use a measured resistance value if you wish)
newY = [i / R_C for i in y]
newY = np.log(newY) # Obtain ln(I_C) from V_C
#Least-squares fit to straight line: y = p[0]*x + p[1]
#p is array of fit coefficients
#cov is covariance matrix used to obtain error estimates
p, cov = np.polyfit(x, newY, 1, cov = True) # first-order polynomial fit
#--------------
#Console Output
#--------------
print("Gradient = ", p[0], " +/- ", np.sqrt(cov[0,0]))
print("Intercept = ", p[1], " +/- ", np.sqrt(cov[1,1]))
#--------
#Plotting
#--------
plt.title("Determining Boltzmann's Constant")
plt.xlabel("$V_{BE}$ (V)") 
plt.ylabel("$V_c$ (V)")
plt.plot(x, y, 'x') # plot data a red dots
plt.show() # explore the lower icons, click the red cross to close window

plt.title("Determining Boltzmann's Constant")
plt.xlabel("$V_{BE}$ (V)") 
plt.ylabel("$I_c$ (A)")
plt.plot(x, newY, 'x') # plot data a red dots
yfit = p[0] * x + p[1]
plt.plot(x,yfit, 'b-') # plot the fit as a blue line
plt.show() # explore the lower icons, click the red cross to close window

plt.title("Residuals") # give a suitable title
plt.xlabel("$V_{BE}$ (V)") # insert a suitable axis label
plt.ylabel("Residuals") # insert a suitable axis label
yfit = p[0] * x + p[1]
resid = newY - yfit
plt.plot(x,resid,'x')
plt.show()
