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
    elif 30 <= hum <= 60:
        return 'confortable'
    else:
        return 'humide'