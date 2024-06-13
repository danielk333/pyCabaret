import sys
import os

#To run locally and find the modules in /src
cabaret_src_folder = '/Users/jeannelonglune/Desktop/memoire/Mutationpp-master/src'
sys.path.insert(0, cabaret_src_folder)

mutation_folder = "/Users/jeannelonglune/Desktop/memoire/Mutationpp/" 
my_distribution = "macosx-13.0-arm64-3.11" 
sys.path.append(mutation_folder + "_skbuild/" + my_distribution +"/cmake-install/interface/python/mutationpp")

mppPyDir=os.environ.get('MPP_LOCALPY')
sys.path.append(mppPyDir)