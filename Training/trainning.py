import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib

# 1. Chargement des données
data = pd.read_csv('datasets/dataset.csv')
X = data[['temperature', 'humidity']]
y_temp = data['temperature_class']
y_humid = data['humidity_class']

# 2. Prétraitement des données
# Encodage des labels
le_temp = LabelEncoder()
le_humid = LabelEncoder()
y_temp_encoded = le_temp.fit_transform(y_temp)
y_humid_encoded = le_humid.fit_transform(y_humid)

# Normalisation des caractéristiques
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 3. Séparation des données en ensembles d'entraînement et de test
X_train, X_test, y_temp_train, y_temp_test, y_humid_train, y_humid_test = train_test_split(
    X_scaled, y_temp_encoded, y_humid_encoded, test_size=0.2, random_state=42)

# 4. Entraînement des modèles
# Modèle pour la température
lr_temp = LogisticRegression(multi_class='ovr', solver='lbfgs', max_iter=1000)
lr_temp.fit(X_train, y_temp_train)

# Modèle pour l'humidité
lr_humid = LogisticRegression(multi_class='ovr', solver='lbfgs', max_iter=1000)
lr_humid.fit(X_train, y_humid_train)

# 5. Évaluation des modèles
# Température
y_temp_pred = lr_temp.predict(X_test)
print("Modèle de température:")
print(f"Accuracy: {accuracy_score(y_temp_test, y_temp_pred):.4f}")
print(classification_report(y_temp_test, y_temp_pred, target_names=le_temp.classes_))

# Humidité
y_humid_pred = lr_humid.predict(X_test)
print("\nModèle d'humidité:")
print(f"Accuracy: {accuracy_score(y_humid_test, y_humid_pred):.4f}")
print(classification_report(y_humid_test, y_humid_pred, target_names=le_humid.classes_))

# 6. Sauvegarde des modèles et des préprocesseurs
joblib.dump(lr_temp, 'Training/model/model_temp.joblib')
joblib.dump(lr_humid, 'Training/model/model_humid.joblib')
joblib.dump(scaler, 'Training/model/scaler.joblib')
joblib.dump(le_temp, 'Training/model/label_encoder_temp.joblib')
joblib.dump(le_humid, 'Training/model/label_encoder_humid.joblib')

print("Modèles et préprocesseurs sauvegardés avec succès.")

# 7. Sauvegarde des métadonnées
import json

metadata = {
    'features': ['temperature', 'humidity'],
    'temperature_classes': le_temp.classes_.tolist(),
    'humidity_classes': le_humid.classes_.tolist(),
    'scaler_mean': scaler.mean_.tolist(),
    'scaler_scale': scaler.scale_.tolist()
}

with open('Training/model/model_metadata.json', 'w') as f:
    json.dump(metadata, f)

print("Métadonnées sauvegardées avec succès.")
