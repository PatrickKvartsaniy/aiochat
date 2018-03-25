function login(){
    let nickname =  document.getElementById('nickname').value
        password = document.getElementById('password').value

    if (login && password){
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
        }).then(data  => console.log('Request succes: ', data)
        ).catch(error => console.log('Reqest failuer: ', error)
    )}
    else{
        alert("Fill all the fields first!")
    }
}