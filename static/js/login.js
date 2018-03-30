function login(){
    let nickname =  document.getElementById('nickname').value
        password = document.getElementById('password').value

    if (nickname && password){
        fetch("/login", {
            headers:{
                "Accept":       "application/json",
                "Content-Type": "application/json"
            },
            method: "POST",
            body:JSON.stringify({
                    "nickname": nickname,
                    "password": password
                }
            )
        }).then(function(response){
            if(response.ok){
                return response.json()
            }
        }).then(function(data){
            console.log(data)
            window.location.href = '/'
        }).catch(error => console.log('Reqest failuer: ', error)
    )}
    else{
        alert("Fill all the fields first!")
    }
}