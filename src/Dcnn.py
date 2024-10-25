import tensorflow as tf, keras

model = keras.layers.TFSMLayer('src/modelo', call_endpoint='serving_default')

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def identificaNumero(image_path):

  image = Image.open(image_path)

  # Redimensionar a imagem para 28x28 pixels
  image = image.resize((28, 28))
  
  # Converter a imagem para um array NumPy
  image_array = np.array(image)

  # Verifique se a imagem está em escala de cinza; se não, converta
  if len(image_array.shape) == 3:  # Se a imagem tem 3 canais (RGB)
      image_array = np.mean(image_array, axis=2)  # Converte para escala de cinza

  # Normalizar os valores da imagem (de 0 a 255 para 0 a 1)
  image_array = image_array / 255.0

  for i_linha in range(len(image_array)):
    for i_item in range(len(image_array[i_linha])):
      if image_array[i_linha][i_item] <= 0.3:
        image_array[i_linha][i_item] = 0
      else:
        image_array[i_linha][i_item] = 1

  # Expandir as dimensões para se tornar (1, 28, 28, 1) - batch size de 1
  image_array = np.expand_dims(image_array, axis=-1)  # Adiciona canal
  image_array = np.expand_dims(image_array, axis=0)   # Adiciona batch dimension

  # Obter a classe prevista
  prediction = model(image_array)
  predicted_class = np.argmax(prediction["output_1"].numpy(), axis=1)

  return predicted_class[0]