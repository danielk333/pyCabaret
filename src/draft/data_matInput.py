import numpy as np
import matplotlib.pyplot as plt 


"""
A NETTOYER ABSOLUMENT : RELIER à MAT_INPUT POUR GENERER LES IMAGES DE CHAQUE R!!!! et avoir les bonnes dims etc


import mat_input 

altitude_list = np.linspace(50,70,100)
mach_list = np.linspace(14,20,100)
rad_list = np.linspace(0.1,1,10)

"""


rad_nbr = 9
alt_min, alt_max, alt_res = 50, 70, 100 
mach_min, mach_max, mach_res = 3,6,100
altitude_list = np.linspace(alt_min, alt_max, alt_res)
mach_list = np.linspace(mach_min, mach_max, mach_res)

#res_tab full de zéro aux bonnes dimensions
res_tab = np.zeros((alt_res, mach_res))

#fichier rad, colonne c'est mach et ligne c'est altitude.

f_read = open("/Users/jeannelonglune/Desktop/memoire/pyCabaret-master/src/data_mat_input/rad_"+str(rad_nbr)+".csv","r") 
for i, line in enumerate(f_read):
    line = line.split(", ")
    for j,nbr in enumerate(line):
        nbr = nbr.strip()  # Supprimez les espaces blancs autour de la chaîne
        if nbr:  # Vérifiez si la chaîne n'est pas vide
            res_tab[i, j] = float(nbr)
f_read.close()

#AUTOMATISER POUR IMPRIMER LES GRAPHS DE CHACUN DES FICHER
fig,ax =plt.subplots()
ims=ax.imshow(res_tab,origin="lower", extent=[mach_min, mach_max, alt_min, alt_max]) #plot le tableau 
cbar = fig.colorbar(ims)
ax.set_aspect("auto")
ax.set_xlabel("Mach number")
ax.set_ylabel("Altitude [km]")
ax.set_title("Value Heat flux [W/m^2] for an effective radius of 0.1 m") #ici changer pour que ça se mette automatiquement.
plt.savefig("/Users/jeannelonglune/Desktop/memoire/pyCabaret-master/src/plot_res/01plot.pdf", bbox_inches ="tight")
plt.show() #affichage