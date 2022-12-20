from keras.datasets import mnist
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from keras.models import Sequential,load_model
from keras.layers import Dense,Dropout,Flatten,Conv2D,MaxPool2D
from keras import optimizers
from sklearn.preprocessing import MinMaxScaler
from keras.utils import to_categorical
import cv2
from keras.preprocessing import image

model = load_model('./model.h5')

FRUITS = {
    0:'Apple',
    1:'Banana',
    2:'Mongo',
    3:'Orange',
    4:'Pineapple'
}

test_img = f'E:/Python/HQYJ/Fruit8/datasets/fruit4test/3.png'
img = image.load_img(test_img, target_size = (128,128))
img_array = image.img_to_array(img)
img_array = np.array(img_array)/255.0

predictions = model.predict(img_array[np.newaxis, ...])
a = np.argmax(predictions, axis=-1)
id = a.tolist()[0]
print('result:',FRUITS[id])


