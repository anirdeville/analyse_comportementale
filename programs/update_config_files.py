from pathlib import Path
import tkinter as tk
from tkinter import filedialog
import shutil
from configparser import ConfigParser
import yaml


# Define your project root
project_root = Path("programs/ressources/self_grooming_mice")
project_folder = project_root / "project_folder"
model_dir = project_root / "models/generated_models"

# Load config
config_path = project_folder / "project_config.ini"
config = ConfigParser()
config.read(config_path)

# Update paths in config
config.set("General settings", "project_path", str(project_folder.resolve()))
config.set("SML settings", "model_dir", str(model_dir.resolve()))
config.set("SML settings", "model_path_1", str((model_dir / "self_grooming.sav").resolve()))

# Save updated config
with open(config_path, "w") as f:
    config.write(f)

print("✅ Config paths updated with general platform-independent paths.")


# Définir le chemin du projet
project_path = Path("programs/ressources/model").resolve()
yaml_file = project_path / "config.yaml"  # <-- adapte ce nom si nécessaire

# Charger le YAML
with open(yaml_file, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# Rendre le chemin du projet absolu et propre
config["project_path"] = str(project_path)

# # Convertir les paths vidéo en relatifs
# new_video_sets = {}
# for abs_path, params in config["video_sets"].items():
#     abs_path_obj = Path(abs_path).resolve()
#     try:
#         rel_path = abs_path_obj.relative_to(project_path)
#     except ValueError:
#         # Si le chemin est externe, on le garde relatif depuis "videos/"
#         videos_folder = project_path / "videos"
#         if videos_folder in abs_path_obj.parents:
#             rel_path = abs_path_obj.relative_to(project_path)
#         else:
#             print(f"⚠️ Vidéo en dehors du dossier projet : {abs_path_obj}")
#             rel_path = abs_path_obj.name  # Fallback: nom de fichier seul
#     new_video_sets[str(rel_path).replace("\\", "/")] = params

# # Remplacer les chemins dans le YAML
# config["video_sets"] = new_video_sets

# Sauvegarder le nouveau fichier YAML
with open(yaml_file, "w", encoding="utf-8") as f:
    yaml.dump(config, f, default_flow_style=False, sort_keys=False)

print("✅ YAML mis à jour avec des chemins relatifs.")