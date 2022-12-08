import pathlib

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers

print(tf.__version__)

dataset_path = tf.keras.utils.get_file('dados.csv', 'file:///C:/Users/giuli/Documents/UFSC/2022.2/sistemas-inteligentes/Trabalhos/estudo%20dirigido/dados/dados.csv')
dataset_path

column_names = ['Entrada','Saida']
#'MPG','Cylinders','Displacement','Horsepower','Weight', 'Acceleration', 'Model Year', 'Origin'
raw_dataset = pd.read_csv(dataset_path, names=column_names)

dataset = raw_dataset.copy()
print("Tail: ", dataset.tail())

dataset.isna().sum()
#exclui itens vazios
dataset = dataset.dropna()



#seleciona 80% do dataset pra amostra e coloca o resto para teste
train_dataset = dataset.sample(frac=0.8,random_state=0) 
test_dataset = dataset.drop(train_dataset.index)
sns.pairplot(train_dataset[["Entrada", "Saida"]], diag_kind="kde")

#plota graficos iniciais
dataset.plot(kind='scatter',x='Entrada',y='Saida',color='red').set_title('DATASET PONTOS')
train_dataset.plot(kind='scatter',x='Entrada',y='Saida',color='red').set_title('TRAIN DATASET PONTOS')
plt.show()


train_stats = train_dataset.describe()
train_stats.pop("Saida")
train_stats = train_stats.transpose()

train_labels = train_dataset.pop('Saida')
test_labels = test_dataset.pop('Saida')

def norm(x):
  return (x - train_stats['mean']) / train_stats['std']
normed_train_data = norm(train_dataset)
normed_test_data = norm(test_dataset)

def build_model():
  model = keras.Sequential([
    layers.Dense(100, activation='relu', input_shape=[len(train_dataset.keys())]),
    layers.Dense(100, activation='relu'),
    layers.Dense(100, activation='relu'),
    layers.Dense(100, activation='relu'),
    layers.Dense(100, activation='relu'),
    layers.Dense(1, activation='linear')
  ])


  optimizer = tf.keras.optimizers.RMSprop(0.001)

  model.compile(loss='mse',
                optimizer=optimizer,
                metrics=['mae', 'mse'])
  return model

model = build_model()

model.summary()

example_batch = normed_train_data[:10]
example_result = model.predict(example_batch)
print("Example result: \n", example_result)

# Mostra o progresso do treinamento imprimindo um único ponto para cada epoch completada
class PrintDot(keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs):
    if epoch % 100 == 0: print('')
    print('.', end='')

EPOCHS = 1000

history = model.fit(
  normed_train_data, train_labels,
  epochs=EPOCHS, validation_split = 0.2, verbose=0,
  callbacks=[PrintDot()])

hist = pd.DataFrame(history.history)
hist['epoch'] = history.epoch
hist.tail()


def plot_history(history):
  hist = pd.DataFrame(history.history)
  hist['epoch'] = history.epoch

  plt.figure()
  plt.xlabel('Epoch')
  plt.ylabel('Mean Abs Error ')
  plt.plot(hist['epoch'], hist['mae'],label='Train Error')
  plt.plot(hist['epoch'], hist['val_mae'],label = 'Val Error')
  plt.xlim([0,5])
  plt.legend()

  plt.figure()
  plt.xlabel('Epoch')
  plt.ylabel('Mean Square Error ')
  plt.plot(hist['epoch'], hist['mse'],label='Train Error')
  plt.plot(hist['epoch'], hist['val_mse'],label = 'Val Error')
  plt.xlim([0,20])
  plt.legend()
  plt.show()


plot_history(history)

model = build_model()

# O parâmetro patience é o quantidade de epochs para checar as melhoras
early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=20)

history = model.fit(normed_train_data, train_labels, epochs=EPOCHS,
                    validation_split = 0.2, verbose=0, callbacks=[early_stop, PrintDot()])

plot_history(history)

loss, mae, mse = model.evaluate(normed_test_data, test_labels, verbose=2)

print("Testing set Mean Abs Error: {:5.2f} Entrada".format(mae))

test_predictions = model.predict(normed_test_data).flatten()

print("\n\n\n Test Predictions:\n\n",test_predictions)

print("labels\n\n",test_labels)
print("normed\n\n",normed_test_data)
print("predictions\n\n",test_predictions)

plt.scatter(test_labels, test_predictions)
plt.xlabel('True Values')
plt.ylabel('Predictions')
plt.axis('equal')
plt.axis('square')
plt.xlim([0,plt.xlim()[1]])
plt.ylim([0,plt.ylim()[1]])
_ = plt.plot([-800, 800], [-800, 800])
plt.legend()
plt.show()

error = test_predictions - test_labels
plt.hist(error, bins = 25)
plt.xlabel("Prediction Error ")
_ = plt.ylabel("Count")
plt.legend()
plt.show()
"""

salvar rede: arquivo com a rede

  
"""