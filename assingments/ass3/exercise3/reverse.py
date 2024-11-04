import tensorflow as tf

# Load the .keras model
model = tf.keras.models.load_model('my_model.keras')
converter = tf.lite.TFLiteConverter.from_keras_model(model) 
tflite_model = converter.convert()
with open('converted_model.tflite', 'wb') as f:     
  f.write(tflite_model)