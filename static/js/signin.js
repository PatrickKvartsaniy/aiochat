function signIn(){
    let nickname     = document.getElementById("nickname").value
        email        = document.getElementById("email").value
        password     = document.getElementById("password").value
        pass_cheking = document.getElementById("password-checking").value

    if(nickname && email && password == pass_cheking){
        fetch("/signin", {
            headers:{
                "Accept":       "application/json",
                "Content-Type": "application/json"
            },
            method: "POST",
            body:JSON.stringify({
                    "nickname": nickname,
                    "email"   : email,
                    "password": password
                }
            )
        }).then(data  => window.location.replace('/')
        ).catch(error => console.log('Reqest failuer: ', error)
    )}
    else{
        alert("Fill all the fields first!")
    }
}