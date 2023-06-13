import os
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Flatten, BatchNormalization
from keras.utils import to_categorical, load_img, img_to_array
import keras.backend as K
from sklearn.model_selection import train_test_split

path = "train-image/"
classes = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

img_rows = 28 
img_cols = 28

X = []
Y = []

for classe in classes:
    for file in os.listdir(path + classe + "/"):
        # print(path + classe + "/" + file)
        img = load_img(path + classe + "/" + file, target_size=(img_rows, img_cols), color_mode = "grayscale")
        x = img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x /= 255.
        X.append(np.array(x))
        Y.append(classes.index(classe))
        
X = np.array(X)
Y = np.array(Y)  

#Now defining some parameters for our model
num_classes = 10
epochs = 30

x_train,x_test,y_train,y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

y_train = to_categorical(y_train, num_classes = 10, dtype = "float32")
y_test = to_categorical(y_test, num_classes = 10, dtype = "float32")

if K.image_data_format() =="channels_first":
    x_train = x_train.reshape(x_train.shape[0],1,img_rows,img_cols)
    x_test = x_test.reshape(x_test.shape[0],1,img_rows,img_cols)
    input_shape = (1,img_rows,img_cols)
else:
    x_train = x_train.reshape(x_train.shape[0],img_rows,img_cols,1)
    x_test = x_test.reshape(x_test.shape[0],img_rows,img_cols,1)
    input_shape = (img_rows,img_cols,1)
    
input_shape = (img_rows,img_cols,1)
    
model = Sequential()
model.add(Conv2D(32, kernel_size = 3, activation="relu", input_shape = input_shape))
model.add(MaxPooling2D())
model.add(Conv2D(32, kernel_size = 3, activation="relu"))
model.add(BatchNormalization())
model.add(Conv2D(32, kernel_size = 5, strides=2, padding="same", activation="relu"))
model.add(BatchNormalization())
model.add(Dropout(0.4))
model.add(Conv2D(64, kernel_size = 3, activation="relu"))
model.add(BatchNormalization())
model.add(Conv2D(64, kernel_size = 3, activation="relu"))
model.add(BatchNormalization())
model.add(Conv2D(64, kernel_size = 5, strides=2, padding="same", activation="relu"))
model.add(BatchNormalization())
model.add(Dropout(0.4))
model.add(Flatten())
model.add(Dropout(0.4))
model.add(Dense(10, activation="softmax"))

model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

nn = model.fit(x_train, y_train, batch_size=32, epochs=epochs, validation_data=(x_test,y_test))

plt.plot(nn.history["loss"])
plt.plot(nn.history["accuracy"])
plt.title("model loss")
plt.ylabel("loss and accuracy")
plt.xlabel("epoch")
plt.legend(["train_loss", "train_accuracy"], loc="upper right")
plt.savefig("stat/model_loss_accuracy.png")

score ,acc = model.evaluate(x_test,y_test)
print("Score is :",score)
print("Accuracy :",acc)

# export du modèle
model.save("model/model.h5")
model.save_weights("model/model_weights.h5")