from flask import Flask, render_template, redirect, url_for
import psutil
import datetime
import RPi.GPIO as GPIO
import water_modif as water
import os

app = Flask(__name__)

def template(title = "Happy plant :)", text = ""):
    dateNow = datetime.datetime.now().strftime("%x")
    timeNow = datetime.datetime.now().strftime("%H:%M")
    templateDate = {
        'title' : title,
        'date' : dateNow,
        'time' : timeNow,
        'text' : text
        }
    return templateDate

@app.route("/")
def hello():
    templateData = template()
    return render_template('main.html', **templateData)

@app.route("/last_watered")
def check_last_watered():
    templateData = template(text = water.get_last_watered())
    return render_template('main.html', **templateData)

@app.route("/sensor")
def action():
    status = water.get_status()
    message = ""
    if (status == 0):
        message = "J'ai soif :("
    else:
        message = "J'me sens bien :)"

    templateData = template(text = message)
    return render_template('main.html', **templateData)

@app.route("/water")
def action2():
    water.pump_on()
    templateData = template(text = "Arrosée")
    return render_template('main.html', **templateData)

@app.route("/auto/water/<toggle>")
def auto_water(toggle):
    running = False
    if toggle == "ON":
        templateData = template(text = "Arrosage automatique activé")
        for process in psutil.process_iter():
            try:
                if process.cmdline()[1] == 'auto_water.py':
                    templateData = template(text = "Arrosage déjà activé")
                    running = True
            except:
                pass
        if not running:
            os.system("python3.9 auto_water.py&")
    else:
        templateData = template(text = "Arrosage desactivé")
        os.system("pkill -f auto_water.py")

    return render_template('main.html', **templateData)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)