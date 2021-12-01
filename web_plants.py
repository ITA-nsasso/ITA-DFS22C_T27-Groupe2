from flask import Flask, render_template, redirect, url_for
import psutil
import datetime
import RPi.GPIO as GPIO
import water_modif as water
import os

app = Flask(__name__) 

def template(title = "Happy plant :)", text = "", humid = 0):
    dateNow = datetime.datetime.now().strftime("%d/%m/%Y")
    templateDate = {
        'title' : title,
        'date' : dateNow,
        'text' : text,
        'humid' : humid 
        }
    return templateDate

@app.route("/")
def home():
    templateData = template(humid = water.get_status())
    
    return render_template('main.html', **templateData)

@app.route("/get_status")
def dynamicHumid():
    return (water.get_status)

@app.route("/last_watered")
def check_last_watered():
    templateData = template(text = water.get_last_watered(), humid = water.get_status())
    return render_template('main.html', **templateData)

@app.route("/sensor")
def action():
    status = water.get_status()
    message = ""
    if (status < 20):
        message = "J'ai soif :("
    else:
        message = "Je me sens bien :)"

    templateData = template(text = message, humid = water.get_status())
    return render_template('main.html', **templateData)

@app.route("/water")
def action2():
    water.pump_on()
    templateData = template(text = "Arrosée", humid = water.get_status())
    return render_template('main.html', **templateData)

@app.route("/auto/water/<toggle>")
def auto_water(toggle):
    running = False
    if toggle == "ON":
        templateData = template(text = "Arrosage automatique activé", humid = water.get_status())
        for process in psutil.process_iter():
            try:
                if process.cmdline()[1] == 'auto_water.py':
                    templateData = template(text = "Arrosage déjà activé", humid = water.get_status())
                    running = True
            except:
                pass
        if not running:
            os.system("python3.9 auto_water.py&")
    else:
        templateData = template(text = "Arrosage desactivé", humid = water.get_status())
        os.system("pkill -f auto_water.py")

    return render_template('main.html', **templateData)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)