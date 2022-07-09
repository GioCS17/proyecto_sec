import tensorflow as tf
import numpy as np
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences


new_model = tf.keras.models.load_model('model_clean_v1.hdf5')
labels = ['CWE-119', 'CWE-120', 'CWE-469', 'CWE-476', 'CWE-other']
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)
#tokenizer= pickle.load('tokenizer.pickle')

def Pipeline( X_test ):

  list_tokenized_test = tokenizer.texts_to_sequences(X_test)
  X_test_pad = pad_sequences(list_tokenized_test,  maxlen=500, padding='post', dtype = float)

  return X_test_pad


def classify(code):
  x_test = np.array( [code , ] )
  x_test = Pipeline(x_test)

  prediction = new_model.predict(x_test)
  confidences = {labels[i]: float(prediction[i][0][1]) for i in range(5)}
  return confidences

