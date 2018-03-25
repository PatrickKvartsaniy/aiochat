const msg   = document.getElementById("messageText")
// const btn   = document.getElementById("send")
const field = document.getElementById("media-list")

try{
    var ws = new WebSocket("ws://" + window.location.host + "/ws")
}
catch(e){
    var ws = new WebSocket("wss://" + window.location.host + "/ws")
}

ws.onmessage = function(e){
    renderMsg(e.data)
}

function sendMsg(){
    if(msg.value != ""){
        ws.send(msg.value)
    }
}

function renderMsg(msg){
    li = document.createElement('li')
    li.innerHTML = msg
    field.appendChild(li)
}