#%%
## Importing local mutationpp python module ##
import sys
import os
import math
import numpy as np
import config.muttconfig
import rebuilding_setup as setup
import reading_input as input_data

from shock import shock
from pathlib import Path
from atmUS76 import Atmosphere
from config.input import R, dx, Twall


# Define gas
from shock import shock
import _mutationpp as mpp
print(mpp)

def modele_gis(Mfreestream, alt, reff, dx, Twall,): 

    opts = ("N.xml")
    mix = mpp.Mixture(opts)
                                                            #I REMOVED SUBLIMATION : add again : check which file they take as

    # Setting up
    set_state_with_rhoi_T = 1 #You are setting state with partial densitites (rhoi) and temperature (2 thermodynamic props needed)
    #pos_T_trans = 0
    ns = mix.nSpecies()
    print('ns', ns)
    #nT = mix.nEnergyEqns()  #1 if thermal equilibrium, 2 if you are using a two-temperature model

    #pre-shock state
    pfreestream = Atmosphere(alt)[0]
    Tfreestream = Atmosphere(alt)[1]

    preshock_state = [Tfreestream,pfreestream,Mfreestream]
    print(preshock_state)
    #[219.58076564683952, 5.219719752495632, 28.56]
    options1 = {"ratio": 0.2,  #limit bf infinite loop is 0.33 #initial guess rho1/rho2
            "robust": "Yes"}

    print("\n--- SHOCK ---")
    #solving post-shock state
    Tgas,pgas,vgas = shock(preshock_state,mix,options1)
    mix.equilibrate(Tgas, pgas)
    rhoigas =  mix.densities()  #post-shock partial densisities
    print("\n post-shock partial densities")
    for i in range(mix.nSpecies()):
        print(mix.speciesName(i) + ": " +str(rhoigas[i]))
    Xgas = mix.X()              #post-shock molar fraction
    print("\n post-shock molar fraction")
    for i in range(mix.nSpecies()):
        print(mix.speciesName(i) + ":" + str(Xgas[i]))
    print(Tgas, pgas, vgas)

    Xgasreduced = Xgas[[7, 10, 11, 13, 14]]
    print('xgasreduced', Xgasreduced)
    rhoigasreduced = rhoigas[[7, 10, 11, 13, 14]]
    print('rhoigasreduced', rhoigasreduced)

    # see Newton method, tentative value
    mix.setSurfaceState(rhoigas, Twall, set_state_with_rhoi_T)    #tentative rhoi and Tw
    mix.setDiffusionModel(Xgas, dx)                               #to compute diffusive velocity ~ (Xgas - Xwall)/dx
    mix.solveSurfaceBalance()                                     #solving surface state
    [rhoiwall, Twall] = mix.getSurfaceState(set_state_with_rhoi_T)   #getting surface state (updated rhoiwall, Twall unchanged as not solving energy balance)
    print('\n rhoiwall', rhoiwall)
    # Get surface production rates
    wdot = np.zeros(ns)
    wdot = mix.surfaceReactionRates()
    print("\nSurface reaction rates:")
    for i in range(mix.nSpecies()):
        print(mix.speciesName(i) + ": " + str(wdot[i]))

    # Blowing flux (should be zero for catalysis)
    mblow = mix.getMassBlowingRate()
    #mblowtot = mblow * surface / speed strong hypothesis : the stagnation temperature is the temperature of the debris ! 
    #maybe it would make sens to multiply it with a sine function or something (as in the paper)
    mblowtot = mblow * 4 * math.pi *reff*reff / (M_1 * 340) # 1 mach = 340 m/s
    print("\nMass blow [kg/(m^2-s)]: " + str(mblow))
    print("\nMass blow tot [kg/(m)]: " + str(mblowtot))


    #Compute heat flux
    #1) conductive part qw: lamda(wall) * (Tgas - Twall) / dx 
    mix.setState(rhoiwall, Twall, set_state_with_rhoi_T)
    lambda_ = mix.frozenThermalConductivity()   
                                          #did we say we ut it as an input? 
    # frozenThermalConductivity : Returns the mixture thermal conductivity for a frozen mixture."" To be used only at thermal equilibrium."
    print('\n tgas', Tgas)
    qcond = lambda_ * (Tgas - Twall) / dx #gradient

    #2) diffusive heat flux: sum_ns (rhoi hi Vi)
    hi = mix.speciesHOverRT() *R *Twall #ns
    E_field = 0.0
    Xwall = mix.X()  #wall molar fraction
    print('xwall', Xwall)
    print('xgas', Xgas)
    v_b = (Xgas - Xwall) / dx  # molar fraction gradient
    #compute diffusive velocities
    #v_Vd_sm = np.zeros(ns)
    v_Vd_sm, E_field = mix.stefanMaxwell(v_b)
        #"Computes the species diffusion velocities and ambipolar electricfield"
        #  " using the Ramshaw approximation of the generalized Stefan-Maxwell equations and the supplied modified driving forces."
    print('\n vvdsm', v_Vd_sm)
    qdiff = 0
    qdiff = np.sum(v_Vd_sm[[7, 10, 11, 13, 14]] * rhoiwall[[7, 10, 11, 13, 14]] * hi[[7, 10, 11, 13, 14]])
    #massloss = np.sum(v_Vd_sm * rhoiwall)
    #print('\n massloss', massloss)

    #3) compute advective flux 
    #qadv =  rho* ug *h where ug = mdot /rho
            #yi * hi *mblow diffusi
    qadv = np.sum(hi[[7, 10, 11, 13, 14]]) * mblow 

    #4) re-radiation heat loss
    sigma = 5.67e-8   #σ is the Stephan-Boltzmann constant (5.67 × 10− 8 W/m2-K4)
    epsilon = 0.98                                           #body emissivity of carbon
    qrad = epsilon * sigma * Twall**4
    print('qrad', qrad)

    print('qdiff', qdiff)
    print('qcond', qcond)
    print('qadv', qadv)

    print('q \n', qcond+qdiff-qadv) #+qadv
    print('mblowtot\n', mblowtot)
    for i in range(mix.nSpecies()):
        print(mix.speciesName(i) + ":" + str(rhoigas[i]))

    qwtot = qcond+qdiff-qadv #-qrad


    return qwtot, mblowtot, rhoigas

print("\n--- FREE STREAM CONDITIONS ---")
M_1 = 20
reff = 0.5 #HOW TO LINK IT TO THE linked to the dx of the boundary layer.
alt = 60 
#surface input
modele_gis(M_1, alt, reff, dx, Twall)

print('with cabaret : Qw = 1238689.8407288808 W/m2 with the same input param M=20, reff = 0.5, alt = 60')
# You might need to replace some functions or classes with their corresponding Python equivalents.

#%%
#data generation





import matplotlib.pyplot as plt 
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

#AUTOMATISER POUR IMPRIMER LES GRAPHS DE CHACUN DES FICHER
fig,ax =plt.subplots()
ims=ax.imshow(res_tab,origin="lower", extent=[18, 24, 30, 80]) #plot le tableau 
cbar = fig.colorbar(ims)
ax.set_aspect("auto")
ax.set_xlabel("Mach number")
ax.set_ylabel("Altitude [km]")
ax.set_title("Value Heat flux [W/m^2] for an effective radius of 0.1 m") #ici changer pour que ça se mette automatiquement.
plt.savefig("/Users/jeannelonglune/Desktop/memoire/pyCabaret/src/plot_res/01plotgsi.pdf", bbox_inches ="tight")
plt.show() #affichage 