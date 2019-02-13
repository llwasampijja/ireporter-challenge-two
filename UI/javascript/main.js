function registerUser() {
    // const USER_USER = 'https://ireporter-challenge-two.herokuapp.com/api/v1/auth/register';
    const USER_USER = 'http://localhost:5000/api/v1/auth/register';

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
    fetch(USER_USER, fetchData)
        .then(function (response) {
            return response.json();
        })
        .then(function (myJson) {
            if (myJson.status == 201) {
                var accessToken = myJson.access_token;
                setCookie("jwtAccessToken", accessToken, 3)
                alert(myJson.message);
                for (let user of myJson.data){
                    setCookie("isAdmin", user.is_admin, 3);
                    setCookie("userIdCookie", user.user_id, 3);
                }
                openHomePage();
            } else {
                alert(myJson.error)
            }
        });
}

function loginUser() {
    // const USER_USER = 'https://ireporter-challenge-two.herokuapp.com/api/v1/auth/login';
    const USER_USER = 'http://localhost:5000/api/v1/auth/login';

    let data = {
        username: document.getElementById("login-username").value,
        password: document.getElementById("login-password").value
    }
    // The parameters to be passed to the fetch function
    let fetchData = {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json'
        }
    }
    fetch(USER_USER, fetchData)
        .then(function (response) {
            return response.json();
        })
        .then(function (myJson) {
            if (myJson.status == 200) {
                alert(myJson.message);
                var accessToken = myJson.access_token;
                setCookie("jwtAccessToken", accessToken, 3)
                for (let user of myJson.data){
                    setCookie("isAdmin", user.is_admin, 3)
                    setCookie("userIdCookie", user.user_id, 3)
                    if (user.is_admin == true){
                        openAdminPage();
                    } else {
                        openHomePage();
                    }
                }
                
            } else {
                alert(myJson.error)
            }
        });
}

function createIncident(incidents){
    // const URL_INCIDENT = 'https://ireporter-challenge-two.herokuapp.com/api/v1/' + incidents;
    const URL_INCIDENT = 'http://localhost:5000/api/v1/' + incidents;
    var accessToken = getCookie("jwtAccessToken");
    var newIncident = {
        title: document.getElementById("modal-create-new-report-title").value,
        comment:document.getElementById("modal-create-new-report-comment").value,
        location: document.getElementById("modal-create-new-report-location").value,
        videos: ["Video url"],
        images: ["imageone", "imagetwo"]
    }
    let fetchData = {
        method: 'POST',
        body: JSON.stringify(newIncident),
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + accessToken
        }
    }

    var createNewIncidentPrompt = confirm("Continue and create a new incident!");
    if (createNewIncidentPrompt == true){
        fetch(URL_INCIDENT, fetchData)
        .then(function(response){
            return response.json();
        }).then(function(myJson){
            if (myJson.status == 201){
                alert(myJson.message);
                openHomePage();
            } else {
                alert(myJson.error)
            }
        })
    }
}

