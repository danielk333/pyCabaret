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


# Species 
Electron_density = np.zeros(len(list))
#N_plus_density = np.zeros(len(list))
#O_plus_density = np.zeros(len(list))
#NO_plus_density = np.zeros(len(list))
#N2_plus_density = np.zeros(len(list))
#O2_plus_density = np.zeros(len(list))

# File reading 
f_read = open("./src/data_ML/MLgsi.csv","r") 

j = 0

for i, line in enumerate(f_read):
    line = line.split(", ")
    # mainvariable == 'Altitude'
    if mainvariable == 'Altitude' and np.abs(float(line[0]) - fixed_rad) < 1e-10 and np.abs(float(line[2]) - fixed_mach) < 1e-10: 
        Electron_density[j] = float(line[8])
        #N_plus_density[j] = float(line[6])
        #O_plus_density[j] = float(line[7])
        #NO_plus_density[j] = float(line[8])
        #N2_plus_density[j] = float(line[9])
        #O2_plus_density[j] = float(line[10])
        j+=1
    # mainvariable == 'Mach'
    elif mainvariable == 'Mach' and np.abs(float(line[0]) - fixed_rad) < 1e-10 and np.abs(float(line[1]) - fixed_altitude) < 1e-10: 
        Electron_density[j] = float(line[8])
        #N_plus_density[j] = float(line[6])
        #O_plus_density[j] = float(line[7])
        #NO_plus_density[j] = float(line[8])
        #N2_plus_density[j] = float(line[9])
        #O2_plus_density[j] = float(line[10])
        j+=1
    # mainvariable == 'Rad'
    elif mainvariable == 'Rad' and np.abs(float(line[1]) - fixed_altitude) < 1e-10 and np.abs(float(line[2]) - fixed_mach) < 1e-10: 
        Electron_density[j] = float(line[8])
        #N_plus_density[j] = float(line[6])
        #O_plus_density[j] = float(line[7])
        #NO_plus_density[j] = float(line[8])
        #N2_plus_density[j] = float(line[9])
        #O2_plus_density[j] = float(line[10])
        j+=1

# Plot

fig, ax = plt.subplots(1,1)
ax.semilogy(list, Electron_density, "r", label = 'e- density')
#ax.plot(list, N_plus_density, "b", label = 'N+ density')
#ax.plot(list, O_plus_density, "g", label = 'O+ density')
#ax.plot(list, NO_plus_density, "k", label = 'NO+ density')
#ax.plot(list, N2_plus_density, "b--", label = 'N2+ density')
#ax.plot(list, O2_plus_density, "g--", label = 'O2+ density')

ax.set_title("number density VS " + x_label +"\n (" + fixed_values +")")
ax.set_xlabel(x_label)
ax.set_ylabel("number density [m^-3]") #check units
ax.legend(loc= 'lower right')
plt.show()
