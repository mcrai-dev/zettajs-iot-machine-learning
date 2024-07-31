import machine
import dht
import utime
import json
import math
import urequests

def load_metadata():
    try:
        with open('model_metadata.json', 'r') as f:
            return json.load(f)
    except OSError as e:
        print("Erreur lors du chargement des métadonnées:", e)
        return None

def normalize(value, mean, scale):
    return (value - mean) / scale

def predict(temp, humid, coef, intercept):
    temp_norm = normalize(temp, metadata['scaler_mean'][0], metadata['scaler_scale'][0])
    humid_norm = normalize(humid, metadata['scaler_mean'][1], metadata['scaler_scale'][1])
    z = coef[0] * temp_norm + coef[1] * humid_norm + intercept
    return 1 / (1 + math.exp(-z))

def get_prediction():
    try:
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
        
        temp_pred = predict(temperature, humidity, temp_model['coef'], temp_model['intercept'])
        humid_pred = predict(temperature, humidity, humid_model['coef'], humid_model['intercept'])
        
        temp_class = metadata['temperature_classes'][int(temp_pred > 0.5)]
        humid_class = metadata['humidity_classes'][int(humid_pred > 0.5)]
        
        return temperature, humidity, temp_class, humid_class
    except Exception as e:
        print("Erreur lors de la prédiction:", e)
        return None, None, None, None

def predict_environment_state(temp, humid, temp_class, humid_class):
    if temp_class == "froid" and humid_class == "sec":
        return "Froid et sec - Risque de inconfort, envisagez d'augmenter la température et l'humidité"
    elif temp_class == "froid" and humid_class == "humide":
        return "Froid et humide - Risque de moisissures, augmentez la température et ventilez"
    elif temp_class == "chaud" and humid_class == "sec":
        return "Chaud et sec - Risque de déshydratation, augmentez l'humidité"
    elif temp_class == "chaud" and humid_class == "humide":
        return "Chaud et humide - Inconfortable, diminuez la température et déshumidifiez"
    elif temp_class == "ambiante" and humid_class == "confortable":
        return "Conditions idéales - Environnement confortable"
    else:
        return f"État intermédiaire - Température: {temp_class}, Humidité: {humid_class}"

def send_data_to_server(temp, humid, temp_class, humid_class):
    url = "http://10.42.0.1:5000/data"
    headers = {'Content-Type': 'application/json'}
    data = {
        'temperature': temp,
        'humidity': humid,
        'temp_class': temp_class,
        'humid_class': humid_class
    }
    try:
        response = urequests.post(url, headers=headers, data=json.dumps(data))
        print(f"Réponse du serveur: {response.text}")
        response.close()
    except Exception as e:
        print(f"Erreur lors de l'envoi des données: {e}")

# Initialisation
print("Démarrage du programme...")

metadata = load_metadata()
if metadata is None:
    print("Impossible de continuer sans métadonnées.")
    machine.reset()


temp_model = {
    'coef': [1.5, -0.5],
    'intercept': 0.1
}
humid_model = {
    'coef': [-0.8, 1.2],
    'intercept': -0.2
}

try:
    dht_sensor = dht.DHT22(machine.Pin(4))
except Exception as e:
    print("Erreur lors de l'initialisation du capteur DHT22:", e)
    machine.reset()

print("Initialisation terminée. Démarrage de la boucle principale...")

# Boucle principale
while True:
    try:
        temp, humid, temp_class, humid_class = get_prediction()
        if temp is not None:
            env_state = predict_environment_state(temp, humid, temp_class, humid_class)
            print(f"Température: {temp}°C, Classe: {temp_class}")
            print(f"Humidité: {humid}%, Classe: {humid_class}")
            print(f"État de l'environnement: {env_state}")
            print("--------------------")

            # Envoyer les données au serveur Flask
            send_data_to_server(temp, humid, temp_class, humid_class)
        else:
            print("Erreur de lecture du capteur")
    except Exception as e:
        print("Erreur dans la boucle principale:", e)
    
    utime.sleep(2)
