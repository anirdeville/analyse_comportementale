from ressources import run_terminal as rt
import ressources
import os
from pathlib import Path

os.chdir("ressources")

rt.rt("conda env create -f DLC.yaml")
rt.rt("conda activate DEEPLABCUT")

rt.rt("conda install -c conda-forge pytables==3.8.0")
rt.rt("conda install deeplabcut[gui]")
rt.rt("conda install cuda -c nvidia/label/cuda-12.8.0")
rt.rt("pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128")
rt.rt("pip install tensorflow")
rt.rt("pip install tensorpack")
