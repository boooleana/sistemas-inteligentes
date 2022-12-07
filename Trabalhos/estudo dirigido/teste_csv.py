import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from tensorflow.keras import layers
import pandas as pd
import os


data_path = tf.keras.utils.get_file('dados.csv', 'file:///C:/Users/giuli/Dropbox/PC/Documents/22.2/sistemas%20inteligentes/Trabalhos/estudo%20dirigido/dados/dados.csv')

dataset = tf.data.experimental.make_csv_dataset(
    data_path, batch_size=61,column_names={"ENTRADA","SAIDA"},shuffle=True,header=False)

train_dataset = dataset.sample(frac=0.8,random_state=0)
test_dataset = dataset.drop(train_dataset.index)

iterator = dataset.as_numpy_array()
print(dict(next(iterator)))

