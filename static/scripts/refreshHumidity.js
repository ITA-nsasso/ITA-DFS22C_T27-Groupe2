function get_status(){
  fetch("./get_status").then(res => res.json()).then(data => console.log(data))
}

function status_loop(){
  setInterval(get_status, 5000)
}