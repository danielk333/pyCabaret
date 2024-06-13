import numpy as np
import matplotlib.pyplot as plt 
from atmUS76 import Atmosphere

altitude_list = np.linspace(0,80,1000)
Pressure = []
Temperature = []


for alt in altitude_list:
    Pressure_i , Temperature_i = Atmosphere(alt)
    Pressure.append(Pressure_i)
    Temperature.append(Temperature_i)

fig, ax = plt.subplots(1,1)
ax.plot(Pressure, altitude_list, 'b')
ax2 = ax.twiny()
ax2.plot(Temperature, altitude_list, 'r')
plt.show()