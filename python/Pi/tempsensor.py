import requests
import json

from datetime import datetime
from Helpers.pi_requests_class import PiRequests
from Helpers.functions import get_sensor, get_user, get_endpoint, get_json_file

sensor_file = get_sensor()

# Userdata

user_name, user_password = get_user()

# REST-API-Endpunkt
api_endpoint = get_endpoint()

pi_request = PiRequests(api_endpoint, user_name, user_password, 'admin')

# Dateipfad für die Temperaturdaten
json_path = 'temperatures.json'
temps = get_json_file(json_path, pi_request.get_auth())


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
            print("Temperatur ist: " + formatted_temperature)
            return formatted_temperature

    except Exception as e:
        print(f"Fehler beim Lesen der Temperatur: {e}")
        return None


def send_to_api(temp_reading):
    temp_c = temp_reading
    temp_f = (float(temp_reading) * 9.0 / 5.0 + 32.0)
    try:
        # Daten an die REST-API senden
        temp_params = {
            'time': datetime.now().timestamp(),
            'temp_c': temp_c,
            'temp_f': temp_f,
        }
        pi_request.make_request(temp_params, 'create_temp')
        response = pi_request.get_response()
        if 'message' in response:
            if 'inserted' in response['message']:
                temps.append(temp_params)
                update_json_file(json_path)
                print(f"Erfolgreich an API gesendet. Antwort: {response['message']}")
                return
            else:
                print(f"Fehler beim Senden an API: {response['message']}")
                return

    except requests.exceptions.RequestException as api_err:
        print(f"Fehler beim Senden an API: {api_err}")


def update_json_file(path):
    with open(path, 'a+') as file:
        file.seek(0)
        json_data = json.load(file)
        auth = pi_request.get_auth()
        for user in json_data['users']:
            if auth in user:
                user[auth]['temps'] = temps
        file.truncate(0)
        json.dump(json_data, file)


last_call = datetime.now().timestamp()
# Hauptprogrammschleife
while True:
    current_time = datetime.now().timestamp()
    # Wartezeit zwischen den Messungen
    if current_time - last_call < 1:
        continue
    try:
        temperature = read_temperature()
        if temperature is not None:
            send_to_api(temperature)
            last_call = current_time
    except Exception as e:
        print(f"Fehler beim Auslesen der Temperatur: {e}")
        break