function getAllIncidents(incidents, tableId) {
    // const URL_INCIDENTS = 'https://ireporter-challenge-two.herokuapp.com/api/v1/' + incidents;
    const URL_INCIDENTS = 'http://localhost:5000/api/v1/' + incidents;
    var accessToken = getCookie("jwtAccessToken");
    let fetchData = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + accessToken
        }
    }

    fetch(URL_INCIDENTS, fetchData)
        .then(function (response) {
            return response.json();
        })
        .then(function (jsonData) {
            if (jsonData.status == 200) {
                var incidentsTable = document.getElementById(tableId);
                var numberOfRows = 1;
                for (let incident of jsonData.data) {
                    var incidentRow = incidentsTable.insertRow(numberOfRows);

                    var incidentIdCell0 = incidentRow.insertCell(0);
                    var locationCell1 = incidentRow.insertCell(1);
                    var titleCell2 = incidentRow.insertCell(2);
                    var commentCell3 = incidentRow.insertCell(3);
                    var imagesCell4 = incidentRow.insertCell(4);
                    var videosCell5 = incidentRow.insertCell(5);
                    var createdOnCell6 = incidentRow.insertCell(6);
                    var createdByCell7 = incidentRow.insertCell(7);
                    var statusCell8 = incidentRow.insertCell(8);
                    var viewIncidentCell9 = incidentRow.insertCell(9);

                    incidentIdCell0.innerHTML = incident.incident_id;
                    locationCell1.innerHTML = incident.location;
                    titleCell2.innerHTML = incident.title;
                    commentCell3.innerHTML = incident.comment;
                    imagesCell4.innerHTML = incident.images;
                    videosCell5.innerHTML = incident.videos;
                    createdOnCell6.innerHTML = incident.created_on;
                    createdByCell7.innerHTML = incident.created_by;
                    statusCell8.innerHTML = incident.status;
                    viewIncidentCell9.innerHTML = '<button class="view-report-btn" id="but" onclick="getIncidentById( \''+incidents + '\',this, \''+tableId + '\')">View </button>';
                }

            } else if (jsonData.status == 401) {
                alert(jsonData.error);
                openSigninPage();
            } else {
                alert(jsonData.error);
            }
        })
}

function getIncidentTab(response) {
    return response.json();
}

function getAllIncidentsPerUser(incidents, tabSectionId) {    
    var accessToken = getCookie("jwtAccessToken");
    var userId = getCookie("userIdCookie");
    let fetchData = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + accessToken
        }
    }

    // const URL_INCIDENTS = 'https://ireporter-challenge-two.herokuapp.com/api/v1/users/' + userId + '/' + incidents;
    const URL_INCIDENTS = 'http://localhost:5000/api/v1/users/' + userId + '/' + incidents;

    fetch(URL_INCIDENTS, fetchData)
        .then(function (response) {
            return response.json();
        })
        .then(function (jsonData) {
            if (jsonData.status == 200) {
                for (let incident of jsonData.data) {
                    var gridContainerUserIncidents = document.getElementById(tabSectionId)
                    var gridBoxContainerDiv = document.createElement('div');
                    gridBoxContainerDiv.className = "grid-box-container";
                    var gridBoxUl = document.createElement("ul");
                    var gridBoxLiDivThumbnail = document.createElement("div");
                    gridBoxLiDivThumbnail.className = "grid-item-thumbnail-wrapper";
                    var gridBoxLiThumbnail = document.createElement("li");
                    var gridBoxImgThumbnail = document.createElement("img");
                    gridBoxImgThumbnail.className = "grid-item-thumbnail";
                    gridBoxImgThumbnail.src = "images/intervention.png";
                    gridBoxLiDivThumbnail.appendChild(gridBoxImgThumbnail);
                    gridBoxLiThumbnail.appendChild(gridBoxLiDivThumbnail);
                    
                    var gridBoxLiIncidentId = document.createElement("li");
                    gridBoxLiIncidentId.innerHTML = "Incident Id: "
                    var gridBoxLiSpanIncidentId = document.createElement("span");
                    gridBoxLiSpanIncidentId.innerHTML = incident.incident_id;
                    gridBoxLiIncidentId.appendChild(gridBoxLiSpanIncidentId);
                    var gridBoxLiTitle = document.createElement("li");
                    gridBoxLiTitle.innerHTML = "Title: "
                    var gridBoxLiSpanTitle = document.createElement("span");
                    gridBoxLiSpanTitle.innerHTML = incident.title;
                    gridBoxLiTitle.appendChild(gridBoxLiSpanTitle);
                    var gridBoxLiRecordType = document.createElement("li");
                    gridBoxLiRecordType.innerHTML = "Incident Type: "
                    var gridBoxLiSpanRecordType = document.createElement("span");
                    gridBoxLiSpanRecordType.innerHTML = incident.incident_type;
                    gridBoxLiRecordType.appendChild(gridBoxLiSpanRecordType);
                    var gridBoxLiSubmissionDate = document.createElement("li");
                    gridBoxLiSubmissionDate.innerHTML = "Date: "
                    var gridBoxLiSpanSubmissionDate = document.createElement("span");
                    gridBoxLiSpanSubmissionDate.innerHTML = incident.created_on;
                    gridBoxLiSubmissionDate.appendChild(gridBoxLiSpanSubmissionDate);
                    var gridBoxLiStatus = document.createElement("li");
                    gridBoxLiStatus.innerHTML = "Status: "
                    var gridBoxLiSpanStatus = document.createElement("span");
                    gridBoxLiSpanStatus.innerHTML = incident.status;
                    gridBoxLiStatus.appendChild(gridBoxLiSpanStatus);
                    var gridBoxLiButtons = document.createElement("li");
                    var gridBoxLiDivButtons = document.createElement("div");
                    gridBoxLiDivButtons.className = "buttons-sowa";
                    gridBoxLiDivButtons.innerHTML = '<button class="view-report-btn" id="but" onclick="getUserIncidentById( \'' + incidents + '\', ' + gridBoxLiSpanIncidentId.innerHTML + ')">View </button>';

                    gridBoxLiButtons.appendChild(gridBoxLiDivButtons);

                    gridBoxUl.appendChild(gridBoxLiThumbnail);
                    gridBoxUl.appendChild(gridBoxLiTitle);
                    gridBoxUl.appendChild(gridBoxLiRecordType);
                    gridBoxUl.appendChild(gridBoxLiSubmissionDate);
                    gridBoxUl.appendChild(gridBoxLiStatus);
                    gridBoxUl.appendChild(gridBoxLiButtons);

                    gridBoxContainerDiv.appendChild(gridBoxUl);
                    gridContainerUserIncidents.appendChild(gridBoxContainerDiv);
                }

            } else if (jsonData.status == 401) {
                alert(jsonData.error);
                openSigninPage();
            } else {
                alert(jsonData.error);
            }
        })
}

