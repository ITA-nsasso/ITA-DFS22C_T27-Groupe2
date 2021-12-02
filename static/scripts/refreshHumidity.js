function get_status(){
  humid = document.getElementById("humid");
  fetch("./get_status").then(res => res.json()).then(data => humid.innerText = (data['humid']) + "%")
}

function status_loop(){
  setInterval(get_status, 5000)
}