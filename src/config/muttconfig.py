import sys
import os
import pathlib

# To run locally and find the modules in /src
cabaret_src_folder = pathlib.Path(__file__).resolve().parents[1]

sys.path.insert(0, cabaret_src_folder)

MPP_DIRECTORY = "/home/danielk/git/Mutationpp/"
my_distribution = "linux-x86_64-3.12"
libfolder = (
    MPP_DIRECTORY
    + "_skbuild/"
    + my_distribution
    + "/cmake-install/interface/python/mutationpp"
)
sys.path.append(libfolder)

# mppPyDir=os.environ.get('MPP_LOCALPY')
# sys.path.append(mppPyDir)

os.environ["MPP_DIRECTORY"] = MPP_DIRECTORY
os.environ["MPP_DATA_DIRECTORY"] = f"{MPP_DIRECTORY}/data"
os.environ["PATH"] = f"{MPP_DIRECTORY}/install/bin:{os.environ['PATH']}"
if "LD_LIBRARY_PATH" not in os.environ:
    os.environ["LD_LIBRARY_PATH"] = ""
os.environ["LD_LIBRARY_PATH"] = (
    f"{MPP_DIRECTORY}/install/lib:{os.environ['LD_LIBRARY_PATH']}"
)
