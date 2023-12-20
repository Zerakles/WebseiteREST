import json
import time

import RPi.GPIO as GPIO

from Helpers.pi_requests_class import PiRequests


# GPIO-Pins
enable_pin = 5
input1_pin = 6
input2_pin = 25

# GPIO-Modus festlegen
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


# GPIO-Pins als Ausg
GPIO.setup(enable_pin, GPIO.OUT)
GPIO.setup(input1_pin, GPIO.OUT)
GPIO.setup(input2_pin, GPIO.OUT)

# Motor aktivieren
GPIO.output(enable_pin, GPIO.HIGH)

# Userdata
user_name = input('Bitte gib deinen Benutzernamen ein: ')
user_password = input('Bitte gib dein Passwort ein: ')

# REST-API-Endpunkt
api_endpoint = input('Bitte gib die IP-Adresse des Servers ein: ')
pi_request = PiRequests(api_endpoint, user_name, user_password, 'admin')


def motor_vorwaerts():
    GPIO.output(input1_pin, GPIO.HIGH)
    GPIO.output(input2_pin, GPIO.LOW)

def motor_rueckwaerts():
    GPIO.output(input1_pin, GPIO.LOW)
    GPIO.output(input2_pin, GPIO.HIGH)

def motor_stop():
    GPIO.output(input1_pin, GPIO.LOW)
    GPIO.output(input2_pin, GPIO.LOW)


def get_temps():
    pi_request.make_request({'limit': 5,'offset': None}, 'get_temps')
    response = pi_request.get_response()
    return json.loads(response)


def process_temps(temps):
    average_temp = None
    if temps is None:
        motor_stop()
    else:
        average_temp = 0
        try:
            for temp in temps:
                average_temp += temp['temp_c']
            average_temp = average_temp / len(temps)
        except Exception as e:
            print(f"Fehler beim Berechnen der Durchschnittstemperatur: {e}")
            average_temp = None
    if average_temp is None:
        motor_stop()
    elif average_temp >= 28:
        motor_vorwaerts()
    elif average_temp < 28:
        motor_stop()
    print(f"Durchschnittstemperatur: {average_temp}")

while True:
    # Temperatur auslesen
    temps = get_temps()
    print(temps)
    process_temps(temps)
    # Wartezeit zwischen den Messungen
    time.sleep(1)


# GPIO zurücksetzen
GPIO.cleanup()