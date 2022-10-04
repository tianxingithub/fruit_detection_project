import os
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Dropout
from keras.losses import sparse_categorical_crossentropy
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator

main_dir = r"E:\Python\HQYJ\Fruit8\datasets\Fruit-Classifier-main\Data"
test_dir = main_dir + '/test'
train_dir = main_dir + '/train'

# Creating a data generator
train = ImageDataGenerator(
  rescale=1./255,
    horizontal_flip = True,
    vertical_flip = True,
    validation_split = 0.2
)
train_datagen = train.flow_from_directory(
        train_dir,
        batch_size=32,
        target_size=(128,128),
        class_mode='sparse',
        subset = 'training')

val_datagen = train.flow_from_directory(
        train_dir,
        batch_size=32,
        target_size=(128,128),
        class_mode='sparse',
        subset = 'validation')

# Printing the training set
train_labels = (train_datagen.class_indices)

# Create a data generator
test_datagen = ImageDataGenerator(
  rescale=1./255,
    horizontal_flip = True,
    vertical_flip = True
)
test_datagen = test_datagen.flow_from_directory(
        test_dir,
        batch_size=32,
        target_size=(128,128),
        class_mode='sparse')

# Printing the test set
test_labels = (test_datagen.class_indices)


def built_model():
    model = Sequential()
    # Convolution blocks
    model.add(Conv2D(32, kernel_size=(3, 3),
                     padding='same',
                     input_shape=(128, 128, 3),
                     activation='relu'))
    model.add(MaxPooling2D(pool_size=2))
    model.add(Conv2D(64, kernel_size=(3, 3),
                     padding='same',
                     activation='relu'))
    model.add(MaxPooling2D(pool_size=2))
    model.add(Conv2D(32, kernel_size=(3, 3),
                     padding='same',
                     activation='relu'))
    model.add(MaxPooling2D(pool_size=2))
    # Classification layers
    model.add(Flatten())
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(32, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(5, activation='softmax'))
    return model

model = built_model()
model.compile(optimizer = 'Adam',
              loss = 'sparse_categorical_crossentropy',
              metrics = ['accuracy'])

trained_model = model.fit(train_datagen, epochs=50,
                          batch_size = 32,
                          validation_data = val_datagen, verbose = 1)


# model_dir = r'E:\Python\HQYJ\Fruit8\ModelFruit5.h5'
# model.save(model_dir)
