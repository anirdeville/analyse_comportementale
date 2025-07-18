from pathlib import Path
import tkinter as tk
from tkinter import filedialog
import deeplabcut
import ressources.globals  # Accès aux variables globales comme make_roi ou make_classifier

# === Configuration de DeepLabCut ===
config_path = "programs/ressources/model/config.yaml"  # Chemin vers le fichier de configuration du projet DLC

# === Définition des dossiers ===
destfolder = Path("videos/csv").resolve()         # Dossier de sortie pour les fichiers CSV générés
video_folder = Path("videos/fixed")               # Dossier contenant les vidéos à analyser
video_paths = [str(p.resolve()) for p in video_folder.glob("*.mp4")]  # Liste des chemins absolus des vidéos .mp4

# === Lancement de l’analyse avec DeepLabCut ===
deeplabcut.analyze_videos(
    config=config_path,
    videos=video_paths,           # Liste des vidéos à analyser
    videotype="mp4",              # Format des vidéos
    shuffle=1,                    # Shuffle utilisé lors de l'entraînement (1 par défaut)
    save_as_csv=True,            # Sauvegarder aussi les résultats en format CSV
    destfolder=str(destfolder),  # Dossier de destination pour les résultats
    allow_growth=True,           # Permet à TensorFlow d'utiliser uniquement la mémoire GPU nécessaire
    gputouse=0,                  # GPU à utiliser (ici GPU 0)
    batch_size=8                 # Taille du batch pour l'analyse
)

# === Extraction des frames avec détection d'outliers (fausses prédictions) ===
deeplabcut.extract_outlier_frames(
    config=config_path,
    videos=video_paths
)