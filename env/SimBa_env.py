import subprocess

def run(command):
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"Command failed: {command}")
    return result.returncode

# run(f"conda create -n simbaenv python=3.6.10")

env='simbaenv'


# run(f"conda run -n {env} conda activate simbaenv")
# run (f"conda run -n {env} pip install simba-uw-tf-dev")
# run (f"conda run -n {env} pip uninstall shapely")
# run (f"conda run -n {env} conda install -c conda-forge shapely")
# run (f"conda run -n {env} conda install -c conda-forge ffmpeg")
# run (f"conda run -n {env} conda install cuda -c nvidia/label/cuda-12.8.0")
# run (f"conda run -n {env} pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128")
