const msgField = document.getElementById("textField")
const sendBtn  = document.getElementById("btn")
const msgList  = document.getElementById("media-list")
const friendN  = document.getElementById("friendName")
const addBtn   = document.getElementById("addFriend")

try{
    var ws = new WebSocket("ws://" + window.location.host + "/ws")
}
catch(e){
    var ws = new WebSocket("wss://" + window.location.host + "/ws")
}

function sendMsg(){
    if(msgField.value != ""){
        ws.send(msgField.value)
    }
}

function renderMsg(msg){
    li = document.createElement('li')
    li.innerHTML = msg
    msgList.appendChild(li)
}

function addFriend(){
    friendName = friendN.value
    if(friendName != ""){
        fetch("/friends", {
            headers:{
                "Accept":       "application/json",
                "Content-Type": "application/json"
            },
            method: "POST",
            body:JSON.stringify({
                    "nickname": friendName
                }
            )
        }).then(function(response){
            if (response.ok){
                return response.json()
            }
        }).then(function(data){
            console.log(data)
        }).catch(error => console.error(`Failed to add frined, ${error}`))
    }
}

sendBtn.onclick = ()=> sendMsg()

addBtn.onclick =  ()=>  addFriend()


ws.onmessage = function(e){
    renderMsg(e.data)
}