function getIncidentById(incidents, element, tableId) {
    var incidentTable = document.getElementById(tableId);
    myRowIndex = element.parentNode.parentNode.rowIndex;
    var incidentId = incidentTable.rows[myRowIndex].cells[0].innerHTML


    // const URL_INCIDENT = 'https://ireporter-challenge-two.herokuapp.com/api/v1/' + incidents + "/" + incidentId;
    const URL_INCIDENT = 'http://localhost:5000/api/v1/' + incidents + "/" + incidentId;
    var accessToken = getCookie("jwtAccessToken");
    let fetchData = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + accessToken
        }
    }

    fetch(URL_INCIDENT, fetchData)
        .then(function (response) {
            return response.json();
        })
        .then(function (jsonData) {
            if (jsonData.status == 200) {
                for (let incident of jsonData.data) {
                    incidentTitle = document.getElementById("modal-incident-title");
                    incidentComment = document.getElementById("modal-incident-comment")
                    incidentCreateDate = document.getElementById("modal-incident-create-date")
                    incidentCreateBy = document.getElementById("modal-incident-creator")
                    incidentStatusSelect = document.getElementById("modal-incident-status-select")
                
                    incidentTitle.innerHTML = incident.title;
                    incidentComment.innerHTML = incident.comment;
                    incidentCreateDate.innerHTML = incident.created_on;
                    incidentCreateBy.innerHTML = incident.created_by;
                    if (incident.status.toLowerCase() == "pending investigation") {
                        incidentStatusSelect.selectedIndex = 0;
                    } else if (incident.status.toLowerCase() == "under investigation") {
                        incidentStatusSelect.selectedIndex = 1;
                    } else if (incident.status.toLowerCase() == "resolved") {
                        incidentStatusSelect.selectedIndex = 2;
                    } else {
                        incidentStatusSelect.selectedIndex = 3;
                    }
                    incidentBody = document.getElementById("model-update-incident-status-btn");
                    incidentBody.innerHTML = '<button id="update-incident-status" class="modal-contents-item edit-form-btn" onclick="changeIncidentStatus(\''+incidents+'\',' + incidentId + ')">Update </button>';
                }

            } else if (jsonData.status == 401) {
                alert(jsonData.error);
                openSigninPage();
            } else {
                alert(jsonData.error);
            }
        })
}

