import os

# Liste des noms de dossiers à créer
dossier_liste = ["train-image", "train-bigger-image", "retrain-image", "test-image", "temp-image", "to-validate-image"]

# Parcours de la liste
for dossier in dossier_liste:
    # Vérifie si le dossier existe
    if not os.path.exists(dossier):
        # Crée le dossier s'il n'existe pas
        os.makedirs(dossier)