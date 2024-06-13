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
        vect_massblow_alt[j_altVar] = float(line[4])
        j_altVar+=1
    #machVar
    if np.abs(float(line[0]) - value_rad_machVar) < 1e-10 and np.abs(float(line[1]) - value_alt_machVar) < 1e-10: 
        vect_heatflux_mach[j_machVar] = float(line[3])
        vect_massblow_mach[j_machVar] = float(line[4])
        j_machVar+=1
    #radVar
    if np.abs(float(line[1]) - value_alt_radVar) < 1e-10 and np.abs(float(line[2]) - value_mach_radVar) < 1e-10: 
        vect_heatflux_rad[j_radVar] = float(line[3])
        vect_massblow_rad[j_radVar] = float(line[4])
        j_radVar+=1


fig, ax = plt.subplots(1,3)
line_0_heatflux = ax[0].plot(rad_list, vect_heatflux_rad, "g")
ax[0].set_title("Heatflux and massblow VS radius \n (mach = "+str(value_mach_radVar) + ",\n  altitude = " + str(value_alt_radVar)+ "km)")
ax_0_twin = ax[0].twinx()
line_0_massblow= ax_0_twin.plot(rad_list, abs(vect_massblow_rad), "g--")
ax[0].set_xlabel("Radius [m]")
ax[0].set_ylabel("Heatflux [W/m^2]")
ax_0_twin.set_ylabel("Massblow [kg/s]") 
lines_0 = line_0_heatflux + line_0_massblow
ax[0].legend(lines_0, ["Heatflux", "Massblow"])


line_1_heatflux =ax[1].plot(mach_list, vect_heatflux_mach, "r")
ax[1].set_title("Heatflux and massblow VS mach \n (rad = "+str(value_rad_machVar) + "m,\n  altitude = " + str(value_alt_machVar)+"km )")
ax_1_twin =ax[1].twinx()
line_1_massblow = ax_1_twin.plot(mach_list, abs(vect_massblow_mach), "r--")
ax[1].set_xlabel("Mach")
ax[1].set_ylabel("Heatflux [W/m^2]")
ax_1_twin.set_ylabel("Massblow [kg/s]")  
lines_1 = line_1_heatflux + line_1_massblow
ax[1].legend(lines_1, ["Heatflux", "Massblow"])


line_2_heatflux = ax[2].plot(altitude_list, vect_heatflux_alt, "b")
ax[2].set_title("Heatflux and massblow VS altitude \n (mach = "+str(value_mach_altVar) + ",\n  rad = " + str(value_rad_altVar)+"m)")
ax_2_twin =ax[2].twinx()
line_2_massblow = ax_2_twin.plot(altitude_list, abs(vect_massblow_alt), "b--")
ax[2].set_xlabel("Altitude [km]")
ax[2].set_ylabel("Heatflux [W/m^2]")
ax_2_twin.set_ylabel("Massblow [kg/s]")  
lines_2 = line_2_heatflux + line_2_massblow
ax[2].legend(lines_2, ["Heatflux", "Massblow"])


fig.tight_layout()

plt.show()