function getUserIncidentById(incidents, incidentId) {
    // const URL_INCIDENT = 'https://ireporter-challenge-two.herokuapp.com/api/v1/' + incidents + "/" + incidentId;
    const URL_INCIDENT = 'http://localhost:5000/api/v1/' + incidents + "/" + incidentId;
    var accessToken = getCookie("jwtAccessToken");
    let fetchData = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + accessToken
        }
    }

    fetch(URL_INCIDENT, fetchData)
        .then(function (response) {
            return response.json();
        })
        .then(function (jsonData) {
            if (jsonData.status == 200) {
                for (let incident of jsonData.data) {
                    var incidentType = document.getElementById("modal-incident-type");
                    var incidentId = document.getElementById("modal-incident-id");
                    var incidentTitle = document.getElementById("modal-incident-title");
                    var incidentComment = document.getElementById("modal-incident-comment");
                    var incidentCreateDate = document.getElementById("modal-incident-create-date");
                    var incidentLocation = document.getElementById('modal-view-incident-geocoordinates-field')
                    incidentStatus = document.getElementById("modal-incident-status");
                    incidentEditId = document.getElementById("modal-edit-incident-incident-id");
                    incidentEditType = document.getElementById("modal-edit-incident-incident-type");
                    incidentEditComment = document.getElementById("modal-edit-incident-detailed-description");
                    incindentEditLocation = document.getElementById("modal-edit-incident-geocoordinates-field");

                    incidentLocation.value = incident.location;
                    incidentType.innerHTML = incident.incident_type;
                    incidentId.innerHTML = incident.incident_id;
                    incidentTitle.innerHTML = incident.title;
                    incidentComment.innerHTML = incident.comment;
                    incidentCreateDate.innerHTML = incident.created_on;
                    incidentStatus.innerHTML = incident.status;
                    incidentUpdateBtnDiv = document.getElementById("model-update-incident-attribute-btn");
                    incidentUpdateBtnDiv.innerHTML = '<button id="update-incident-attribute" class="modal-contents-item edit-form-btn" onclick="updateUserIncident(\''+incidents+'\',' + incidentId.innerHTML + ')">Update </button>';
                    incidentDeleteBtnDiv = document.getElementById("model-delete-incident-attribute-btn");
                    incidentDeleteBtnDiv.innerHTML = '<button id="update-incident-attribute" class="modal-contents-item edit-form-btn" onclick="deleteUserIncident(\''+incidents+'\',' + incidentId.innerHTML + ')">Delete </button>';
                }

            } else if (jsonData.status == 401) {
                alert(jsonData.error);
                openSigninPage();
            } else {
                alert(jsonData.error);
            }
        })
}

function updateUserIncident(incidents, incidentId) {
    var accessToken = getCookie("jwtAccessToken");
    let data = {};
    var incidentAttribute = "";

    var radioButtonComment = document.getElementById("checkbutton-comment");
    var incidentComment = document.getElementById("modal-incident-comment").value;
    var incidentLocation = document.getElementById('modal-view-incident-geocoordinates-field').value
 
    if (radioButtonComment.checked){
        incidentAttribute = "comment";
        data = {
            comment: incidentComment
        }
    } else {
        incidentAttribute = "location";
        data = {
            location: incidentLocation
        }
    }

    // const URL_INCIDENT = 'https://ireporter-challenge-two.herokuapp.com/api/v1/' + incidents + '/' + incidentId + '/' + incidentAttribute;
    const URL_INCIDENT = 'http://localhost:5000/api/v1/' + incidents + '/' + incidentId + '/' + incidentAttribute;

    let fetchData = {
        method: 'PATCH',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + accessToken
        }
    }
    var changeMessage = confirm("Do you really want to change this incident's " + incidentAttribute + "?");
    if (changeMessage == true) {
        fetch(URL_INCIDENT, fetchData)
        .then(function (response) {
            return response.json();
        })
        .then(function (myJson) {
            
            if (myJson.status == 201) {
                alert(myJson.message);
                openAdminPage();
            } else {
                alert(myJson.error);
            }
        });
        return true;
    }
}

