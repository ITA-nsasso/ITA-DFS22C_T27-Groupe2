# External module imp
import RPi.GPIO as GPIO
import datetime
from smbus import SMBus
import time

init = False
bus = SMBus(1)
ads7830_commands = (0x84, 0xc4, 0x94, 0xd4, 0xa4, 0xe4, 0xb4, 0xf4)
maxHumidity = 220
maxWet = 100

GPIO.setmode(GPIO.BOARD) # Broadcom pin-numbering scheme

def get_last_watered():
    try:
        f = open("last_watered.txt", "r")
        return f.readline()
    except:
        return "NEVER!"

def read_ads7830(input):
    bus.write_byte(0x4b, ads7830_commands[input])
    return bus.read_byte(0x4b)    

def get_status(input = 0):
    value = read_ads7830(input)
    value = int((value - maxHumidity) * (100 - 0) / (maxWet - maxHumidity) + 0)
    print(str(value) + "%")
    return value
    
def auto_water(delay = 5, pump_pin = 40, water_sensor_input = 0):
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
    except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
        GPIO.cleanup() # cleanup all GPI

def pump_on(pump_pin = 40, delay = 1):
    f = open("last_watered.txt", "w")
    f.write("Dernier arrosage le {}".format(datetime.datetime.now().strftime("%x à %X")))
    f.close()
    GPIO.setup(pump_pin, GPIO.OUT)
    time.sleep(delay)
    GPIO.cleanup(pump_pin)
