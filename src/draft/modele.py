"""loop : see modele2!"""

import numpy as np
import sys
import time
import os

cabaret_src_folder = '/Users/jeannelonglune/Desktop/memoire/Mutationpp-master/src' # Change to your folder path
sys.path.insert(0, cabaret_src_folder)

mutation_folder = "/Users/jeannelonglune/Desktop/memoire/Mutationpp-master/" # Your folder
my_distribution = "macosx-13.0-arm64-3.11" # Your particular distribution
sys.path.append(mutation_folder + "_skbuild/" + my_distribution +"/cmake-install/interface/python/mutationpp")

## Importing local mutationpp python module ##
mppPyDir=os.environ.get('MPP_LOCALPY')
sys.path.append(mppPyDir)

from shock import shock
from total import total
from heatflux import heatflux
from atmUS76 import Atmosphere
import rebuilding_setup as setup
#import reading_input as input_data


#input 
alt = 70 
# Free stream conditions
#T_1 = 243 #data of the paper that should give a catalic heatflux of 3.488 MW/m^2 but for the moment I have Qw = 7392361.20 W/m2
#p_1 = 18.54
M_1 = 28.56
reff = 0.48
#heatflux 
pr = 0.713 # Prandtl number
L = 1.0 # Lewis number
#reff = 0.49 # Effective radius
T_w = 350.0 # Wall temperature



#def modele(alt, M_1, reff):
#p_1 = Atmosphere(alt)[1]
#T_1 = Atmosphere(alt)[2]
T_1 = 243 #data of the paper that should give a catalic heatflux of 3.488 MW/m^2 but for the moment I have Qw = 7392361.20 W/m2
p_1 = 18.54
print('INPUT')
print('Mach number : ' + str(M_1), 'altitude : ' + str(alt), 'pressure : ' + str(p_1), 'temperature : ' + str(T_1), "effective radius : " + str(reff))

# Mutation++ mixture setup
mix = setup.setup_mpp('/Users/jeannelonglune/Desktop/memoire/pyCabaret/input.in')

#SCHOCKING
# Specify module options
options = {"ratio": 0.2,  #limit bf infinite loop is 0.33 #initial guess rho1/rho2
       "robust": "No"}
#results for 0.33, 0.3, 0.2, 0.1 & Yes and No : Qw = -32753.33 W/m2 for any size
#not the same as in cabaret initial
#=> feel like I've an heaviside function... 

preshock_state = [T_1,p_1,M_1]

start_time = time.time()
T2,p2,v2 = shock(preshock_state,mix,options)
end_time = time.time()
exec_time = end_time - start_time
#print('T2 = ' + str(T2))
#print('v2 = ' + str(v2))
#print('p2 = ' + str(p2)) #p2 is really big... and same as pt2.

print('AFTER SHOCK')
print('T2 = '+ "{:.2f}".format(T2)+' K;', 'p2 = '+ "{:.2f}".format(p2)+' Pa;', 'v2 = '+ "{:.2f}".format(v2)+' m/s')
#print('Execution time = '+"{:.4f}".format(exec_time), ' seconds = '+"{:.4f}".format(exec_time/60), ' minutes')

#TOTAL QUANTITIES
options = {"pressure": 1, 
        "temperature": 1,
        "robust": "No"}  #change something here with robust or not

start_time = time.time()
Tt2 , pt2, vt2 = total(T2,p2,v2,1.0e-06,mix,"total",options) #changed total() bc only 2 output 
#print('pt2 in total quantities = ' + str(pt2))  #here pressure seems really big.

end_time = time.time()
exec_time = end_time - start_time

print('TOTAL QUANTITIES')
print('Tt2 = '+ "{:.2f}".format(Tt2)+' K;', 'pt2 = '+ "{:.2f}".format(pt2)+' Pa;', 'vt2 = '+ "{:.2f}".format(vt2)+' m/s')
#print('Execution time = '+"{:.4f}".format(exec_time), ' seconds = '+"{:.4f}".format(exec_time/60), ' minutes')

#HEAT FLUX COMPUTATION

#print('Tt2 = ' + str(Tt2))
#print('pt2 = ' + str(pt2))  #here pressure seems really big.

mix.equilibrate(Tt2, pt2)
ht2 = mix.mixtureHMass()
#print('ht2 mutation= '+ str(ht2))  # ht2 is neg here

print('reff'+ str(reff))
start_time = time.time()
qw = heatflux(mix, pr, L, p_1, pt2, Tt2, ht2, reff, T_w)
end_time = time.time()

exec_time = end_time - start_time

print('FINAL HEAT FLUX')
print('Qw = '+ "{:.2f}".format(qw)+' W/m2')

#print('Execution time = '+"{:.4f}".format(exec_time), ' seconds = '+"{:.4f}".format(exec_time/60), ' minutes')
#return qw


#heatflux_test = modele(70, 68, 0.49)
print('printheatfluxtext '+ str(qw))