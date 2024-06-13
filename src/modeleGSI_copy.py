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
from config.input import R, Na


# Define gas
from shock import shock
import _mutationpp as mpp
print('mpp\n', mpp)

def modele_gsi(Mfreestream, alt, reff, Twall): 

    dx = reff*18e-4 
    dx2 = dx

    opts = ("C.xml")
    mix = mpp.Mixture(opts)

    opts2 =("shockIon.xml")
    mix2= mpp.Mixture(opts2)

    # Setting up
    set_state_with_rhoi_T = 1
    ns = mix.nSpecies()

    #pre-shock state
    Pfreestream = Atmosphere(alt)[0]
    Tfreestream = Atmosphere(alt)[1]


    preshock_state = [Tfreestream,Pfreestream,Mfreestream]
    print('\n preshockstate, T, P, M', preshock_state)

    options1 = {"ratio": 0.2, 
            "robust": "Yes"}

    #post-shock state
    print("\n--- SHOCK ---")
    Tgas,Pgas,Vgas = shock(preshock_state,mix,options1)
    print('\n tgas, pgas, vgas', Tgas, Pgas, Vgas)

    mix2.equilibrate(Tgas, Pgas)
    rhoigasIon =  mix2.densities()                               #post-shock partial mass densisities   
    #print("\n post-shock partial densities Ion")
    #for i in range(mix2.nSpecies()):
        #print(mix2.speciesName(i) + ": " +str(rhoigasIon[i]))
    #XgasIon = mix2.X()                                            #post-shock molar fraction
    #print("\n post-shock molar fraction Ion ")
    #for i in range(mix2.nSpecies()):
        #print(mix2.speciesName(i) + ":" + str(XgasIon[i]))
    #YgasIon = mix2.Y()                                            #post-shock mass fraction
    #print("\n Ygas post-shock mass fraction Ion")
    #for i in range(mix2.nSpecies()):
        #print(mix2.speciesName(i) + ":" + str(YgasIon[i]))
    molarmass = mix2.speciesMw()
    print("\n MOLAR mass [kg/mol]")
    for i in range(mix2.nSpecies()):
        print(mix2.speciesName(i) + ":" + str(molarmass[i]))

    #compute number density : N = rho_mix Na / M mix  ([kg/m^3] [atoms/mole] / [kg/mole])
    Numberdensity = rhoigasIon * Na / molarmass
    print('Numberdensity [m^-3] \n', Numberdensity)


    mix.equilibrate(Tgas, Pgas)
    rhoigas =  mix.densities()                                #post-shock partial densisities
    mix.setState(rhoigas, Tgas, set_state_with_rhoi_T)        #tentative rhoi and Tgas
    print("\n post-shock partial densities")
    for i in range(mix.nSpecies()):
        print(mix.speciesName(i) + ": " +str(rhoigas[i]))
    Xgas = mix.X()                                            #post-shock molar fraction
    print("\n post-shock molar fraction")
    for i in range(mix.nSpecies()):
        print(mix.speciesName(i) + ":" + str(Xgas[i]))
    Ygas = mix.Y()                                            #post-shock mass fraction
    print("\n Ygas post-shock mass fraction")
    for i in range(mix.nSpecies()):
        print(mix.speciesName(i) + ":" + str(Ygas[i]))


    # see Newton method, tentative value
    mix.setSurfaceState(rhoigas, Twall, set_state_with_rhoi_T)       #tentative rhoi and Tw
    mix.setDiffusionModel(Xgas, dx2)                                  #to compute diffusive velocity ~ (Xgas - Xwall)/dx
    mix.solveSurfaceBalance()                                        #solving surface state
    rhoiwall, Twall = mix.getSurfaceState(set_state_with_rhoi_T)     #getting surface state (updated rhoiwall, Twall unchanged as not solving energy balance)
    print('\n rhoiwall', rhoiwall)
    # Get surface production rates
    wdot = np.zeros(ns)
    wdot = mix.surfaceReactionRates()
    print("\nSurface reaction rates:")
    for i in range(ns):
        print(mix.speciesName(i) + ": " + str(wdot[i]))

    # Blowing flux (should be zero for catalysis)
    mblow = mix.getMassBlowingRate()
    print("\nMass blow [kg/(m^2-s)]: " + str(mblow))
   # mblowtot = mblow * surface / speed strong hypothesis : the stagnation temperature is the temperature of the debris ! 
    mblowtot = mblow * 4 * math.pi *reff*reff  #maybe it would make sens to multiply it with a sine function or something (as in the paper)
    print("\nMass blow tot [kg/s)]: " + str(mblowtot))

    #Compute heat flux
    #1) conductive part qw: lamda(wall) * (Tgas - Twall) / dx 
    mix.setState(rhoiwall, Twall, set_state_with_rhoi_T)
    lambda_ = mix.frozenThermalConductivity()   
    qcond = lambda_ * (Tgas - Twall) / dx                       #gradient

    #2) diffusive heat flux: sum_ns (rhoi hi Vi)
    hi = mix.speciesHOverRT() *R *Twall  / mix.speciesMw()      #ns
    E_field = 0.0
    Xwall = mix.X()                                             #wall molar fraction
    print('xwall', Xwall)
    print('xgas', Xgas)
    v_b = (Xgas - Xwall) / dx2                                   # molar fraction gradient
    #compute diffusive velocities
    v_Vd_sm, E_field = mix.stefanMaxwell(v_b)
    print('\n vvdsm', v_Vd_sm)
    qdiff = - np.sum(v_Vd_sm * rhoiwall * hi)

    qdiff2 = np.sum(wdot*hi)

    Ywall = mix.Y()
    print("\nYwall:")
    for i in range(ns):
        print(mix.speciesName(i) + ": " + str(Ywall[i]))

    #3) compute advective flux 
    #qadv =  rho* ug *h where ug = mdot /rho
    Ywall = mix.Y()
    htot = hi*Ywall
    qadv = np.sum(htot) * mblow

    #4) re-radiation heat loss
    sigma = 5.67e-8                                          #σ is the Stephan-Boltzmann constant (5.67 × 10− 8 W/m2-K4)
    epsilon = 0.98                                           #body emissivity of carbon
    qrad = epsilon * sigma * Twall**4 
    
    print('qrad', qrad)
    print('qdiff2', -qdiff2)
    print('qdiff', qdiff)
    print('qcond', qcond)
    print('qadv', qadv)
    print('q', qcond+qdiff+qadv) #-qrad 

    qwtot = qcond+qdiff+qadv #-qrad

    dT_dx = (Tgas - Twall) / dx
    print('dT_dx \n', dT_dx)
    dT_dx2= (qwtot - qdiff- qadv)/lambda_
    print('dT_dx2 \n', dT_dx2)

    dT_dt = dT_dx * Mfreestream *343
    print('dT_dt \n', dT_dt)


    return qwtot, mblowtot, Numberdensity[0]   #, qdiff, qcond, qadv, Numberdensity[0], wdot


print("\n--- FREE STREAM CONDITIONS ---")
M_1 = 28.78
reff = 0.48 #HOW TO LINK IT TO link reff and the dx of the boundary layer.
alt = 61
#surface input
dx = reff*1e-4  # to be changed to the right value
Twall = 2000 #2823  #melting temperature of carbon
results = modele_gsi(M_1, alt, reff, Twall)
print('results model: qwtot, mblowtot, qdiff, qcond, qadv, Numberdensity[0], wdot', results)


print('with cabaret : Qw = 1238689.8407288808 W/m2 with the same input param M=20, reff = 0.5, alt = 60')
