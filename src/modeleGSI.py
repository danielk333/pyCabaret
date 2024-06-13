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
from config.input import R


# Define gas
from shock import shock
import _mutationpp as mpp
print(mpp)

def modele_gis(Mfreestream, alt, reff, dx, Twall): 

    opts = ("C.xml")
    mix = mpp.Mixture(opts)

    # Setting up
    set_state_with_rhoi_T = 1 
    ns = mix.nSpecies()
 
    #pre-shock state
    Pfreestream = Atmosphere(alt)[0]
    Tfreestream = Atmosphere(alt)[1]
    

    preshock_state = [Tfreestream,Pfreestream,Mfreestream]
    options1 = {"ratio": 0.2,  
            "robust": "Yes"}

    #solving post-shock state
    print("\n--- SHOCK ---")
    Tgas,Pgas,Vgas = shock(preshock_state,mix,options1)
    mix.equilibrate(Tgas, Pgas)
    rhoigas =  mix.densities()                                  #post-shock partial densisities
    mix.setState(rhoigas, Tgas, set_state_with_rhoi_T)          #tentative rhoi and Tw
    Xgas = mix.X()                                              #post-shock molar fraction
    Ygas = mix.Y()                                              #post-shock mass fraction

    # see Newton method, tentative value
    mix.setSurfaceState(rhoigas, Twall, set_state_with_rhoi_T)       #tentative rhoi and Tw
    mix.setDiffusionModel(Xgas, dx)                                  #to compute diffusive velocity ~ (Xgas - Xwall)/dx
    mix.solveSurfaceBalance()                                        #solving surface state
    [rhoiwall, Twall] = mix.getSurfaceState(set_state_with_rhoi_T)   #getting surface state (updated rhoiwall, Twall unchanged as not solving energy balance)
    
    # Get surface production rates and massblow
    wdot = np.zeros(ns)
    wdot = mix.surfaceReactionRates()
    mblow = mix.getMassBlowingRate()
    mblowtot = mblow * 4 * math.pi *reff*reff / (M_1 * 340) # 1 mach = 340 m/s


    #Compute heat flux
    #1) conductive part qw: lamda(wall) * (Tgas - Twall) / dx 
    mix.setState(rhoiwall, Twall, set_state_with_rhoi_T)
    lambda_ = mix.frozenThermalConductivity()   
    qcond = lambda_ * (Tgas - Twall) / dx 

    #2) diffusive heat flux: sum_ns (rhoi hi Vi)
    hi = mix.speciesHOverRT() *R *Twall                 #ns
    E_field = 0.0
    Xwall = mix.X()                                     #wall molar fraction
    print('xwall', Xwall)
    print('xgas', Xgas)
    v_b = (Xgas - Xwall) / dx                           # molar fraction gradient
    [v_Vd_sm, E_field] = mix.stefanMaxwell(v_b)
    qdiff = np.sum(v_Vd_sm * rhoiwall * hi)

    #3) compute advective flux : rho* ug *h where ug = mdot /rho
    Ywall = mix.Y()
    toth = hi*Ywall
    qadv = np.sum(toth) * mblow

    #4) re-radiation heat loss
    sigma = 5.67e-8   #σ is the Stephan-Boltzmann constant (5.67 × 10− 8 W/m2-K4)
    epsilon = 0.98                                           #body emissivity of carbon
    qrad = epsilon * sigma * Twall**4 

    print('qdiff', qdiff)
    print('qcond', qcond)
    print('qadv', qadv)
    print('q', qcond+qdiff+qadv) 

    qwtot = qcond+qdiff+qadv 

    return qwtot, mblowtot, rhoigas, wdot

print("\n--- FREE STREAM CONDITIONS ---")
M_1 = 20
reff = 0.5 #HOW TO LINK IT TO  dx of the boundary layer.
alt = 80 
#surface input
dx = 4e-4  # to be changed to the right value
Twall = 3823  #melting temperature of carbon
results = modele_gis(M_1, alt, reff, dx, Twall)
print('results model, qwtot, mblowtot, rhoigas, wdot', results)
print(results)

print('with cabaret : Qw = 1238689.8407288808 W/m2 with the same input param M=20, reff = 0.5, alt = 60')