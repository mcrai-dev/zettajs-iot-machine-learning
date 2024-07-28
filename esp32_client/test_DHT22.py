from machine import Pin
from dht import DHT22
import time

sensor = DHT22(Pin(4)) 

while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        print(f'Temperature: {temp}°C, Humidity: {hum}%')
    except OSError as e:
        print('Erreur de lecture du capteur:', e)
    time.sleep(2)

