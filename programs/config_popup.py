import tkinter as tk
from pathlib import Path

# Chemin vers le fichier globals.py que l'on souhaite mettre à jour
globals_file = Path("programs/ressources/globals.py")

def save_and_exit():
    """
    Récupère les valeurs des cases à cocher et les écrit dans le fichier globals.py.
    Ferme ensuite la fenêtre.
    """
    make_roi_val = roi_var.get()
    make_classifier_val = classifier_var.get()
    keep_files_val = keep_files_var.get()

    # Contenu du fichier globals.py généré automatiquement
    new_content = f"""# globals.py (auto-updated)
make_roi = {make_roi_val}
make_classifier = {make_classifier_val}
keep_files = {keep_files_val}
"""
    # Écriture du contenu dans le fichier
    globals_file.write_text(new_content)
    print("✅ globals.py updated.")
    root.destroy()

# === Interface graphique ===
root = tk.Tk()
root.title("Configure Global Variables")

# Titre descriptif
tk.Label(root, text="Choose your processing options:").pack(pady=10)

# Déclaration des variables associées aux cases à cocher
roi_var = tk.BooleanVar()
classifier_var = tk.BooleanVar()
keep_files_var = tk.BooleanVar()

# Cases à cocher pour les différentes options
tk.Checkbutton(root, text="Generate ROI Videos (much longer)", variable=roi_var).pack(anchor='w', padx=20)
tk.Checkbutton(root, text="Generate Classifier Videos (much longer)", variable=classifier_var).pack(anchor='w', padx=20)
tk.Checkbutton(root, text="Keep intermediate/generated files", variable=keep_files_var).pack(anchor='w', padx=20)

# Bouton de validation
tk.Button(root, text="Save & Exit", command=save_and_exit).pack(pady=15)

# Lancement de la boucle principale de l'interface
root.mainloop()
