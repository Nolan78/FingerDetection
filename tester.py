import os
from keras.models import load_model
from keras.utils import load_img, img_to_array
import numpy as np
from tqdm import tqdm
import shutil

# dimensions des images d'entrée
img_rows, img_cols = 28, 28
pathTest = 'test-image/'
pathTrain = 'train-image/'
logger = False

# charger le modèle entraîné
model = load_model("model/model.h5")

# charger les poids entraînés
model.load_weights("model/model_weights.h5")

# fonction pour prétraiter l'image
def preprocess_image(img_path):
    img = load_img(img_path, target_size=(img_rows, img_cols), color_mode = "grayscale")
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x /= 255.
    return x

# classes de sortie du modèle
classes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
nombreTotalDeTest = 0
nombreDeReussite = 0
nombreDeFailed = 0

for file in tqdm(os.listdir(pathTest)):
    test_image = preprocess_image(pathTest + file)
    prediction = model.predict(test_image, verbose = False)
    nombreTotalDeTest += 1
    
    # Create directory if not exist
    if not os.path.exists(pathTest + classes[np.argmax(prediction)] + '/'):
        os.makedirs(pathTest + classes[np.argmax(prediction)] + '/')
        
    # copy file to test folder
    shutil.copyfile(pathTest + file, pathTest + classes[np.argmax(prediction)] + '/' + file)
    
    if logger: print(pathTrain + classes[np.argmax(prediction)] + '/' + file)
    if os.path.isfile(pathTrain + classes[np.argmax(prediction)] + '/' + file):
        nombreDeReussite += 1
        if logger: print("TEST OK ✅")
    else:
        nombreDeFailed += 1
        if logger: print("TEST FAILED ⛔")

print("Nombre total de test:", nombreTotalDeTest)
print("Nombre de test réussie:", nombreDeReussite)
print("Nombre de test ratée ", nombreDeFailed)
print("Taux de réussite:", nombreDeReussite/nombreTotalDeTest * 100, '%')