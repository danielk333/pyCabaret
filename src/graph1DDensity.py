#%%
## Importing local mutationpp python module ##
import sys
import os
import math
import numpy as np
import config.muttconfig
import rebuilding_setup as setup
import reading_input as input_data
import matplotlib.pyplot as plt 

from shock import shock
from pathlib import Path
from atmUS76 import Atmosphere
from config.input import R


# Define gas
from shock import shock
import _mutationpp as mpp
print('mpp\n', mpp)

altitude_list = np.linspace(0,80,1000)
Pressure = []
Temperature = []
density = []
opts = ("C.xml")
mix = mpp.Mixture(opts)
densi = mix.setState(50, 300, 1)
print('densi', densi)



for alt in altitude_list:
    Pressure_i , Temperature_i = Atmosphere(alt)
    mix.setState(Pressure_i, Temperature_i, 1)
    density_i = mix.density()
    Pressure.append(Pressure_i)
    Temperature.append(Temperature_i)
    density.append(density_i)

fig, ax = plt.subplots(1,1)
ax.plot(density, altitude_list, 'b')
#ax2 = ax.twiny()
#ax2.plot(density, altitude_list, 'r')
plt.show()