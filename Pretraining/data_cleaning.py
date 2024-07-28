import pandas as pd
import numpy as np

# Charger les données du CSV
df = pd.read_csv('data.csv')

# Fonctions de classification pour la température et l'humidité
def classify_temperature(temp):
    if temp < 18:
        return 'froid'
    elif 18 <= temp <= 25:
        return 'ambiante'
    else:
        return 'chaud'

def classify_humidity(hum):
    if hum < 30:
        return 'sec'
    elif 30 <= hum <= 80:
        return 'confortable'
    else:
        return 'humide'

# Modifier environ 20 lignes pour inclure les cas non représentés
num_modifications = 20
indices_to_modify = np.random.choice(df.index, num_modifications, replace=False)

for index in indices_to_modify:
    # Modifier aléatoirement température et humidité pour générer d'autres classes
    if np.random.rand() < 0.5:
        new_temp = np.random.uniform(15, 30)  # Températures variées pour générer différents cas
        df.at[index, 'temperature'] = new_temp
        df.at[index, 'temperature_class'] = classify_temperature(new_temp)
    if np.random.rand() < 0.5:
        new_humidity = np.random.uniform(22, 99)  # Humidités variées pour générer différents cas
        df.at[index, 'humidity'] = new_humidity
        df.at[index, 'humidity_class'] = classify_humidity(new_humidity)

# Sauvegarder le CSV modifié
df.to_csv('datasets/dataset.csv', index=False)
