import os
import time
import requests

# Adresse des DS18B20-Sensors im Dateisystem
sensor_file = '/sys/bus/w1/devices/28-00000cb47b8d/w1_slave'

# REST-API-Endpunkt
api_endpoint = 'DEINE_API_ENDPOINT_URL_HIER_EINFÜGEN'

# Pfad zur TXT-Datei für die Temperatur
txt_file_path = 'temperatur.txt'

def read_temperature():
    try:
        # DS18B20-Sensor auslesen
        with open(sensor_file, 'r') as file:
            lines = file.readlines()
            raw_temperature = lines[1].split('=')[1].strip()

            # Konvertiere die Roh-Temperatur in eine Dezimalzahl
            temperature_celsius = float(raw_temperature) / 1000.0

            # Formatieren auf zwei Dezimalstellen
            formatted_temperature = "{:.2f}".format(temperature_celsius)
            print("Temperatur ist: "+formatted_temperature)
            return formatted_temperature

    except Exception as e:
        print(f"Fehler beim Lesen der Temperatur: {e}")
        return None
"""
def send_to_api(temperature):
    try:
        # Daten an das REST-API senden
        payload = {'temperature': temperature}
        response = requests.post(api_endpoint, json=payload)
        response.raise_for_status()
        print(f"Erfolgreich an API gesendet. Antwort: {response.text}")

    except requests.exceptions.RequestException as api_err:
        print(f"Fehler beim Senden an API: {api_err}")

def update_txt_file(temperature):
    try:
        # Temperatur in die TXT-Datei schreiben
        with open(txt_file_path, 'w') as txt_file:
            txt_file.write(temperature)
        print(f"Temperatur in {txt_file_path} aktualisiert.")

    except Exception as txt_err:
        print(f"Fehler beim Aktualisieren der TXT-Datei: {txt_err}")
"""
# Hauptprogrammschleife
while True:
    temperature = read_temperature()
"""""
    if temperature is not None:
        send_to_api(temperature)
        update_txt_file(temperature)

    # Wartezeit zwischen den Messungen
    time.sleep(1)
"""
