// Cherche et remplace dynamiquement la valeur de la balise avec id "humid" avec le retour de la fonction Python en appelant la route du même nom ("get_status")
function get_status(){
  humid = document.getElementById("humid");
  fetch("/get_status").then(res => res.json()).then(data => humid.innerText = "Taux d'humidité : " + (data['humid']) + "%")
}

// Fonction appelée depuis le HTML, permets d'appeler la fonction "get_status" toutes les 0.5s
function status_loop(){
  setInterval(get_status, 500)
}
