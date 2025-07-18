import simba
from pathlib import Path
import ressources.globals
import os
import shutil

from simba.outlier_tools.skip_outlier_correction import OutlierCorrectionSkipper
from simba.pose_importers.dlc_importer_csv import import_dlc_csv_data  # Import de l'importateur CSV DLC (non utilisé ici)

from simba.mixins.config_reader import read_config_file
from simba.feature_extractors.feature_extractor_8bp import ExtractFeaturesFrom8bps
from simba.roi_tools.ROI_analyzer import ROIAnalyzer
from simba.plotting.roi_plotter import ROIPlotter

from simba.model.inference_batch import InferenceBatch

from simba.plotting.single_run_model_validation_video import ValidateModelOneVideo

from simba.plotting.plot_clf_results import PlotSklearnResultsSingleCore


# === Définition des chemins principaux ===
project_path = Path("programs/ressources/self_grooming_mice/project_folder")
config_path = project_path / "project_config.ini"
video_path = project_path / "videos"


# === Correction des outliers (valeurs aberrantes) sur les données vidéos ===
outlier_skip = OutlierCorrectionSkipper(config_path=config_path)
outlier_skip.run()


# === Extraction des features (caractéristiques) à partir des vidéos traitées ===
feature_extractor = ExtractFeaturesFrom8bps(config_path)
feature_extractor.run()


# === Analyse des régions d’intérêt (ROI) avec calcul des distances et données détaillées ===
roi_analysis = ROIAnalyzer(
    config_path,
    calculate_distances=True,
    detailed_bout_data=True,
    body_parts=['Center'],  # Partie du corps ciblée pour l’analyse
    threshold=0.0
)
roi_analysis.run()
roi_analysis.save()  # Sauvegarde les résultats de l’analyse ROI


# === Exécution du modèle d'inférence en batch sur les vidéos ===
inferencer = InferenceBatch(config_path)
inferencer.run()


# === Préparation de la liste des vidéos au format chaîne pour l’utilisation ultérieure ===
videos_folder = Path("programs/ressources/self_grooming_mice/project_folder/videos")
video_files = list(videos_folder.glob("*.mp4"))  # Recherche tous les fichiers .mp4
video_files_str = [str(p) for p in video_files]  # Conversion des Path en chaînes de caractères


# === Fonction utilitaire pour déplacer les vidéos d'un dossier source vers un dossier destination ===
def move_videos(source, dest):
    only_mp4 = []  # Liste des fichiers mp4 trouvés
    for f in os.listdir(source):
        name, ext = os.path.splitext(f)
        if ext.lower() == '.mp4':
            only_mp4.append(f)
            src_file = os.path.join(source, f)
            dst_file = os.path.join(dest, f)

            try:
                shutil.move(src_file, dst_file)  # Déplace le fichier
                print(f"📁 Moved '{f}' to '{dest}'")
            except Exception as e:
                print(f"❌ Failed to move '{f}': {e}")


# === Création et déplacement des vidéos d’analyse ROI si demandé ===
if ressources.globals.make_roi:
    for video_path in video_files_str:
        roi = ROIPlotter(
            config_path,
            video_path=video_path,
            body_parts=['Center'],
            style_attr={'show_body_part': True, 'show_animal_name': False}
        )
        roi.run()

    source_path = project_path / "frames/output/ROI_analysis"
    dest_path = Path("output/ROI")
    move_videos(source_path, dest_path)


# === Création et déplacement des vidéos issues du classificateur si demandé ===
if ressources.globals.make_classifier:
    classifier = PlotSklearnResultsSingleCore(
        config_path=config_path,
        video_setting=True,
        frame_setting=False,
        video_paths=video_files_str,
        print_timers=True,
        rotate=False
    )
    classifier.run()

    source_path = project_path / "frames/output/sklearn_results"
    dest_path = Path("output/classifier")
    move_videos(source_path, dest_path)
