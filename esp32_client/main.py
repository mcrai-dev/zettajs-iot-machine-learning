from machine import Pin
from dht import DHT22
from classification import classify_temperature, classify_humidity
import time
import urequests
import network

# Configuration du capteur DHT22 et de la LED
sensor = DHT22(Pin(4))
led = Pin(13, Pin.OUT)

# Configuration Wi-Fi
SSID = 'mcrai_linux_lab'
PASSWORD = ''

# Adresse IP et port du serveur Zetta.js
SERVER_IP = '10.42.0.1'
SERVER_PORT = 3000
SERVER_URL = f'http://{SERVER_IP}:{SERVER_PORT}'



def get_local_time():
    local_time = time.localtime()  # Obtenir l'heure locale
    return "{:04}-{:02}-{:02} {:02}:{:02}:{:02}".format(
        local_time[0], local_time[1], local_time[2],
        local_time[3], local_time[4], local_time[5]
    )

def check_connection():
    try:
        # Tester la connexion en envoyant une requête GET
        response = urequests.get(SERVER_URL)
        response.close()
        return True
    except:
        return False

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    
    # Attendre la connexion
    while not wlan.isconnected():
        print('Connexion en cours...')
        time.sleep(1)
    
    print('Connecté à', SSID)
    print('Adresse IP:', wlan.ifconfig()[0])

# Connecter au Wi-Fi
connect_wifi()

while True:
    try:
        # Vérifier la connexion au serveur
        connected = check_connection()

        if connected:
            # Clignotement de la LED pour connexion stable
            led.on()
            time.sleep(0.25)
            led.off()
            time.sleep(0.75)
        else:
            # Clignotement de la LED pour connexion instable
            led.on()
            time.sleep(0.5)
            led.off()
            time.sleep(0.5)
        
        # Timestamp actuel
        timestamp = time.time()
        
        # Afficher l'heure UTC pour vérifier
        utc_time = time.gmtime(timestamp)
        formatted_utc_time = "{:04}-{:02}-{:02} {:02}:{:02}:{:02}".format(
            utc_time[0], utc_time[1], utc_time[2],
            utc_time[3], utc_time[4], utc_time[5]
        )
        print(f'UTC Time: {formatted_utc_time}')
        
        # Convertir le timestamp en heure locale à Madagascar (UTC+3)
        local_time = time.localtime(timestamp + 3*3600)
        formatted_time = "{:04}-{:02}-{:02} {:02}:{:02}:{:02}".format(
            local_time[0], local_time[1], local_time[2],
            local_time[3], local_time[4], local_time[5]
        )
        
        # Mesure de la température et de l'humidité
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()

        # Classification des données
        temp_class = classification.classify_temperature(temp)
        hum_class = classification.classify_humidity(hum)
        
        print(f'Timestamp: {formatted_time}, Temperature: {temp}°C, Temp_class: {temp_class}, Humidity: {hum}% , Hum_class: {hum_class}')

        # Envoi des données au serveur si connecté
        if connected:
            url = f'http://{SERVER_IP}:{SERVER_PORT}/data'
            data = {
                'timestamp': timestamp,
                'formatted_time': formatted_time,
                'temperature': temp,
                'temperature_class': temp_class,
                'humidity': hum,
                'humidity_class': hum_class
            }
            response = urequests.post(url, json=data)
            response.close()
            
    except OSError as e:
        print('Erreur de lecture du capteur:', e)
    except Exception as e:
        print('Erreur lors de l\'envoi des données:', e)
    time.sleep(2)
