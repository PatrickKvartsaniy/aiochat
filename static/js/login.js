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
        }).then(data  => window.location.replace('/')
        // }).then(data => console.log(data)
        ).catch(error => console.log('Reqest failuer: ', error)
    )}
    else{
        alert("Fill all the fields first!")
    }
}