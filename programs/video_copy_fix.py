from pathlib import Path
import subprocess
import tkinter as tk
from tkinter import filedialog
import os
import shutil
import ressources.globals

# === Sélection du dossier source contenant les vidéos MP4 via une fenêtre Tkinter ===
root = tk.Tk()
root.withdraw()  # Cache la fenêtre principale Tkinter
ressources.globals.video_source_folder = filedialog.askdirectory(title="Select directory containing MP4 videos")

# === Définition des dossiers vidéo locaux ===
video_folder = Path("videos")              # Dossier où seront copiées les vidéos
output_folder = video_folder / "fixed"    # Dossier de sortie pour les vidéos corrigées

only_mp4 = []  # Liste qui stockera uniquement les fichiers MP4 détectés

# === Copie des fichiers MP4 depuis le dossier source sélectionné vers le dossier local "videos" ===
for f in os.listdir(ressources.globals.video_source_folder):
    name, ext = os.path.splitext(f)
    if ext.lower() == '.mp4':
        only_mp4.append(f)
        src_file = os.path.join(ressources.globals.video_source_folder, f)  # Chemin source complet
        dst_file = os.path.join(video_folder, f)                            # Chemin destination complet

        try:
            shutil.copyfile(src_file, dst_file)
            print(f"📁 Copied '{f}' to '{video_folder}'")
        except Exception as e:
            print(f"❌ Failed to copy '{f}': {e}")

print(only_mp4)  # Affiche la liste des fichiers MP4 copiés

# === Re-encodage des vidéos avec ffmpeg en utilisant le GPU NVIDIA ===
# Liste de tous les fichiers MP4 dans le dossier local "videos"
video_paths = [p.resolve() for p in video_folder.glob("*.mp4")]

for input_video in video_paths:
    output_video = output_folder / f"fixed_{input_video.name}"  # Nom du fichier de sortie préfixé "fixed_"

    # Commande ffmpeg pour ré-encoder la vidéo en H264 via NVENC avec accélération CUDA
    cmd = [
        "ffmpeg",
        "-hwaccel", "cuda",           # Active l'accélération matérielle GPU via CUDA (optionnel mais recommandé)
        "-i", str(input_video),       # Vidéo d'entrée
        "-c:v", "h264_nvenc",         # Utilisation du codec vidéo NVIDIA NVENC
        "-preset", "fast",            # Préréglage d'encodage rapide (équilibre vitesse/qualité)
        "-cq", "23",                  # Niveau de qualité constant NVENC (plus bas = meilleure qualité)
        "-c:a", "copy",               # Copie la piste audio sans la ré-encoder
        str(output_video)             # Vidéo de sortie
    ]

    print(f"🔧 Re-encoding {input_video.name}...")
    result = subprocess.run(cmd)  # Exécution de la commande ffmpeg

    # Vérification du succès de l'encodage
    if result.returncode == 0:
        print(f"✅ Saved: {output_video.name}")
    else:
        print(f"❌ Failed: {input_video.name}")
