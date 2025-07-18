from pathlib import Path
import yaml
import ressources.globals  # Import des variables globales définies dans globals.py

# Liste des dossiers dans lesquels les fichiers doivent éventuellement être supprimés
folders = [
    "videos",
    "videos/fixed",
    "videos/csv",
    "programs/ressources/self_grooming_mice/project_folder/videos",
    "programs/ressources/self_grooming_mice/project_folder/logs",

    # Dossiers de sortie utilisés dans SimBA pour stocker les résultats
    "programs/ressources/self_grooming_mice/project_folder/frames/output/live_data_table",
    "programs/ressources/self_grooming_mice/project_folder/frames/output/ROI_analysis",
    "programs/ressources/self_grooming_mice/project_folder/frames/output/sklearn_results",

    # Dossiers CSV utilisés pour stocker différentes étapes de traitement
    "programs/ressources/self_grooming_mice/project_folder/csv/machine_results",
    "programs/ressources/self_grooming_mice/project_folder/csv/input_csv",
    "programs/ressources/self_grooming_mice/project_folder/csv/features_extracted",
    "programs/ressources/self_grooming_mice/project_folder/csv/outlier_corrected_movement_location"
]

# Fichiers que l'on ne doit jamais supprimer (nom sans extension)
protected_files = {"video_info", "project_log"}

# Suppression des fichiers dans les dossiers, uniquement si keep_files est désactivé
if not ressources.globals.keep_files:
    for folder in folders:
        path = Path(folder)
        for file in path.glob("*"):  # Parcourt de tous les fichiers du dossier
            if file.is_file():
                if file.stem in protected_files:
                    print(f"⛔ Skipped protected file: {file.name}")
                    continue
                try:
                    file.unlink()  # Suppression du fichier
                    print(f"🗑️ Deleted: {file.name}")
                except Exception as e:
                    print(f"❌ Failed to delete {file.name}: {e}")


# === Nettoyage du fichier de configuration DeepLabCut ===

# Chemin vers le fichier config.yaml de DeepLabCut
dlc_config_path = Path("programs/ressources/model/config.yaml")

# Chargement du fichier YAML
with open(dlc_config_path, "r") as f:
    config = yaml.safe_load(f)

# Réinitialisation de la section "video_sets" (permet de supprimer tous les anciens chemins de vidéos)
config["video_sets"] = {}

# Sauvegarde du fichier YAML modifié
with open(dlc_config_path, "w") as f:
    yaml.dump(config, f, default_flow_style=False)

print("🗑️ All video_sets removed from config.yaml.")
