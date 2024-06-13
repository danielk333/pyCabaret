import numpy as np
import matplotlib.pyplot as plt 
from config.input import altitude_list, mach_list, rad_list

#variable = altitude
value_mach_altVar = mach_list[10] #valeur du param mach quand on fait varier l'altitude
value_rad_altVar = rad_list[10]
#variable = mach
value_rad_machVar = rad_list[10] 
value_alt_machVar = altitude_list[30]
#variable = rad
value_alt_radVar = altitude_list[30]
value_mach_radVar = mach_list[10]

#definition vectors
vect_heatflux_alt = np.zeros(len(altitude_list))
vect_heatflux_mach = np.zeros(len(mach_list))
vect_heatflux_rad = np.zeros(len(rad_list))

vect_heatflux_diff_alt = np.zeros(len(altitude_list))
vect_heatflux_cond_alt = np.zeros(len(altitude_list))
vect_heatflux_adv_alt = np.zeros(len(altitude_list))


vect_massblow_alt = np.zeros(len(altitude_list))
vect_massblow_mach = np.zeros(len(mach_list))
vect_massblow_rad = np.zeros(len(rad_list))

f_read = open("/Users/jeannelonglune/Desktop/memoire/pyCabaret/src/data_ML/MLgsi.csv","r") 

j_altVar=0
j_machVar=0
j_radVar=0

for i, line in enumerate(f_read):
    line = line.split(", ")
    #altVar
    if np.abs(float(line[0]) - value_rad_altVar) < 1e-10 and np.abs(float(line[2]) - value_mach_altVar) < 1e-10: 
        vect_heatflux_alt[j_altVar] = float(line[3])
        vect_heatflux_diff_alt[j_altVar] = float(line[5])
        vect_heatflux_cond_alt[j_altVar] = float(line[6])
        vect_heatflux_adv_alt[j_altVar] = float(line[7])
        j_altVar+=1


fig, ax = plt.subplots(1,1)

ax.set_title("Heatflux and massblow VS altitude \n (mach = "+str(value_mach_altVar) + ",\n  rad = " + str(value_rad_altVar)+"m)")
ax.plot(altitude_list, vect_heatflux_diff_alt, "b", label = 'Diffusive heatflux')
#ax.plot(altitude_list, vect_heatflux_cond_alt, "g", label = 'Conductive heatflux')
ax.plot(altitude_list, abs(vect_heatflux_adv_alt), "r", label = 'Advective heatflux')

ax.set_xlabel("Altitude [km]")
ax.set_ylabel("Heatflux [W/m^2]")

ax.legend()

fig.tight_layout()

plt.show()
