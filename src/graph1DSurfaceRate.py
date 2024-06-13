import numpy as np
from modeleGSI import modele_gis
import matplotlib.pyplot as plt 
from config.input import altitude_list, mach_list, rad_list

# Main conditions
mainvariable = 'Rad' #change altitude, mach or radius

fixed_mach = mach_list[15] # change ind to observe for a different mach
fixed_altitude = altitude_list[30] # change ind to observe for a different altitude
fixed_rad = rad_list[15] # change ind to observe for a different radius

if mainvariable == 'Altitude':
    list = altitude_list
    x_label = 'Altitude [km]'
    fixed_values = 'mach = '+str(fixed_mach)+ ', radius = '+ str(fixed_rad)+ ' m'
elif mainvariable == 'Mach' : 
    list = mach_list
    x_label = 'Mach'
    fixed_values = 'altitude = '+str(fixed_altitude)+ ' km, radius = '+ str(fixed_rad)+ ' m'
elif mainvariable == 'Rad': 
    list = rad_list
    x_label = 'Rad[m]'
    fixed_values = 'mach = '+str(fixed_mach)+ ', altitude = '+ str(fixed_altitude)+ ' km'


# Species CHECK
N_surface_rate = np.zeros(len(list))
O_surface_rate = np.zeros(len(list))
N2_surface_rate = np.zeros(len(list))

O2_surface_rate = np.zeros(len(list))
CO_surface_rate = np.zeros(len(list))
#C_surface_rate = np.zeros(len(list))
C3_surface_rate = np.zeros(len(list))

# File reading 
f_read = open("/Users/jeannelonglune/Desktop/memoire/pyCabaret/src/data_ML/MLgsi.csv","r") 

j = 0

for i, line in enumerate(f_read):
    line = line.split(", ")
    # mainvariable == 'Altitude'
    if mainvariable == 'Altitude' and np.abs(float(line[0]) - fixed_rad) < 1e-10 and np.abs(float(line[2]) - fixed_mach) < 1e-10: 
        N_surface_rate[j] = float(line[9])
        O_surface_rate[j] = float(line[10])
        N2_surface_rate[j] = float(line[10])

        O2_surface_rate[j] = float(line[13])
        CO_surface_rate[j] = float(line[14])
        #C_surface_rate[j] = float(line[33])
        C3_surface_rate[j] = float(line[17])
        j+=1
    # mainvariable == 'Mach'
    elif mainvariable == 'Mach' and np.abs(float(line[0]) - fixed_rad) < 1e-10 and np.abs(float(line[1]) - fixed_altitude) < 1e-10: 
        #O_surface_rate[j] = float(line[27])
        O2_surface_rate[j] = float(line[13])
        CO_surface_rate[j] = float(line[14])
        #C_surface_rate[j] = float(line[33])
        C3_surface_rate[j] = float(line[17])
        j+=1
    # mainvariable == 'Rad'
    elif mainvariable == 'Rad' and np.abs(float(line[1]) - fixed_altitude) < 1e-10 and np.abs(float(line[2]) - fixed_mach) < 1e-10: 
        #O_surface_rate[j] = float(line[27])
        O2_surface_rate[j] = float(line[13])
        CO_surface_rate[j] = float(line[14])
        #C_surface_rate[j] = float(line[33])
        C3_surface_rate[j] = float(line[17])
        j+=1

# Plot

O2_surface_rate = abs(O2_surface_rate)
CO_surface_rate = abs(CO_surface_rate)
#C_surface_rate = np.zeros(len(list))
C3_surface_rate = abs(C3_surface_rate)

fig, ax = plt.subplots(1,1)
#ax.plot(list, O_surface_rate, "r", label = 'O surface rate')
ax.semilogy(list, O2_surface_rate, "b", label = 'O2 surface rate')
ax.semilogy(list, CO_surface_rate, "g", label = 'CO surface rate')
#ax.plot(list, C_surface_rate, "k", label = 'C surface rate')
ax.semilogy(list, C3_surface_rate, "m", label = 'C3 surface rate')

ax.set_title("Surface rate VS " + x_label +"\n (" + fixed_values +")")
ax.set_xlabel(x_label)
ax.set_ylabel("Surface rate") #check units
ax.legend(loc= 'lower right')
plt.show()
