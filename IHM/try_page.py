import streamlit as st
import time
from PIL import Image
import os
from streamlit_drawable_canvas import st_canvas
import numpy as np
from keras.models import load_model
from keras.utils import load_img, img_to_array

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
    st.write("Try page")
        
    # Center the canvas
    col1, col2 = st.columns(2)
    with col1:
        st.write("Essayez notre super captcha !")
    with col2:
        canvas_result_try = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",  # Initial fill color
            stroke_width=stroke_width,  # Stroke width
            stroke_color="white",  # Stroke color
            background_color="black",  # Background color
            width=canvas_width,
            height=canvas_height,
            drawing_mode="freedraw",  # Drawing mode (freehand drawing)
            key="canvas_try"
        )

    # Save the drawn image upon button click
    if st.button("Save"):
        if canvas_result_try.image_data is not None:
            # Convert canvas data to PIL image
            img_array = canvas_result_try.image_data.astype(np.uint8)
            img = Image.fromarray(img_array)
            img.save("temp.png")

            # Save the image as a PNG file
            pathTempImage = "../temp-image/"
            timestamp = str(int(time.time()))
            fileName = timestamp +  ".jpg"
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
            # Affiche les 3 plus grandes valeurs avec leurs pourcentages sans for
            print("Prediction: ", classes[top3[0]], "(", round(prediction[0][top3[0]] * 100, 2), "%)")
     
            for i in range(3):
                print("{}".format(classes[top3[i]])+" ({:.3})".format(prediction[0][top3[i]]))
                label = "{}".format(classes[top3[i]])+ " (" + str(round(prediction[0][top3[i]] * 100, 2)) + "%)"
                progress_bar = st.progress(round(prediction[0][top3[i]] * 100))
                progress_bar.progress(round(prediction[0][top3[i]] * 100))
                st.write(label)
                
            # On delete le fichier dans temp dans tout les cas
            os.unlink(file_path_temp)
                
        else:
            st.warning("Please draw something on the canvas before saving.")