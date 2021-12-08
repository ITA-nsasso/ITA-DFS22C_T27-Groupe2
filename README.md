# Système d'arrosage pour plante verte

## Présentation du projet
Ce projet, assez classique, consiste à automatiser l'arrosage d'une plante pour la fournir en eau quand elle en a besoin.

Pour ce faire, on utilise un capteur d'humidité planté dans la terre de la plante. Si le taux d'humidité capté par ce dernier passe en dessous d'un seuil (ici 20%), la pompe s'active à intervalle régulier jusqu'à ce que la terre redépasse ce seuil, et est donc considérée comme suffisamment hydratée.

L'interface web du projet présente aussi d'autres fonctionnalités, nottament la possibilité de forcer l'activation de la pompe (ou simplement "l'arrosage"), ainsi que d'accéder à la dernière date/horaire d'arrosage de la plante.

## Équipe sur le projet
Ce projet a été réalisé en équipe, dans le cadre du projet IT-Akademy T27 - IoT. Les membre ayant participé à ce projet sont : 
- Ferial ABDELLI
- Roberto ASCIONE
- Ludovic BLANC
- Achouak HALLOUMI
- Nathan SASSO

## Video de présentation & démonstration
Voici le lien vers notre vidéo de présentation et de démonstration de projet : https://youtu.be/usrXa7U7lEc

## Code commenté
Le code a été commenté afin de préciser l'utilitée de chaque fonction et de chaque route.

## Matériel
- Raspberry Pi 4 model B
- Capteur d'humidité analogique
- Relais 5v
- Puce ADC (dans notre montage, la puce ADS7830 de Freenove)
- Breadboard
- Micro pompe (3-6V recommandé)
- Tuyeau PVC souple
- Et un moyen d'alimenter la pompe, nous recommandons un ancien câble de chargeur de smartphone. Ces câbles permettent de transporter une alimentation de 5V.

## Montage électronique
![Montage électronique](/static/images/montage.jpg "Montage électronique")

## Dépendances
### Support et OS
Ce projet est conçu pour fonctionner sur un Raspberry Pi. En effet, le code contient plusieurs dépendances de librairies utilisées pour communiquer avec les ports GPIO, et la norme de bus I2C. Le système d'exploitation Raspbian OS contient nativement les librairies et supporte également la norme I2C. Un Raspberry Pi et son os Raspbian OS sont donc nécessaires pour le bon fonctionnement de ce projet.

**Il est fortement recommandé de mettre à jour votre Raspberry Pi** avant de lacer le serveur, surtout si c'est la première fois que vous lancez votre Raspberry Pi.

bien-sûr ;
```
sudo apt-get update
```
puis ;
```
sudo apt-get upgrade
```

Cela permet d'assurer la présence et le bon fonctionnement des modules et librairies qui sont utilisés dans ce projet.

### Module I2C 
Avant de pouvoir faire fonctionner notre projet, il est impératif d'activer le chargement automatic du module I2C au noyeau de l'OS, afin de pouvoir communiquer avec la puce ADC.

#### 1ère Étape, Vérifier si le module est actif ou non
Il suffit d'ouvrir un nouvel terminal et de taper la commande suivante : 
```
i2cdetect -y 1
```
Si vous avez le retour :
```
Error: Could not open file `/dev/i2c-1` or `/dev/i2c/1`: No such file or directory
```
**Il vous faut passer à la deuxième étape**.

Si au contraire, vous avez un retour sous le format d'un tableau de valeurs hexadécimales, vous pouvez **ignorer la deuxième étape**

#### 2ème Étape, Activer le module
Toujours dans le terminal, taper la commande : 
```
sudo raspi-config
```
Dirigez vous dans la section options d'interface, puis selectionnez l'option I2C pour activer le module associé. Une fois fait, vous pouvez quitter l'interface de configuration.

On vérifie l'activation de l'interface avec la commande précédente :
```
i2cdetect -y 1
```
le tableau de valeurs hexadécimales apparaît, le module I2C est activé

## Cron
Il est possible de lancer le serveur au démarrage du Raspberry Pi afin d'accéder directement à l'interface sans avoir à lancer le serveur nous même à chaque redémarrage.

Cron permet d'automatiser le lancement de scripts, on peut lui dire dans notre cas d'en lancer un au démarrage.

Pour ce faire, ouvrez un terminal, puis tapez :
```
sudo crontab -e
```

Il vous suffit d'ajouter la ligne suivante tout en haut du fichier :
```
@reboot cd chemin/jusqu'au/projet/local; sudo python web_plants.py
```

Enregistrez, quittez, et c'est opérationnel. Le serveur se lancera à chqaue démarrage du Python, vous n'aurez plus qu'à accéder à l'interface sur le navigateur web du Raspberry Pi directement, ou alors avec le navigateur web d'un matériel sur le même réseau local que le Raspberry Pi grâce à son adresse IP.