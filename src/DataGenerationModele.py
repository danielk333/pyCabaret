import sys
import os
import config.muttconfig
import numpy as np
import atmUS76 as atmosphere
import rebuilding_setup as setup
import config.input

from modele import modele
from config.input import mach_list, altitude_list, rad_list

"""

This script computes the heat flux for various combinations of altitude, Mach number, and radiation level,
Using the `modele` function. The computed data is stored in different CSV filesfor further analysis.

Output stored in 'data_ML:
- One master CSV file ('ML.csv') containing rad, altitude, Mach, heatflux, ionization data.

"""

#data generation

#stored each row as: rad, altitude, mach, heatflux, massblowtot, rhoigas
f_ML = open("/Users/jeannelonglune/Desktop/memoire/pyCabaret/src/data_ML/ML_8000.csv","w")

for i,rad in enumerate(rad_list):
    for j,altitude in enumerate(altitude_list):
        for k,mach in enumerate(mach_list):
            output = modele(altitude, mach, rad)
            f_ML.write(f"{rad}, {altitude}, {mach}, {output[0]}, {output[1]},")
            f_ML.write("\n")
f_ML.close()

