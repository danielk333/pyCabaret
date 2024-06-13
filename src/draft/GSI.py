import sys
import os
import numpy as np
import config.muttconfig

import _mutationpp as mpp

mix = mpp.Mixture("N")
ns = mix.nSpecies()
nT = mix.nEnergyEqns()
pos_T_trans = 0
set_state_with_rhoi_T = 1

Tgas = 6000.
Pgas = 1000.
mix.equilibrate(Tgas, Pgas)


rhoigas =  mix.densities()
Xgas = mix.X()  #Returns the current species mole fractions.
print('Xgas, Returns the current species mole fractions', Xgas)
Twall = 2500.
dx = 1e-2

mix.setState(rhoigas, Tgas, set_state_with_rhoi_T)   #Sets the state of the mixture using the StateModel belonging to the mixture.
           #"The input variables depend on the type of StateModel being used.

mix.setSurfaceState(rhoigas, Tgas, set_state_with_rhoi_T)
mix.setDiffusionModel(Xgas, dx) 
mix.solveSurfaceBalance()
[rhoiwall, Twall] = mix.getSurfaceState(set_state_with_rhoi_T)

mix.setState(rhoiwall, Twall, set_state_with_rhoi_T)
print(Twall)
Ygas = mix.Y() #Returns the current species mass fractions.
print('\n Ygas, current species mass fraction', Ygas)
print('\n rhoigas sum ', rhoigas.sum()) 

print("\nSurface mass fractions:")
for i in range(mix.nSpecies()):
    print(mix.speciesName(i) + ": " + str(rhoigas[i] / rhoigas.sum()))


wdot = mix.surfaceReactionRates()
print('wdot', wdot)
print("\nSurface reaction rates:")
for i in range(mix.nSpecies()):
    print(mix.speciesName(i) + ": " + str(wdot[i]))

mblow = mix.getMassBlowingRate()
print("\nMass blow [kg/(m^2-s)]: " + str(mblow))

mix.setState(rhoigas, Twall, set_state_with_rhoi_T)
E_field = 0.0
lambda_ = mix.frozenThermalConductivity() #should change this no? 

qcond = lambda_ * (Tgas - Twall) / dx  #Tw : temperature of the wall
xw=1 #makes sens? 
v_b = (Xgas - xw) / dx  # mass fractions
#v_b = 1 #mass fraction
v_Vd_sm = np.zeros(ns)
print('v_b', v_b)
print('E', E_field)
qdiff = 0
R=8.31446261815324
h = mix.speciesHOverRT() *R *Twall
#h = output["Total_enthalpy"] #output is model? not sure, check notes bc otherwise no modification on the heatflux computation

v_Vd_sm, E_field = mix.stefanMaxwell(v_b) 
print('v_Vd_sm', v_Vd_sm)
print('rhoi_gas', rhoigas)
print('h', h)
qdiff = np.sum(v_Vd_sm * rhoigas * h)

q = qcond+qdiff
print('q', q)
print('qcond', qcond)
print('qdiff', qdiff)
print('mblow', mblow)