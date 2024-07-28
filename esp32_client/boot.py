# boot.py
import time
from machine import Pin
import os

# Attendez quelques secondes pour s'assurer que tout est initialisé
time.sleep(2)

# Clignotez la LED pour indiquer que le boot.py a démarré
led = Pin(13, Pin.OUT)
for _ in range(3):
    led.on()
    time.sleep(0.1)
    led.off()
    time.sleep(0.1)

# Afficher le contenu du répertoire
print("Contenu du répertoire :")
print(os.listdir())

# Essayez d'importer le module main
try:
    import main
    print("Module main importé avec succès")
except ImportError as e:
    print(f"Erreur lors de l'importation de main : {e}")
except Exception as e:
    print(f"Erreur inattendue : {e}")

print("Fin de boot.py")