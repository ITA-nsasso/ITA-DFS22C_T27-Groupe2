from flask import Flask, render_template, redirect, url_for, jsonify
import psutil
import datetime
import RPi.GPIO as GPIO
import water_modif as water
import os

app = Flask(__name__) 

# Données passées depuis le back pour être affichées en front
def template(title = "Happy plant :)", text = "", humid = 0):
    dateNow = datetime.datetime.now().strftime("%d/%m/%Y")
    templateDate = {
        'title' : title,
        'date' : dateNow,
        'text' : text,
        'humid' : humid 
        }
    return templateDate

# Différentes routes, permettant de lancer les différentes fonctions du programme, avec un retour front assosié pour informer l'utilisateur
@app.route("/")
def home():
    templateData = template(humid = water.get_status())
    
    return render_template('main.html', **templateData)

# Route permettant la récupération dynamique du taux d'humidité
@app.route("/get_status")
def dynamicHumid():
    return jsonify({'humid' : water.get_status()})

# Route pour avoir la dernière date d'arrosage de la plante
@app.route("/last_watered")
def check_last_watered():
    templateData = template(text = water.get_last_watered(), humid = water.get_status())
    return render_template('main.html', **templateData)

# Route pour retourner un message selon l'état de la terre de la plante
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

# Route activant la pompe de façon manuel
@app.route("/water")
def action2():
    water.pump_on()
    templateData = template(text = "Arrosée", humid = water.get_status())
    return render_template('main.html', **templateData)

# Route pour gérer si l'on dois allumer ou eteindre l'arrosage automatique, selon le paramètre "toggle" récupéré dans l'url
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

# Permets de lancer le serveur web à l'éxécution de ce fichier
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=False)