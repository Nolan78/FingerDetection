import os
import cv2
import numpy as np

# Chemin du dossier d'origine contenant les images
input_folder = 'train-image'

# Chemin du dossier de destination pour les images décalées
output_folder = 'train-image-decalle-banger'

# Vérification et création du dossier de destination s'il n'existe pas
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Liste des sous-dossiers correspondant aux chiffres
subfolders = [str(i) for i in range(10)]

# Parcours des sous-dossiers
for subfolder in subfolders:
    input_subfolder = os.path.join(input_folder, subfolder)
    output_subfolder = os.path.join(output_folder, subfolder)
    
    # Vérification et création du sous-dossier de destination pour le chiffre s'il n'existe pas
    if not os.path.exists(output_subfolder):
        os.makedirs(output_subfolder)
    
    # Parcours des images dans le sous-dossier
    for filename in os.listdir(input_subfolder):
        print("Image de la classe : " + subfolder + " fichier : " + filename)
        image_path = os.path.join(input_subfolder, filename)
        output_path = os.path.join(output_subfolder, filename)
        
        # Lecture de l'image
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        
        # Sauvegarde de l'image d'origine
        cv2.imwrite(os.path.join(output_subfolder, f"original_{filename}"), image)
        
        # Décalages avec différents nombres de pixels
        for pixels in range(1, 4):
            # Décalage de l'image vers la gauche
            shifted_left = np.roll(image, -pixels, axis=1)
            cv2.imwrite(os.path.join(output_subfolder, f"left_{pixels}_{filename}"), shifted_left)
            
            # Décalage de l'image vers la droite
            shifted_right = np.roll(image, pixels, axis=1)
            cv2.imwrite(os.path.join(output_subfolder, f"right_{pixels}_{filename}"), shifted_right)
            
            # Décalage de l'image vers le haut
            shifted_up = np.roll(image, -pixels, axis=0)
            cv2.imwrite(os.path.join(output_subfolder, f"up_{pixels}_{filename}"), shifted_up)
            
            # Décalage de l'image vers le bas
            shifted_down = np.roll(image, pixels, axis=0)
            cv2.imwrite(os.path.join(output_subfolder, f"down_{pixels}_{filename}"), shifted_down)
