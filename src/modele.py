import numpy as np
import sys
import time
import os
import config.muttconfig
import config.input


from shock import shock
from total import total
from heatflux import heatflux
import rebuilding_setup as setup
from atmUS76 import Atmosphere
from config.input import pr, L, Twall, Na



def modele(alt, M_1, reff) :
    """
    Computes heat flux using shock and total functions.

    Parameters:
    alt (float): Geometric altitude in kilometers.
    M_1 (float): Mach number of the incoming flow.
    reff (float): Effective radius.

    Returns:
    float: Heat flux computed using shock, total functions and heatflux is computed with the Fay and Riddel equation 
    which has strong assumptions.

    """
    p_1 = Atmosphere(alt)[0]
    T_1 = Atmosphere(alt)[1]

    mix = setup.setup_mpp('/Users/jeannelonglune/Desktop/memoire/pyCabaret/input.in')

    options1 = {"ratio": 0.2,  
            "robust": "Yes"}


    preshock_state = [T_1,p_1,M_1]

    T2,p2,v2 = shock(preshock_state,mix,options1)

    options2 = {"pressure": 1, 
        "temperature": 1,
        "robust": "Yes"}  

    Tt2 , pt2, vt2 = total(T2,p2,v2,1.0e-06,mix,"total",options2) 

    mix.equilibrate(Tt2, pt2)
    rhoigas = mix.densities()
    molarmass = mix.speciesMw()
    #compute number density : N = rho_mix Na / M mix  ([kg/m^3] [atoms/mole] / [kg/mole])
    Numberdensity = rhoigas * Na / molarmass
    
    ht2 = mix.mixtureHMass()
    qw = heatflux(mix, pr, L, p_1, pt2, Tt2, ht2, reff, Twall)

    return qw, Numberdensity[0]


#variables globales 
#p0 = 1
#t0 = 1
M_1 = 28.78
reff = 0.48 #HOW TO LINK IT TO THE linked to the dx of the boundary layer.
alt = 61 
test = modele(alt, M_1, reff)
print('test modele '+ str(test))
#paper full cat with those input param : circa 3.5 MW/m^2