import tensorflow as tf
import numpy as np
import joblib

# 1. Chargement des modèles et des préprocesseurs
lr_temp = joblib.load('Training/model/model_temp.joblib')
lr_humid = joblib.load('Training/model/model_humid.joblib')
scaler = joblib.load('Training/model/scaler.joblib')

# 2. Conversion des modèles scikit-learn en modèles TensorFlow
def sklearn_to_tf(sklearn_model):
    # Extraire les coefficients et l'intercept
    coef = sklearn_model.coef_
    intercept = sklearn_model.intercept_

    # Créer un modèle TensorFlow équivalent
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(coef.shape[0], input_shape=(coef.shape[1],), use_bias=True)
    ])

    # Définir les poids
    model.layers[0].set_weights([coef.T, intercept])
    
    return model

tf_model_temp = sklearn_to_tf(lr_temp)
tf_model_humid = sklearn_to_tf(lr_humid)

# 3. Conversion en TensorFlow Lite
converter = tf.lite.TFLiteConverter.from_keras_model(tf_model_temp)
tflite_model_temp = converter.convert()

converter = tf.lite.TFLiteConverter.from_keras_model(tf_model_humid)
tflite_model_humid = converter.convert()

# 4. Sauvegarde des modèles TFLite
with open('deploiement_In_ESP32/model/model_temp.tflite', 'wb') as f:
    f.write(tflite_model_temp)

with open('deploiement_In_ESP32/model/model_humid.tflite', 'wb') as f:
    f.write(tflite_model_humid)

print("Modèles TensorFlow Lite sauvegardés avec succès.")

# 5. Génération du code C pour les modèles
def generate_model_h(tflite_model, filename):
    with open(filename, 'w') as f:
        f.write("const unsigned char model[] = {\n")
        f.write(",".join([hex(x) for x in tflite_model]))
        f.write("\n};\n")
        f.write(f"const unsigned int model_len = {len(tflite_model)};\n")

generate_model_h(tflite_model_temp, 'deploiement_In_ESP32/model/model_temp.h')
generate_model_h(tflite_model_humid, 'deploiement_In_ESP32/model/model_humid.h')

print("Fichiers d'en-tête C générés avec succès.")