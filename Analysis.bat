@echo off
pip install pyyaml
python programs/config_popup.py

python programs/update_config_files.py

call conda activate DEEPLABCUT
python programs/video_copy_fix.py
python programs/DLC_analysis.py

call conda activate simbaenv
python programs/files_copy_simba.py
python programs/simba_analysis.py
python programs/results.py
python programs/results_plotter.py
python programs/delete_files.py

pause