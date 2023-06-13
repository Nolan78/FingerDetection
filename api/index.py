import os
import numpy as np
import tensorflow as tf
from flask import Flask, request
from keras.utils import load_img, img_to_array
from werkzeug.utils import secure_filename
from keras.models import load_model

UPLOAD_FOLDER = './temp'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
img_rows = 28 
img_cols = 28

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
# fonction pour prétraitement l"image
def preprocess_image(img_path):
    img = load_img(img_path, target_size=(img_rows, img_cols), color_mode = "grayscale")
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x /= 255.
    return x

@app.route("/")
def hello_world():
    return "Hello World !"

@app.route('/test-image', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    if not request.files['file'].filename.endswith(".jpg"):
        return "File is not a jpg image"
    
    file = request.files['file']
    filename = secure_filename(file.filename)
    temp_image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(temp_image_path)
    
    # charger le modèle entraîné
    model = load_model("../model/model.h5")
    # charger les poids de l'entrainement
    model.load_weights("../model/model_weights.h5")

    # Liste des classes
    class_names = [
        '0','1','2',
        '3','4','5',
        '6','7','8',
        '9'
    ]
        
    predictions = model.predict(preprocess_image(temp_image_path))
    
    os.remove(temp_image_path)
    
    scores = tf.nn.softmax(predictions[0])
    scores = scores.numpy()
    image_class = class_names[np.argmax(predictions)]
    
    # renvoyer les différents taux de prédiction en json
    retun_json = {
        "predictions" : {
            "0" : str(scores[0]),
            "1" : str(scores[1]),
            "2" : str(scores[2]),
            "3" : str(scores[3]),
            "4" : str(scores[4]),
            "5" : str(scores[5]),
            "6" : str(scores[6]),
            "7" : str(scores[7]),
            "8" : str(scores[8]),  
            "9" : str(scores[9])
        },
        "image_class" : image_class
    }
    
    return retun_json
        