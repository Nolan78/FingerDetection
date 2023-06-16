import os
import shutil
import streamlit as st
from PIL import Image

# Chemin du dossier contenant les images à valider
dossier_parent = "../to-validate-image"

def afficher_images_dossier(dossier_parent):
    # Liste des chemins des images
    chemins_images = []

    # Parcourir tous les sous-dossiers
    for sous_dossier in os.listdir(dossier_parent):
        chemin_sous_dossier = os.path.join(dossier_parent, sous_dossier)
        # Vérifier si c'est un dossier
        if os.path.isdir(chemin_sous_dossier):
            # Parcourir les fichiers dans le sous-dossier
            for fichier in os.listdir(chemin_sous_dossier):
                chemin_image = os.path.join(chemin_sous_dossier, fichier)
                # Vérifier si c'est un fichier image
                if os.path.isfile(chemin_image) and fichier.endswith((".jpg", ".jpeg", ".png")):
                    # Ajouter le chemin de l'image à la liste
                    chemins_images.append(chemin_image)

    # si il n'y a pas d'image
    if len(chemins_images) == 0:
        st.write("Il n'y a pas d'image à verifier.")
        return
    # Afficher l'image actuelle
    chemin_image_actuel = chemins_images[0]
    image = Image.open(chemin_image_actuel)
    st.image(image, caption=chemin_image_actuel, use_column_width=True, width=100)   
    st.write("Le numéro de l'image a verfier est "+ str(chemin_image_actuel[-5:-4]))

    # Boutons pour les actions
    if st.button("Valider", key="valider"+str(chemin_image_actuel) ):
        # On met l'url de l'image dans le dossier retrain-image et le dossier correspondant au numéro
        shutil.move(chemin_image_actuel, "../retrain-image/"+chemin_image_actuel[-5:-4])

        st.info("L'image a été validée.")
        st.experimental_rerun()
    
    if st.button("Supprimer", key="supprimer"+str(chemin_image_actuel)):
        st.write("Image supprimée :", chemin_image_actuel)
        os.remove(chemin_image_actuel)
        st.info("L'image a été supprimée.")
        st.experimental_rerun()

    name = st.text_input('Numéro')
    if st.button("Changer le numéro", key="changer_numero"+str(chemin_image_actuel) ):
        # Saisie du nouveau numéro
        if not name:
            st.warning('Please input a numéro.')
            st.stop()
        # On renomme l'image avec le numéro 1686822100-x.jpg (x = numéro) et on la met dans le dossier retrain-image
        chemin_image_nouveau = chemin_image_actuel.replace(chemin_image_actuel[-5:-4], name)
        os.rename(chemin_image_actuel, chemin_image_nouveau) 
        # On met l'url de l'image dans le dossier retrain-image et le dossier correspondant au numéro
        shutil.move(chemin_image_nouveau, "../retrain-image/"+name)
        st.info("L'image a été renommée.")
        st.experimental_rerun()

# Appel de la fonction pour afficher les images
afficher_images_dossier(dossier_parent)

def show_page(self):
    st.header(self.title)
        
    st.write("Vérification des images !")
    afficher_images_dossier(dossier_parent)