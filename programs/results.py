import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

# Dossier contenant les fichiers CSV de résultats machine de SIMBA
folder_path = Path("programs/ressources/self_grooming_mice/project_folder/csv/machine_results")

# Paramètres de calibration
pixels_per_mm = 1.60689
cm_per_pixel = 1 / (pixels_per_mm * 10)
fps = 30  # Images par seconde

# Génère le nom de fichier de sortie daté
date_str = datetime.now().strftime("%Y%m%d")
output_path = "output/analysis_summary"
dated_output_path = f"{output_path}_{date_str}" + ".txt"

# Recherche du fichier contenant les temps passés dans les ROIs
logs_path = Path("programs/ressources/self_grooming_mice/project_folder/logs")
index = 0
for csv_file in logs_path.glob("*.csv"):
    csv_name = csv_file.name.split("_")[1]
    if csv_name == "time":
        ROI_file_path = Path.resolve(csv_file)

# Ouvre le fichier de sortie pour écrire le résumé d’analyse
with open(dated_output_path, 'w') as f:
    f.write(f"Analysis Summary for folder: {folder_path.name}\n\n")
    
    # Charge le fichier de temps passé dans chaque ROI
    dROI = pd.read_csv(ROI_file_path, usecols=["VIDEO", "SHAPE", "TIME (S)"])

    # Parcours de chaque fichier CSV de résultats dans le dossier
    for csv_file in folder_path.glob('*.csv'):
        df = pd.read_csv(csv_file)

        # Filtrage des points avec une faible vraisemblance (< 0.3)
        df = df[df['Lat_right_p'] >= 0.3]

        # Suppression des lignes contenant des coordonnées manquantes
        df = df.dropna(subset=['Lat_right_x', 'Lat_right_y'])

        # Calcul de la distance totale parcourue (entre images successives)
        dx = df['Lat_right_x'].diff()
        dy = df['Lat_right_y'].diff()
        pixel_distances = np.sqrt(dx**2 + dy**2)
        total_distance_cm = pixel_distances.sum() * cm_per_pixel

        # Calcul du temps total de toilettage détecté
        grooming_frames = df["self_grooming"].sum()
        total_grooming_time_seconds = grooming_frames / fps

        # Écriture des résultats globaux dans le fichier
        f.write(f"{csv_file.name}:\n")
        f.write(f"  - Total distance (Center): {total_distance_cm:.2f} cm\n")
        f.write(f"  - Total grooming time: {total_grooming_time_seconds:.2f} seconds\n\n")

        # Écriture des temps passés dans chaque ROI pour cette vidéo
        f.write(f"Total time spent in ROIs :\n")
        dROI_temp = dROI[dROI["VIDEO"] == csv_file.stem]
        dROI_temp = dROI_temp.reset_index(drop=True)
        print(dROI_temp)

        for i in range(5):
            roi_time = round(float(dROI_temp['TIME (S)'][i]), 2)
            roi_time = str(roi_time)
            f.write(f"  - {dROI_temp['SHAPE'][i]} : {roi_time} seconds\n")

        f.write(f"\n\n")
        index += 1

# Affiche un message une fois toutes les vidéos traitées
print(f"\nProcessed all files in folder: {folder_path.name}")