function deleteUserIncident(incidents, incidentId){
    // const URL_INCIDENT = 'https://ireporter-challenge-two.herokuapp.com/api/v1/' + incidents + '/' + incidentId;
    const URL_INCIDENT = 'http://localhost:5000/api/v1/' + incidents + '/' + incidentId;
    var accessToken = getCookie("jwtAccessToken");
    let fetchData = {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + accessToken
        }
    }

    var promptDeleteUserIncident  = confirm("Do you really want to delete this incident?");
    if (promptDeleteUserIncident == true){
        fetch(URL_INCIDENT, fetchData)
        .then(function(response){
            return response.json();
        }).then(function(myJson){
            if (myJson.status == 200){
                alert(myJson.message);
                openHomePage();
            } else {
                alert(myJson.error);
            }
        })
    }

    
}

function changeIncidentStatus(incidents, incidentId) {
    // const URL_INCIDENT = 'https://ireporter-challenge-two.herokuapp.com/api/v1/' + incidents + "/" + incidentId + "/status";
    const URL_INCIDENT = 'http://localhost:5000/api/v1/' + incidents + "/" + incidentId + "/status";
    incidentStatusSelect = document.getElementById("modal-incident-status-select")
    statusChange =  incidentStatusSelect.options[incidentStatusSelect.selectedIndex].text;
    var accessToken = getCookie("jwtAccessToken")
    let data = {
        status: statusChange.toLowerCase()
    }
    let fetchData = {
        method: 'PATCH',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + accessToken
        }
    }
    var changeMessage = confirm("Do you really want to change this incident's status?");
    if (changeMessage == true) {
        fetch(URL_INCIDENT, fetchData)
        .then(function (response) {
            return response.json();
        })
        .then(function (myJson) {
            if (myJson.status == 201) {
                alert(myJson.message);
                openAdminPage();
            } else {
                alert(myJson.error)
            }
        });
        return true;
    }
}

function getAllUsers() {
    // const url = 'https://ireporter-challenge-two.herokuapp.com/api/v1/users';
    const url = 'http://localhost:5000/api/v1/users';
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
                    otherNamesCell2.innerHTML = user.othernames;
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
    date.setTime(date.getTime() + (expiryPeriod * 60 * 60 * 1000));
    var expires = "expires=" + date.toGMTString();
    document.cookie = cookieName + "=" + cookieValue + ";" + expires + ";path=/";
}

function getCookie(cookieName) {
    var name = cookieName + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var cookieElements = decodedCookie.split(';');
    for (var i = 0; i < cookieElements.length; i++) {
        var storedCookie = cookieElements[i];
        while (storedCookie.charAt(0) == ' ') {
            storedCookie = storedCookie.substring(1);
        }
        if (storedCookie.indexOf(name) == 0) {
            storedCookieValue = storedCookie.substring(name.length, storedCookie.length);
            return storedCookieValue;
        }
    }
    return "";
}

function logoutUser(){
    document.cookie = "jwtAccessToken=; expires=Thu, 31 Jan 2018 00:00:00 UTC; path=/;";
    document.cookie = "isAdmin=; expires=Thu, 31 Jan 2018 00:00:00 UTC; path=/;";
    document.cookie = "userIdCookie=; expires=Thu, 31 Jan 2018 00:00:00 UTC; path=/;";
    openSigninPage();
}