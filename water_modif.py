# External module imp
import RPi.GPIO as GPIO
import datetime
from smbus import SMBus
import time

# On définit une adresse de bus sur laquelle nous communiquerons les informations
bus = SMBus(1)

# On renseigne la liste des adresses hexadécimales pour les différentes entrées de notre puce ADC (Freenove - ADS7830)
ads7830_commands = (0x84, 0xc4, 0x94, 0xd4, 0xa4, 0xe4, 0xb4, 0xf4)
# Ici l'adresse héxadécimale de la puce, définit par le constructeur afin de pouvoir communiquer avec le protocol I2C
ads7830_address = 0x4b
# Ces deux valeurs sont les valeurs maximum et minimum brutes retournées par le capteur
maxWhenDry = 220
maxWhenWet = 100

# Mode de lecture des broches par numéro
GPIO.setmode(GPIO.BOARD)

# Récupérer la date/horaire du dernier arrosage
def get_last_watered():
    try:
        f = open("last_watered.txt", "r")
        return f.readline()
    except:
        return "N'as jamais été arrosée"

# Récupérer la valeur retournée par le capteur d'humidité
def read_ads7830(input):
    bus.write_byte(ads7830_address, ads7830_commands[input])
    return bus.read_byte(ads7830_address)    

# Retourner, en pourcentage, le taux d'humidité de la terre
def get_status(input = 0):
    value = read_ads7830(input)
    value = int((value - maxWhenDry) * (100 - 0) / (maxWhenWet - maxWhenDry) + 0)
    return value

# Fonction d'arrosage automatique
def auto_water(delay = 3, pump_pin = 40, water_sensor_input = 0):
    consecutive_water_count = 0
    print("Here we go! Press CTRL+C to exit")
    try:
        while 1 and consecutive_water_count < 10:
            time.sleep(delay)
            wet = (get_status(water_sensor_input) > 20)
            print(consecutive_water_count)
            if not wet:
                if consecutive_water_count < 5:
                    pump_on(pump_pin, 1)
                consecutive_water_count += 1
            else:
                consecutive_water_count = 0
    except KeyboardInterrupt: # Si lancé via le terminal, permets de quitter la fonction proprement après l'entrée Ctrl + C :
        GPIO.cleanup()

# Activer la pompe sur une durée déterminée
def pump_on(pump_pin = 40, delay = 1):
    f = open("last_watered.txt", "w")
    f.write("Dernier arrosage le {}".format(datetime.datetime.now().strftime("%x à %X")))
    f.close()
    GPIO.setup(pump_pin, GPIO.OUT)
    time.sleep(delay)
    GPIO.cleanup(pump_pin)
