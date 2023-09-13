from all_data import create_df
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras

# Variables
API_KEY = 'AIzaSyCarGpEfvHg-9zsYEMpbZ754o1OvsuBvok'
MAX_RESULTS = 10

df = create_df(API_KEY=API_KEY, MAX_RESULTS=MAX_RESULTS)
images = df["image_array"]
views = df["views"]

# CNN model
model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3,3), padding='same', activation=tf.nn.relu,
                           input_shape=(90,120,3)),
    tf.keras.layers.MaxPooling2D((2, 2), strides=2),
    tf.keras.layers.Conv2D(64, (3,3), padding='same', activation=tf.nn.relu),
    tf.keras.layers.MaxPooling2D((2, 2), strides=2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation=tf.nn.relu),
    tf.keras.layers.Dense(1, activation=tf.nn.softmax)
])

model.compile(optimizer='adam',
              loss="mse",
              metrics=["mae"])

history = model.fit(images, views, epochs=10, validation_split=0.1)