import streamlit as st
from streamlit_drawable_canvas import st_canvas
import numpy as np
from PIL import Image
import os
from keras.models import load_model
from keras.utils import load_img, img_to_array
import random
import time
import shutil
import base64

# Page layout
st.set_page_config(page_title="Google Killer", page_icon="📝", layout="wide")
@st.cache_data 
def bind_socket():
    randomNumber = random.randint(0, 9)
    print("Random number: ", randomNumber) 
    return randomNumber

randomNumber=bind_socket()

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

# Navigation bar
menu = ["Home", "About"]
choice = st.sidebar.selectbox("Menu", menu)

# App title
st.title("Captcha")

# Center the canvas
col1, col2 = st.columns(2)
with col1:
    st.write("Nous voudrions un " + str(randomNumber) + " !")
with col2:
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # Initial fill color
        stroke_width=stroke_width,  # Stroke width
        stroke_color="white",  # Stroke color
        background_color="black",  # Background color
        width=canvas_width,
        height=canvas_height,
        drawing_mode="freedraw",  # Drawing mode (freehand drawing)
        key="canvas",
    )

# Save the drawn image upon button click
if st.button("Save"):
    if canvas_result.image_data is not None:
        # Convert canvas data to PIL image
        img_array = canvas_result.image_data.astype(np.uint8)
        img = Image.fromarray(img_array)
        img.save("temp.png")

        # Save the image as a PNG file
        pathTempImage = "temp-image/"
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
        resultat = "false"
        print(randomNumber, int(np.argmax(prediction)))
        if randomNumber == int(np.argmax(prediction)): 
            resultat = "true"
            # copy temp file to retrain directory
            file_path_re_train = "retrain-image/"
            file_path_retrain = os.path.join(file_path_re_train, fileName)
            shutil.copyfile(file_path_temp, file_path_retrain)
            # TODO: Entrainer sur les images de retrain-image/ puis re save les poids
            st.success("The result given by the AI is "+ classes[np.argmax(prediction)] + " so it's " + resultat + " !")
            # Lire le fichier GIF en tant que tableau d'octets
            with open("giphy.gif", "rb") as file:
                gif_bytes = file.read()

            # Convertir le GIF en base64
            gif_base64 = base64.b64encode(gif_bytes).decode("utf-8")

            # Générer le code HTML pour afficher le GIF
            html_code = f'<img src="data:image/gif;base64,{gif_base64}" alt="gif" />'
            
            st.markdown(html_code, unsafe_allow_html=True)
        else:
            st.error("The result given by the AI is "+ classes[np.argmax(prediction)] + " so it's " + resultat + " !")
            random_int = random.choice([1, 2])
            # Lire le fichier GIF en tant que tableau d'octets
            with open("giphy"+str(random_int)+".gif", "rb") as file:
                gif_bytes = file.read()

            # Convertir le GIF en base64
            gif_base64 = base64.b64encode(gif_bytes).decode("utf-8")

            # Générer le code HTML pour afficher le GIF
            html_code = f'<img src="data:image/gif;base64,{gif_base64}" alt="gif" />'
            
            st.markdown(html_code, unsafe_allow_html=True)
            
        # On delete le fichier dans temp dans tout les cas
        os.unlink(file_path_temp)
            
    else:
        st.warning("Please draw something on the canvas before saving.")