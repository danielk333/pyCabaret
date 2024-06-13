#%%
#data generation
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import matplotlib.pyplot as plt 
from config.input import altitude_list, mach_list, rad_list

##Plot 2D 
#Plotted value
ind = 4 #value = 3 if plot of heatflux and 4 if plot massblow
if ind == 3 : 
    y_label = "Heatflux [W/m^2]"
else : 
    y_label = "Massblow [kg/s]"
#fixed = altitude
fixed_alt = altitude_list[0] #valeur du param fixe
#fixed = mach
fixed_mach = mach_list[0]
#fixed = rad
fixed_rad = rad_list[0]

#definition matrices
mat_fixed_rad = np.zeros([len(altitude_list), len(mach_list)])
mat_fixed_alt = np.zeros([len(rad_list), len(mach_list)])
mat_fixed_mach = np.zeros([len(rad_list), len(altitude_list)])

f_read = open("/Users/jeannelonglune/Desktop/memoire/pyCabaret/src/data_ML/MLgsi.csv","r") 

for i, line in enumerate(f_read):
    line = line.split(", ")
    #fixed rad
    if np.abs(float(line[0]) - fixed_rad) < 1e-10 : 
        i = np.argmin(np.abs(float(line[1]) - altitude_list))
        j = np.argmin(np.abs(float(line[2]) - mach_list))
        mat_fixed_rad[i,j] = float(line[ind])
    #fixed altitude
    if np.abs(float(line[1]) - fixed_alt) < 1e-10: 
        i = np.argmin(np.abs(float(line[0]) - rad_list))
        j = np.argmin(np.abs(float(line[2]) - mach_list))
        mat_fixed_alt[i,j] = float(line[ind])
    #fixed mach
    if np.abs(float(line[2]) - fixed_mach) < 1e-10 : 
        i = np.argmin(np.abs(float(line[0]) - rad_list))
        j = np.argmin(np.abs(float(line[1]) - altitude_list))
        mat_fixed_mach[i,j] = float(line[ind])

mat_fixed_rad = abs(mat_fixed_rad)
mat_fixed_alt = abs(mat_fixed_alt)
mat_fixed_mach = abs(mat_fixed_mach)

fig, ax = plt.subplots(1,3)

extent_0 = [mach_list[0], mach_list[-1], altitude_list[0], altitude_list[-1]]
shape_0 = (len(altitude_list), len(mach_list))
dx_0 = (extent_0[1] - extent_0[0]) / shape_0[1]
dy_0 = (extent_0[3] - extent_0[2]) / shape_0[0]
dx_dy_0 = dx_0/dy_0
colormesh_0 = ax[0].pcolormesh(mach_list, altitude_list, mat_fixed_rad)
ax[0].set_aspect(dx_dy_0)
ax[0].set_xlabel("mach")
ax[0].set_ylabel("altitude [km]")
ax[0].set_title(y_label+ " VS mach and altitude \n (rad = "+str(fixed_rad)+ " m)")
fig.colorbar(colormesh_0, ax=ax[0], fraction=0.046, pad=0.04) #3 param fraction, pad, aspect

extent_1 = [mach_list[0], mach_list[-1], rad_list[0], rad_list[-1]]
shape_1 = (len(rad_list), len(mach_list))
dx_1 = (extent_1[1] - extent_1[0]) / shape_1[1]
dy_1 = (extent_1[3] - extent_1[2]) / shape_1[0]
dx_dy_1 = dx_1/dy_1
colormesh_1 = ax[1].pcolormesh(mach_list, rad_list, mat_fixed_alt)
ax[1].set_aspect(dx_dy_1)
ax[1].set_xlabel("mach")
ax[1].set_ylabel("rad[m]")
ax[1].set_title(y_label+ " VS mach and rad \n (altidue = "+str(fixed_alt)+ " km)")
fig.colorbar(colormesh_1, ax= ax[1], fraction=0.046*len(rad_list)/len(altitude_list), pad=0.04)


extent_2 = [altitude_list[0], altitude_list[-1], rad_list[0], rad_list[-1]]
shape_2 = (len(rad_list), len(altitude_list))
dx_2 = (extent_2[1] - extent_2[0]) / shape_2[1] 
dy_2 = (extent_2[3] - extent_2[2]) / shape_2[0]
dx_dy_2 = dx_2/dy_2
colormesh_2 = ax[2].pcolormesh(altitude_list, rad_list, mat_fixed_mach)
ax[2].set_aspect(dx_dy_2)
ax[2].set_xlabel("altitude [km]")
ax[2].set_ylabel("rad [m]")
ax[2].set_title(y_label+ " VS rad and altitude \n (mach = "+str(fixed_mach)+ ")")
fig.colorbar(colormesh_2, ax= ax[2], fraction=0.046*len(rad_list)/len(altitude_list), pad=0.04)



plt.show()




"""
#res_tab full de zéro aux bonnes dimensions
res_tab = np.zeros((10, 10))

#fichier rad, colonne c'est mach et ligne c'est altitude.

f_read = open("/Users/jeannelonglune/Desktop/memoire/pyCabaret/src/data_ML/rad_gis"+str(1)+".csv","r") 
for i, line in enumerate(f_read):
    line = line.split(", ")
    for j,nbr in enumerate(line):
        nbr = nbr.strip()  # Supprimez les espaces blancs autour de la chaîne
        if nbr:  # Vérifiez si la chaîne n'est pas vide
            res_tab[i, j] = float(nbr)
f_read.close()

fig,ax =plt.subplots()
ims=ax.imshow(res_tab,origin="lower", extent=[18, 24, 30, 80]) #plot le tableau 
cbar = fig.colorbar(ims)
#print(res_tab.T)
ax.set_aspect("auto")
ax.set_xlabel("Mach number")
ax.set_ylabel("Altitude [km]")
ax.set_title("Value Heat flux [W/m^2] for an effective radius of 0.1 m") #ici changer pour que ça se mette automatiquement.
plt.savefig("/Users/jeannelonglune/Desktop/memoire/pyCabaret/src/plot_res/01plotgsi.pdf", bbox_inches ="tight")
plt.show() #affichage

##Plot 3D"""
