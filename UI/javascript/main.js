function registerUser() {
    const url = 'https://ireporter-challenge-two.herokuapp.com/api/v1/auth/register';
    // const url = 'http://localhost:5000/api/v1/auth/register';

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
    // const url = 'http://localhost:5000/api/v1/auth/login';

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
                var accessToken = myJson.access_token;
                setCookie("jwtAccessToken", accessToken, 30)
                alert(accessToken);
                openHomePage();
            } else {
                alert(myJson.error)
            }
        });
}

function getAllUsers() {
    const url = 'https://ireporter-challenge-two.herokuapp.com/api/v1/users';
    // const url = 'http://localhost:5000/api/v1/users';
    // The parameters we are gonna pass to the fetch function
    var accessToken = getCookie("jwtAccessToken")
    let fetchData = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + accessToken
        }
    }
    fetch(url, fetchData)
        .then(function (response) {
            return response.json();
        })
        .then(function (myJson) {
            if (myJson.status == 200) {
                var usersTable = document.getElementById("users-list-table");
                var numberOfRows = 1;
                for (let user of myJson.data) {
                    alert(JSON.stringify(user));
                    var userRow = usersTable.insertRow(numberOfRows);

                    // Insert new cells (<td> elements)
                    var idCell0 = userRow.insertCell(0);
                    var fullNameCell1 = userRow.insertCell(1);
                    var otherNamesCell2 = userRow.insertCell(2);
                    var usernameCell3 = userRow.insertCell(3);
                    var emailCell4 = userRow.insertCell(4);
                    var phoneNumberCell5 = userRow.insertCell(5);
                    var isAdminCell6 = userRow.insertCell(6);
                    var registeredOnCell7 = userRow.insertCell(7);

                    // Add data to the new cells:
                    idCell0.innerHTML = user.user_id;
                    fullNameCell1.innerHTML = user.firstname + " " + user.lastname;
                    otherNamesCell2.innerHTML = user.username;
                    usernameCell3.innerHTML = user.username;
                    emailCell4.innerHTML = user.email;
                    phoneNumberCell5.innerHTML = user.phonenumber;
                    isAdminCell6.innerHTML = user.is_admin;
                    registeredOnCell7.innerHTML = user.registered_on;
                    numberOfRows = numberOfRows + 1;
                }
            } else {
                alert(myJson.error);
                openSigninPage();
            }
        });
}


function setCookie(cookieName, cookieValue, expiryPeriod) {
    var date = new Date();
    date.setTime(date.getTime() + (expiryPeriod * 24 * 60 * 60 * 1000));
    var expires = "expires=" + date.toGMTString();
    document.cookie = cookieName + "=" + cookieValue + ";" + expires + ";path=/";
}

function getCookie(cookieName) {
    var name = cookieName + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var cookieElements = decodedCookie.split(';');
    for (var i = 0; i < cookieElements.length; i++) {
        var storedCookieValue = cookieElements[i];
        while (storedCookieValue.charAt(0) == ' ') {
            storedCookieValue = storedCookieValue.substring(1);
        }
        if (storedCookieValue.indexOf(name) == 0) {
            return storedCookieValue.substring(name.length, storedCookieValue.length);
        }
    }
    return "";
}