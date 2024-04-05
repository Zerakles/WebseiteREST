import os
import re
import sys
import socket
import json

# Liest Daten aus einer JSON-Datei
def get_json_file(file_path, auth):
    temps = []
    with open(file_path, 'a+') as file:
        file.seek(0)
        try:
            json_data = json.load(file)
            if 'users' in json_data:
                for user in json_data['users']:
                    if auth in user:
                        temps = user[auth]['temps']
                        break
            else:
                json_data = {
                    'users': [{f'{auth}': {'temps': []}}]
                }
                file.truncate(0)
                json.dump(json_data, file)
        except json.JSONDecodeError:
            json_data = {
                'users': [{f'{auth}': {'temps': []}}]
            }
            file.truncate(0)
            json.dump(json_data, file)
    return temps

# Liest die Temperatur aus dem Sensor aus
def get_sensor():
    # Adresse des DS18B20-Sensors im Dateisystem
    # regEx for the sensor file
    regex = "^28-\w+$"
    # get the sensor file
    sensor_file = None
    for root, dirs, files in os.walk('/sys/bus/w1/devices/'):
        for file in files:
            if re.match(regex, file):
                sensor_file = os.path.join(root, file, 'w1_slave')
                break
    if not sensor_file:
        print("Keine Sensor-Datei gefunden.")
        sys.exit(1)
    return sensor_file

# Überprüft, ob es Userdaten gibt und gibt sie zurück
def get_user():
    # Prüft, ob der Ordner 'cache' existiert und erstellt ihn, wenn er nicht existiert
    if not os.path.exists('cache/'):
        os.makedirs('cache/')
    save_data = check_for_save_data()
    user = None
    user_data = {
        'P1': {'username': 'PI1', 'password': 'PI1'},
        'P2': {'username': 'PI2', 'password': 'PI2'},
    }
    # Prüft, ob es einen gespeicherten Benutzer gibt und ob er in der Liste der Benutzerdaten enthalten ist
    if save_data:
        saved_user = save_data['user']
        if saved_user in user_data:
            while True:
                print(f'Soll der Benutzer {saved_user} verwendet werden? (j/n):')
                choice = input()
                if choice.lower() == 'j':
                    return user_data[saved_user]['username'], user_data[saved_user]['password']
                elif choice.lower() == 'n':
                    break
                else:
                    print('Bitte gib j oder n ein:')
    # Wählt den Benutzer aus der Liste der Benutzerdaten aus und speichert ihn in der Datei save_data.json
    while True:
        if user and user in user_data.keys():
            break
        print('Wähle dein Benutzer: P1 oder P2:')
        user = input()
    with open('cache/save_data.json', 'w') as file:
        data = {
            'user': user,
            'hostname': save_data['hostname']
        }
        json.dump(data, file)
    return user_data[user]['username'], user_data[user]['password']

# Prüft, ob die Datei save_data.json existiert und gibt den Inhalt zurück oder erstellt die Datei
def check_for_save_data():
    with open('cache/save_data.json', 'a+') as file:
        file.seek(0)
        try:
            save_data = json.load(file)
            return save_data
        except json.JSONDecodeError:
            save_data = {
                'user': '',
                'hostname': '0.0.0.0'
            }
            file.truncate(0)
            json.dump(save_data, file)
            return save_data


# Gibt die IP-Adresse des Servers zurück
def get_endpoint():
    save_data = check_for_save_data()
    hostname = socket.gethostname()
    # Prüft, ob der Hostname 'mmbbs' enthält und ersetzt ihn durch 'mmbbs.local'
    if 'mmbbs' in hostname:
        hostname = 'mmbbs.local'
    ip_address = socket.gethostbyname(hostname)
    first_octet = ip_address.split('.')[0]
    # Prüft, ob die IP-Adresse des Servers die Loopback-Adresse ist
    if first_octet == '127':
        ip_address = input('Bitte gib die Adresse des Servers ein:')
        with open('cache/save_data.json', 'w') as file:
            data = {
                'user': save_data['user'],
                'hostname': f'{ip_address}'
            }
            json.dump(data, file)
            return f'{ip_address}'
    # Gibt die ersten beiden Oktette der IP-Adresse zurück
    ip_address = '.'.join(ip_address.split('.')[:2])
    # Prüft, ob die IP-Adresse des Servers bereits in der Datei save_data.json gespeichert ist
    if save_data and save_data['hostname'] != '0.0.0.0':
        ip_check = '.'.join(str(save_data['hostname']).split('.')[:2])
        if ip_check == ip_address:
            print(f"Soll {save_data['hostname']} verwendet werden? (j/n):")
            while True:
                choice = input()
                if choice.lower() == 'j':
                    return str(save_data['hostname'])
                elif choice.lower() == 'n':
                    break
                else:
                    print('Bitte gib j oder n ein:')
    octave_1 = -1
    octave_2 = -1
    # Prüft, ob die Oktette der IP-Adresse gültig ist
    while int(octave_1) > 255 or int(octave_1) <= -1:
        octave_1 = input('Bitte gib die dritte Oktette des Servers ein:')
    while int(octave_2) > 255 or int(octave_2) <= -1:
        octave_2 = input('Bitte gib die Letzte Oktette des Servers ein:')
    # Speichert die IP-Adresse in der Datei save_data.json
    with open('cache/save_data.json', 'w') as file:
        data = {
            'user': save_data['user'],
            'hostname': f'{ip_address}.{octave_1}.{octave_2}'
        }
        json.dump(data, file)
    return f'{ip_address}.{octave_1}.{octave_2}'
