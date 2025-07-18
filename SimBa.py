import subprocess

def run(command):
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"Command failed: {command}")
    return result.returncode

run(f"conda activate simbaenv")
run(f"conda run -n {'simbaenv'} simba") 