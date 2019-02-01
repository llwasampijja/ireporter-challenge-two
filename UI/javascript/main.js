accessToken = "";
function registerUser() {
    const url = 'https://ireporter-challenge-two.herokuapp.com/api/v1/auth/register';

    let data = {
        firstname: document.getElementById("reg-firstname").value,
        lastname: document.getElementById("reg-lastname").value,
        othernames: document.getElementById("reg-othernames").value,
        phonenumber: document.getElementById("reg-phonenumber").value,
        email: document.getElementById("reg-email").value,
        username: document.getElementById("reg-username").value,
        password: document.getElementById("reg-password").value
    }
    // The parameters we are gonna pass to the fetch function
    let fetchData = {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json'
        }
    }
    fetch(url, fetchData)
        .then(function (response) {
            return response.json();
        })
        .then(function (myJson) {
            if (myJson.status == 201) {
                alert(myJson.message);
                openHomePage();
            } else {
                alert(myJson.error)
            }
        });
}

function loginUser() {
    const url = 'https://ireporter-challenge-two.herokuapp.com/api/v1/auth/login';

    let data = {
        username: document.getElementById("login-username").value,
        password: document.getElementById("login-password").value
    }
    // The parameters we are gonna pass to the fetch function
    let fetchData = {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json'
        }
    }
    fetch(url, fetchData)
        .then(function (response) {
            return response.json();
        })
        .then(function (myJson) {
            if (myJson.status == 200) {
                alert(myJson.message);
                accessToken = myJson.access_token;
                alert(accessToken);
                openHomePage();
            } else {
                alert(myJson.error)
            }
        });
}