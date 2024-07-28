import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report

# Charger les données
data = pd.read_csv('datasets/dataset.csv')  # Assurez-vous que le chemin du fichier est correct

# Prétraitement des données
X = data[['temperature', 'humidity']]
y_temp = data['temperature_class']
y_humid = data['humidity_class']

# Encodage des variables cibles
le_temp = LabelEncoder()
le_humid = LabelEncoder()
y_temp_encoded = le_temp.fit_transform(y_temp)
y_humid_encoded = le_humid.fit_transform(y_humid)

# Normalisation des caractéristiques
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Séparation des données en ensembles d'entraînement et de test
X_train, X_test, y_temp_train, y_temp_test, y_humid_train, y_humid_test = train_test_split(
    X_scaled, y_temp_encoded, y_humid_encoded, test_size=0.2, random_state=42)

# Fonction pour entraîner et évaluer un modèle
def train_and_evaluate(model, X_train, X_test, y_train, y_test, target_name):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nRésultats pour {target_name}:")
    print(f"Accuracy: {accuracy:.4f}")
    print("Rapport de classification:")
    print(classification_report(y_test, y_pred, target_names=le_temp.classes_ if target_name == 'Température' else le_humid.classes_))

# 1. K plus proches voisins (K-NN)
knn_temp = KNeighborsClassifier(n_neighbors=5)
knn_humid = KNeighborsClassifier(n_neighbors=5)

print("K plus proches voisins (K-NN)")
train_and_evaluate(knn_temp, X_train, X_test, y_temp_train, y_temp_test, 'Température')
train_and_evaluate(knn_humid, X_train, X_test, y_humid_train, y_humid_test, 'Humidité')

# 2. Régression logistique multinomiale
lr_temp = LogisticRegression(multi_class='multinomial', solver='lbfgs', max_iter=1000)
lr_humid = LogisticRegression(multi_class='multinomial', solver='lbfgs', max_iter=1000)

print("\nRégression logistique multinomiale")
train_and_evaluate(lr_temp, X_train, X_test, y_temp_train, y_temp_test, 'Température')
train_and_evaluate(lr_humid, X_train, X_test, y_humid_train, y_humid_test, 'Humidité')

# 3. Arbre de décision
dt_temp = DecisionTreeClassifier(random_state=42)
dt_humid = DecisionTreeClassifier(random_state=42)

print("\nArbre de décision")
train_and_evaluate(dt_temp, X_train, X_test, y_temp_train, y_temp_test, 'Température')
train_and_evaluate(dt_humid, X_train, X_test, y_humid_train, y_humid_test, 'Humidité')
