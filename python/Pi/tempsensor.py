import os
import time
from datetime import datetime

import requests
from Helpers.pi_requests_class import PiRequests



# Adresse des DS18B20-Sensors im Dateisystem
sensor_file = '/sys/bus/w1/devices/28-00000cb47b8d/w1_slave'

# REST-API-Endpunkt
api_endpoint = 'DEINE_API_ENDPOINT_URL_HIER_EINFÜGEN'

# Pfad zur TXT-Datei für die Temperatur
txt_file_path = 'temperatur.txt'

# Userdata
user_name = 'DEIN_USERNAME_HIER_EINFÜGEN'
user_password = 'DEIN_PASSWORD_HIER_EINFÜGEN'

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

def send_to_api(temperature):
    temp_c = temperature
    temp_f = float(temperature) * 9.0 / 5.0 + 32.0
    try:
        # Daten an das REST-API senden
        user_data = PiRequests(f'http://${api_endpoint}:8000/api/v1/users', {'username': user_name, 'password': user_password}, 'get_users')
        if user_data == 'User not found':
            PiRequests(f'http://${api_endpoint}:8000/api/v1/users', {'name': user_name, 'password': user_password, 'token': 'admin'}, 'insert_user')
            user_data = PiRequests(f'http://${api_endpoint}:8000/api/v1/users', {'username': user_name, 'password': user_password}, 'get_users')
        timestamp = datetime.now().strftime("%Y-%m-%dT%HH:%M:%S")
        response = PiRequests(f'http://${api_endpoint}:8000/api/v1/temps', {'time': timestamp, 'temp_c': temp_c, 'temp_f': temp_f, 'HID': user_data}, 'insert_temp')
        print(f"Erfolgreich an API gesendet. Antwort: {response}")

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

# Hauptprogrammschleife
while True:
    temperature = read_temperature()

    if temperature is not None:
        send_to_api(temperature)
        update_txt_file(temperature)

    # Wartezeit zwischen den Messungen
    time.sleep(1)

