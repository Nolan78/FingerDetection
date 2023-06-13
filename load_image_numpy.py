import os
import numpy as np
from keras.utils import load_img, img_to_array

path = "train-image/"
classes = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

img_rows = 28 
img_cols = 28

X = []
Y = []

for classe in classes:
    for file in os.listdir(path + classe + "/"):
        print("Image de la classe : " + classe + " fichier : " + file)
        img = load_img(path + classe + "/" + file, target_size=(img_rows, img_cols), color_mode = "grayscale")
        x = img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x /= 255.
        X.append(np.array(x))
        Y.append(classes.index(classe))
        
X = np.array(X)
Y = np.array(Y)  

if os.path.exists("model/X_numpy_array.npy"):
    os.remove("model/X_numpy_array.npy")
if os.path.exists("model/Y_numpy_array.npy"):
    os.remove("model/Y_numpy_array.npy")

np.save("model/X_numpy_array", X)
np.save("model/Y_numpy_array", Y)