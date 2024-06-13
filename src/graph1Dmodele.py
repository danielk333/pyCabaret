#%%
#data generation

import numpy as np
import matplotlib.pyplot as plt 
from config.input import altitude_list, mach_list, rad_list


##Plot 1D
#Plotted value
ind = 3 #value = 3 if plot of heatflux and 4 if plot massblow
if ind == 3 : 
    y_label = "Heatflux [W/m^2]"
else : 
    y_label = "Massblow [kg/m]"

#variable = altitude
value_mach_altVar = mach_list[0] #valeur du param mach quand on fait varier l'altitude
value_rad_altVar = rad_list[0]
#variable = mach
value_rad_machVar = rad_list[0] 
value_alt_machVar = altitude_list[0]
#variable = rad
value_alt_radVar = altitude_list[0]
value_mach_radVar = mach_list[0]
#definition vectors
vect_alt = np.zeros(len(altitude_list))
vect_mach = np.zeros(len(mach_list))
vect_rad = np.zeros(len(rad_list))


f_read = open("/Users/jeannelonglune/Desktop/memoire/pyCabaret/src/data_ML/ML.csv","r") 

j_altVar=0
j_machVar=0
j_radVar=0

for i, line in enumerate(f_read):
    line = line.split(", ")
    #altVar
    if np.abs(float(line[0]) - value_rad_altVar) < 1e-10 and np.abs(float(line[2]) - value_mach_altVar) < 1e-10: 
        vect_alt[j_altVar] = float(line[ind])
        j_altVar+=1
    #machVar
    if np.abs(float(line[0]) - value_rad_machVar) < 1e-10 and np.abs(float(line[1]) - value_alt_machVar) < 1e-10: 
        vect_mach[j_machVar] = float(line[ind])
        j_machVar+=1
    #radVar
    if np.abs(float(line[1]) - value_alt_radVar) < 1e-10 and np.abs(float(line[2]) - value_mach_radVar) < 1e-10: 
        vect_rad[j_radVar] = float(line[ind])
        j_radVar+=1


fig, ax = plt.subplots(1,3)
ax[0].plot(rad_list, vect_rad, "g")
ax[0].set_title(y_label+ " VS radius \n (mach = "+str(value_mach_radVar) + ",  altitude = " + str(value_alt_radVar)+ "km)")
ax[0].set_xlabel("Radius [m]")
ax[0].set_ylabel(y_label)


ax[1].plot(mach_list, vect_mach, "r")
ax[1].set_title(y_label +" VS mach \n (rad = "+str(value_rad_machVar) + "m,  altitude = " + str(value_alt_machVar)+"km )")
ax[1].set_xlabel("Mach")
ax[1].set_ylabel(y_label)


ax[2].plot(altitude_list, vect_alt, "b")
ax[2].set_title(y_label+" VS altitude \n (mach = "+str(value_mach_altVar) + ",  rad = " + str(value_rad_altVar)+"m)")
ax[2].set_xlabel("Altitude [km]")
ax[2].set_ylabel(y_label)


fig.tight_layout()

plt.show()
