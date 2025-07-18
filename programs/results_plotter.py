import simba
from pathlib import Path
import shutil

from simba.plotting.data_plotter import DataPlotter
import ressources.globals
from simba.outlier_tools.outlier_corrector_location import OutlierCorrecterLocation

from simba.pose_importers.dlc_importer_csv import import_dlc_csv_data

from simba.mixins.config_reader import read_config_file
from simba.feature_extractors.feature_extractor_8bp import ExtractFeaturesFrom8bps
from simba.roi_tools.ROI_analyzer import ROIAnalyzer
from simba.plotting.roi_plotter import ROIPlotter

from simba.model.inference_batch import InferenceBatch

from simba.plotting.single_run_model_validation_video import ValidateModelOneVideo
from simba.plotting.plot_clf_results import PlotSklearnResultsSingleCore

from simba.plotting.frame_mergerer_ffmpeg import FrameMergererFFmpeg


# === Définition des chemins principaux ===
project_path = Path("programs/ressources/self_grooming_mice/project_folder")
config_path = project_path / "project_config.ini"      # Chemin vers le fichier de config du projet
video_path = project_path / "videos"                    # Dossier des vidéos

# Liste des vidéos .mp4 en format Path puis converties en chaînes
videos_folder = Path("programs/ressources/self_grooming_mice/project_folder/videos")
video_files = list(videos_folder.glob("*.mp4"))  
video_files_str = [str(p) for p in video_files]        # Conversion en str pour les fonctions Simba

# Liste des fichiers CSV de résultats machine learning
csv_folder = project_path / "csv/machine_results"
csv_files = list(csv_folder.glob("*.csv"))
csv_files_str = [str(p) for p in csv_files]


# === Création des ROI (regions of interest) sur les vidéos si demandé ===
if ressources.globals.make_roi:
    for video_path in video_files_str:
        test = ROIPlotter(
            config_path,
            video_path=video_path,
            body_parts=['Center'],               # Points d’intérêt à afficher
            style_attr={'show_body_part': True, 'show_animal_name': False}  # Options d’affichage
        )
        test.run()  # Lance la création et visualisation des ROI
        

# === Affichage des résultats du classificateur si demandé ===
if ressources.globals.make_classifier:
    test = PlotSklearnResultsSingleCore(
        config_path=config_path,
        video_setting=True,       # Afficher les résultats vidéo
        frame_setting=False,      # Pas d’affichage par frame individuelle
        video_paths=video_files_str,
        print_timers=True,        # Affiche les temps d’exécution
        rotate=False              # Ne pas faire de rotation dans la visualisation
    )
    test.run()  # Exécute l’affichage


# === Copie des vidéos ROI dans un dossier de sortie local si demandé ===
if ressources.globals.make_roi:
    ROI_path = project_path / "frames/output/ROI_analysis"
    for file in ROI_path.glob("*.mp4"):
        shutil.copy(Path(file), "output/ROI")  # Copie les fichiers vidéos ROI dans output/ROI


# === Copie des vidéos résultats classificateur dans un dossier local si demandé ===
if ressources.globals.make_classifier:
    class_path = project_path / "frames/output/sklearn_results"
    for file in class_path.glob("*.mp4"):
        shutil.copy(Path(file), "output/classifier")  # Copie les vidéos dans output/classifier
