import RPi.GPIO as GPIO
from time import sleep

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

def motor_vorwaerts():
    GPIO.output(input1_pin, GPIO.HIGH)
    GPIO.output(input2_pin, GPIO.LOW)

def motor_rueckwaerts():
    GPIO.output(input1_pin, GPIO.LOW)
    GPIO.output(input2_pin, GPIO.HIGH)

def motor_stop():
    GPIO.output(input1_pin, GPIO.LOW)
    GPIO.output(input2_pin, GPIO.LOW)

# Motor vorwärts für 2 Sekunden
motor_vorwaerts()
sleep(2)

# Motor stoppen für 1 Sekunde
motor_stop()
sleep(1)

# Motor rückwärts für 2 Sekunden
motor_rueckwaerts()
sleep(2)

# Motor stoppen
motor_stop()

# GPIO zurücksetzen
GPIO.cleanup()
