#%%
#data generation

import numpy as np
from modeleGSI_copy import modele_gsi
from config.input import mach_list, altitude_list, rad_list, dx, Twall

#stored each row as: rad, altitude, mach, heatflux, massblowtot, rhoigas
f_ML = open("/Users/jeannelonglune/Desktop/memoire/pyCabaret/src/data_ML/MLgsi_8000.csv","w")

for i,rad in enumerate(rad_list):
    for j,altitude in enumerate(altitude_list):
        for k,mach in enumerate(mach_list):
            output = modele_gsi(mach, altitude, rad, Twall)
            f_ML.write(f"{rad}, {altitude}, {mach}, {output[0]}, {output[1]}, {output[2]}, ") #, {output[3]}, {output[4]}, {output[5]}
            #for x in range(len(output[2])):
                #f_ML.write(f"{output[2][x]}, ")
            #for x in range( len(output[6])):
                #f_ML.write(f"{output[6][x]}, ")
            f_ML.write("\n")
f_ML.close()
