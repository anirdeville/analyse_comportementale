from pathlib import Path
import shutil
from simba.mixins.config_reader import read_config_file
import subprocess
import csv

# Paramètres du projet
project_path = Path("programs/ressources/self_grooming_mice/project_folder")
config_path = project_path / "project_config.ini"

# Dossiers de destination des vidéos et CSV
video_dest = project_path / "videos"
csv_dest = project_path / "csv/input_csv"

# Dossiers contenant les vidéos corrigées et les CSV produits par DLC
video_folder = Path("videos/fixed")
csv_folder = Path("videos/csv")

# Fichier de métadonnées
metadata_csv = project_path / "logs/video_info.csv"

# Chargement du fichier de configuration SIMBA
cfg = read_config_file(str(config_path))

# Copie des vidéos dans le dossier du projet SIMBA
for video_file in video_folder.glob("*.mp4"):
    video_name = video_file.name
    try:
        shutil.copy(video_file, video_dest / video_name)
        print(f"🎞️ Copied video: {video_name}")
    except Exception as e:
        print(f"❌ Error copying video {video_name}: {e}")

    # Ajout ou mise à jour des métadonnées associées à la vidéo
    video_stem = video_file.stem
    fps = 30 if "564" not in video_stem else 29  # Framerate ajusté selon l'identifiant
    resolution_width = 1296
    resolution_height = 972
    distance_mm = 450
    pixels_per_mm = 1.60689

    # Vérifie si la vidéo est déjà dans le fichier de métadonnées
    existing_videos = set()
    if metadata_csv.exists():
        with open(metadata_csv, mode='r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_videos.add(row['Video'])

    # Écrit les métadonnées si la vidéo n'est pas encore enregistrée
    if video_stem not in existing_videos:
        write_header = not metadata_csv.exists()
        with open(metadata_csv, mode='a', newline='') as f:
            writer = csv.writer(f)
            if write_header:
                writer.writerow(["Video", "fps", "Resolution_width", "Resolution_height", "Distance_in_mm", "pixels/mm"])
            writer.writerow([video_stem, fps, resolution_width, resolution_height, distance_mm, pixels_per_mm])
        print(f"📝 Metadata added for: {video_stem}")
    else:
        print(f"⚠️ Metadata already exists for: {video_stem}")

# Copie des fichiers CSV de DLC dans le dossier d'entrée de SIMBA
for csv_file in csv_folder.glob("*.csv"):
    csv_name = csv_file.name.split("DLC")[0] + ".csv"
    try:
        shutil.copy(csv_file, csv_dest / csv_name)
        print(f"📄 Copied csv: {csv_name}")
    except Exception as e:
        print(f"❌ Error copying csv {csv_name}: {e}")
