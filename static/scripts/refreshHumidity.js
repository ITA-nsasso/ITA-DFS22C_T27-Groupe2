function get_status(){
  humid = document.getElementById("humid");
  fetch("http://0.0.0.0/get_status").then(res => res.json()).then(data => humid.innerText = "Taux d'humidité : " + (data['humid']) + "%")
}

function status_loop(){
  setInterval(get_status, 500)
}
