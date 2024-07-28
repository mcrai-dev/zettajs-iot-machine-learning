import pandas as pd
import matplotlib.pyplot as plt

# Charger les données CSV
df = pd.read_csv('datasets/dataset.csv')

# Convertir le timestamp en datetime
df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')

# Visualiser les données
plt.figure(figsize=(12, 8))

# Trace des températures
plt.plot(df['datetime'], df['temperature'], label='Temperature', color='r')

# Trace de l'humidité
plt.plot(df['datetime'], df['humidity'], label='Humidity', color='b')

plt.xlabel('Datetime')
plt.ylabel('Value')
plt.title('Temperature and Humidity timelime')
plt.legend()
plt.grid(True)

# Afficher le graphique
plt.show()
