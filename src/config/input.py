import numpy as np

altitude_list = np.linspace(30, 80, 20)
mach_list = np.linspace(20, 28, 20)
rad_list = np.linspace(0.1, 1, 20)

#HEAT FLUX COMPUTATION
#modele
pr = 0.713 # Prandtl number
L = 1.0 # Lewis number
Twall = 2000.0 # Wall temperature
dx = 4e-4  # to be changed to the right value
Na = 6.022e23 # avogadro number [mol^-1]

R=8.31446261815324

residual = 1.0e-10
throat_area =9.621e-04
Lewis =1.0
print_info = "No"
option = {"reservoir": {"pressure": 10000.0, 
                        "temperature":100.0,
                        "robust": "Yes"},
                        "massflow": {"pressure": 10.0, 
                                    "temperature": 2.0,
                                    "robust": "No"},
                        "shocking": {"ratio": 0.2,
                                    "robust": "No"},
                        "total":    {"pressure": 1.0, 
                                    "temperature": 1.0,
                                    "robust": "No"}
                        }

