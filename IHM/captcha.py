import streamlit as st
import time
import shutil
import base64
from PIL import Image
import os
import random
from streamlit_drawable_canvas import st_canvas
import numpy as np
from keras.models import load_model
from keras.utils import load_img, img_to_array
import colorama


st.set_page_config(page_title="Google Killer", page_icon="📝", layout="wide")

def bind_socket():
    global randomNumber
    randomNumber = random.randint(0, 9)
    print("Random number: ", randomNumber) 

bind_socket()

# Initialiser colorama
colorama.init()



# Define canvas parameters
canvas_width = 200
canvas_height = 200
stroke_width = 15

def preprocess_image(img_path):
    img = load_img(img_path, target_size=(28, 28), color_mode = "grayscale")
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x /= 255.
    return x

def show_page(self):
    st.header(self.title)
    # st.write("Captcha")
        
    # Center the canvas
    col1, col2 = st.columns(2)
    with col1:
        st.write("Nous voudrions un " + str(randomNumber) + " !")
    with col2:
        # Sélection de la couleur de fond
        background_color = st.color_picker("Couleur de fond", "#000000")

        # Sélection de la couleur du pinceau
        brush_color = st.color_picker("Couleur du pinceau", "#ffffff")


        canvas_result = st_canvas(
            # fill_color="rgba(255, 165, 0, 0.3)",  # Initial fill color
            # fill_color=brush_color,
            stroke_width=stroke_width,  # Stroke width
            stroke_color=brush_color,  # Stroke color
            # background_color="black",  # Background color
            background_color=background_color,  # Background color
            width=canvas_width,
            height=canvas_height,
            drawing_mode="freedraw",  # Drawing mode (freehand drawing)
            key="canvas"
        )

    # Save the drawn image upon button click
    if st.button("Save"):
        if canvas_result.image_data is not None:
            # Convertir le résultat du canvas en image
            image_data = np.array(canvas_result.image_data)

            # Convertir les couleurs en format hexadécimal en valeurs RVB entières
            brush_color_rgb = tuple(int(brush_color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
            background_color_rgb = tuple(int(background_color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))

            # Définir la tolérance de comparaison
            tolerance = 10

            # Réformer l'image avec la couleur du pinceau en blanc et la couleur de fond en noir
            brush_mask = np.all(np.abs(image_data[:, :, :3].astype(int) - np.array(brush_color_rgb)) <= tolerance, axis=-1)
            background_mask = np.all(np.abs(image_data[:, :, :3].astype(int) - np.array(background_color_rgb)) <= tolerance, axis=-1)
            image_data[brush_mask] = [255, 255, 255, 255]  # Couleur du pinceau en blanc
            image_data[background_mask] = [0, 0, 0, 255]  # Couleur de fond en noir

            # Convertir les données de l'image en format PIL
            img = Image.fromarray(image_data.astype(np.uint8))

            # Enregistrer l'image avec les nouvelles couleurs au format PNG
            img.save("temp.png")

            # Save the image as a PNG file
            pathTempImage = "../temp-image/"
            timestamp = str(int(time.time()))
            fileName = timestamp + "-" + str(randomNumber) + ".jpg"
            file_path_temp = os.path.join(pathTempImage, fileName)
            im = Image.open("temp.png")
            
            rgb_im = im.convert('RGB')
            rgb_im.save(file_path_temp)

            os.unlink("temp.png")
            classes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            
            test_image = preprocess_image(file_path_temp)
            # charger le modèle entraîné
            model = load_model("../model/model.h5")

            # charger les poids entraînés
            model.load_weights("../model/model_weights.h5")
            prediction = model.predict(test_image, verbose = False)
            print(prediction)
            # Recupere les 3 plus grandes valeurs avec leurs pourcentages
            top3 = np.argsort(prediction[0])[:-4:-1]        

            print(randomNumber, int(np.argmax(prediction)))
            if randomNumber == int(np.argmax(prediction)): 
                # copy temp file to retrain directory
                file_path_retrain = os.path.join("../retrain-image/", str(randomNumber))
                # Création du dossier au besoin
                if not os.path.exists(file_path_retrain):
                    os.makedirs(file_path_retrain)
                shutil.copyfile(file_path_temp, file_path_retrain + "/" + fileName)
                # TODO: Entrainer sur les images de retrain-image/ puis re save les poids
                st.success("The result given by the AI is "+ classes[np.argmax(prediction)] + " at " + str(round(prediction[0][top3[0]] * 100, 2)) + "%" + " !")
                # Lire le fichier GIF en tant que tableau d'octets
                with open("giphy.gif", "rb") as file:
                    gif_bytes = file.read()

                # Convertir le GIF en base64
                gif_base64 = base64.b64encode(gif_bytes).decode("utf-8")

                # Générer le code HTML pour afficher le GIF
                html_code = f'<img src="data:image/gif;base64,{gif_base64}" alt="gif" />'
                
                st.markdown(html_code, unsafe_allow_html=True)
            else:
                file_path_to_validate = os.path.join("../to-validate-image/", str(randomNumber))
                # Création du dossier au besoin
                if not os.path.exists(file_path_to_validate):
                    os.makedirs(file_path_to_validate)
                shutil.copyfile(file_path_temp, file_path_to_validate + "/" + fileName)
                
                st.error("The result given by the AI is "+ classes[np.argmax(prediction)] + " at " + str(round(prediction[0][top3[0]] * 100, 2)) + "%" + " !")
                random_int = random.choice([1, 2])

                # Lire le fichier GIF en tant que tableau d'octets
                with open("giphy"+str(random_int)+".gif", "rb") as file:
                    gif_bytes = file.read()

                # Convertir le GIF en base64
                gif_base64 = base64.b64encode(gif_bytes).decode("utf-8")

                # Générer le code HTML pour afficher le GIF
                html_code = f'<img src="data:image/gif;base64,{gif_base64}" alt="gif" />'
                
                st.markdown(html_code, unsafe_allow_html=True)
                bind_socket()
                
            # On delete le fichier dans temp dans tout les cas
            os.unlink(file_path_temp)
                
        else:
            st.warning("Please draw something on the canvas before saving.")