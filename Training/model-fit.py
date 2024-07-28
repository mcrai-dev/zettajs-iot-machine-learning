"""
Script d'entrainement et d'évaluation des modèles de classification de la température et de l'humidité.

Ce script utilise scikit-learn pour entrainer et évaluer trois modèles différents :
- K-plus proches voisins (K-NN)
- Régression logistique multinomiale
- Arbre de décision

Auteur : M'Crai LAYDAM
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report

# Charger les données
df = pd.read_csv('datasets/dataset.csv')

# Préparation des données
X = df[['temperature', 'humidity']]  # Utiliser les caractéristiques de température et d'humidité
y = df['temperature_class']  # Utiliser temperature_class comme la classe cible

# Diviser les données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Normalisation des données
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# K-plus proches voisins (K-NN)
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)
y_pred_knn = knn.predict(X_test)
knn_score = accuracy_score(y_test, y_pred_knn)
print("K-NN Accuracy:", knn_score)
print("K-NN Classification Report:\n", classification_report(y_test, y_pred_knn))

# Régression logistique multinomiale
log_reg = LogisticRegression(multi_class='multinomial', solver='lbfgs', max_iter=200)
log_reg.fit(X_train, y_train)
y_pred_log_reg = log_reg.predict(X_test)
log_reg_score = accuracy_score(y_test, y_pred_log_reg)
print("Logistic Regression Accuracy:", log_reg_score)
print("Logistic Regression Classification Report:\n", classification_report(y_test, y_pred_log_reg))

# Arbre de décision
tree = DecisionTreeClassifier()
tree.fit(X_train, y_train)
y_pred_tree = tree.predict(X_test)
tree_score = accuracy_score(y_test, y_pred_tree)
print("Decision Tree Accuracy:", tree_score)
print("Decision Tree Classification Report:\n", classification_report(y_test, y_pred_tree))

