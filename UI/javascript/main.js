function registerUser() {
    let registerSuccessMessage = document.getElementById("form-response-message-ok");
    let registerFailMessage = document.getElementById("form-response-message-fail");
    registerFailMessage.style.display = "none"
    let mySignupLoader = document.getElementById("mysignup-loader");
    mySignupLoader.style.display = "block";

    const USER_USER = 'https://ireporter-challenge-two.herokuapp.com/api/v1/auth/register';
    // const USER_USER = 'http://localhost:5000/api/v1/auth/register';

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
                registerSuccessMessage.innerHTML = myJson.message;
                registerSuccessMessage.style.display = "inline-block";
                for (let user of myJson.data) {
                    setCookie("isAdmin", user.is_admin, 3);
                    setCookie("userIdCookie", user.user_id, 3);
                }
                setTimeout(openHomePage, 2000);
                // openHomePage();
                mySignupLoader.style.display = "none";
            } else {
                registerFailMessage.innerHTML = myJson.error;
                registerFailMessage.style.display = "inline-block";
                mySignupLoader.style.display = "none";
                console.log(myJson.error)
            }
        });
}

function loginUser() {
    let myLoginLoader = document.getElementById("myloader");
    let loginSuccessMessage = document.getElementById("form-response-message-ok");
    let loginFailMessage = document.getElementById("form-response-message-fail");
    loginFailMessage.style.display = "none"
    myLoginLoader.style.display = "block";
    const USER_USER = 'https://ireporter-challenge-two.herokuapp.com/api/v1/auth/login';
    // const USER_USER = 'http://localhost:5000/api/v1/auth/login';

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
                // alert(myJson.message);
                loginSuccessMessage.innerHTML = myJson.message;
                loginSuccessMessage.style.display = "inline-block";
                console.log(myJson.message)
                var accessToken = myJson.access_token;
                setCookie("jwtAccessToken", accessToken, 3)
                for (let user of myJson.data) {
                    setCookie("isAdmin", user.is_admin, 3)
                    setCookie("userIdCookie", user.user_id, 3)
                    if (user.is_admin == true) {
                        setTimeout(openAdminPage, 2000);
                    } else {
                        setTimeout(openHomePage, 2000);
                    }
                    myLoginLoader.style.display = "none";
                }

            } else {
                // alert(myJson.error);
                loginFailMessage.innerHTML = myJson.error;
                loginFailMessage.style.display = "inline-block";
                myLoginLoader.style.display = "none";
                console.log(myJson.error);

            }
        });
}

function uploadMedia(incidentType, incident_id) {
    let userUpdateIncidentImagesLoader = document.getElementById("user-update-incident-images-loader");
    let uploadImageMessageFail = document.getElementById("modal-id-images-message-fail");
    let uploadImageMessageSuccess = document.getElementById("modal-id-images-message-success");
    uploadImageMessageFail.style.display = "none";
    userUpdateIncidentImagesLoader.style.display = "block";
    const URL_INCIDENT = 'https://ireporter-challenge-two.herokuapp.com/api/v1/files/uploads/images/' + incidentType + '/' + incident_id;
    // const URL_INCIDENT = 'http://localhost:5000/api/v1/files/uploads/images/' + incidentType + '/' + incident_id;
    var accessToken = getCookie("jwtAccessToken");
    var date = new Date();
    var timestamp = date.getTime();

    let myHeader = new Headers();
    myHeader.append('Accept', 'application/json');
    myHeader.append('Authorization', 'Bearer ' + accessToken);

    let myFormData = new FormData();

    let myFileInput = document.getElementById('modal-create-new-report-images-input').files[0];
    myFormData.append('images', myFileInput, "IMG-" + timestamp + ".png");
    let req = new Request(URL_INCIDENT, {
        method: 'PATCH',
        headers: myHeader,
        body: myFormData
    });

    // var uploadImageIncidentPrompt = confirm("Continue and upload this image!");
    // if (uploadImageIncidentPrompt == true) {
    fetch(req).then(function (response) {
        return response.json();
    }).then(function (myJson) {

        if (myJson.status == 201) {
            uploadImageMessageSuccess.innerHTML = myJson.message;
            uploadImageMessageSuccess.style.display = "inline-block";
            setTimeout(openHomePage, 2000);
            userUpdateIncidentImagesLoader.style.display = "none";
        } else {
            uploadImageMessageFail.innerHTML = myJson.error;
            uploadImageMessageFail.style.display = "inline-block";
            console.log(myJson.error);
            userUpdateIncidentImagesLoader.style.display = "none";
        }
    }).catch((myError) => {
        uploadImageMessageFail.innerHTML = myError.message;
        uploadImageMessageFail.style.display = "inline-block";
        console.log("Image Upload Error: " + myError.message);
    })
}
// }


function uploadVideo(incidentType, incident_id) {
    let userUpdateIncidentVideosLoader = document.getElementById("user-update-incident-videos-loader");
    let uploadVideosMessageFail = document.getElementById("modal-id-videos-message-fail");
    let uploadVideosMessageSuccess = document.getElementById("modal-id-videos-message-success");
    uploadVideosMessageFail.style.display = "none";
    userUpdateIncidentVideosLoader.style.display = "block";
    const URL_INCIDENT = 'https://ireporter-challenge-two.herokuapp.com/api/v1/files/uploads/videos/' + incidentType + '/' + incident_id;
    // const URL_INCIDENT = 'http://localhost:5000/api/v1/files/uploads/videos/' + incidentType + '/' + incident_id;
    var accessToken = getCookie("jwtAccessToken");
    var date = new Date();
    var timestamp = date.getTime();

    let myHeader = new Headers();
    myHeader.append('Accept', 'application/json');
    myHeader.append('Authorization', 'Bearer ' + accessToken);

    let myFormData = new FormData();

    let myFileInput = document.getElementById('modal-create-new-report-videos-input').files[0];
    myFormData.append('videos', myFileInput, "VID-" + timestamp + ".mp4");
    let req = new Request(URL_INCIDENT, {
        method: 'PATCH',
        headers: myHeader,
        body: myFormData
    });

    // var uploadVideoIncidentPrompt = confirm("Continue and upload this video!");
    // if (uploadVideoIncidentPrompt == true) {
    fetch(req).then(function (response) {
        return response.json();
    }).then(function (myJson) {

        if (myJson.status == 201) {
            uploadVideosMessageSuccess.innerHTML = myJson.message;
            uploadVideosMessageSuccess.style.display = "inline-block";
            setTimeout(openHomePage, 2000);
            console.log(myJson.message);
            userUpdateIncidentVideosLoader.style.display = "none";
        } else {
            uploadVideosMessageFail.innerHTML = myJson.error;
            uploadVideosMessageFail.style.display = "inline-block";
            console.log(myJson.error);
            userUpdateIncidentVideosLoader.style.display = "none";
        }
    }).catch((myError) => {
        uploadVideosMessageFail.innerHTML = myError.message;
        uploadVideosMessageFail.style.display = "inline-block";
        console.log("Video Upload Error: " + myError.message);
    })
}

// }

function createIncident(incidents) {
    let userCreateIncidentLoader = document.getElementById("user-create-incident-loader");
    let createIncidentMessageFail = document.getElementById("modal-id-create-incident-message-fail");
    let createIncidentMessageSuccess = document.getElementById("modal-id-create-incident-message-success");
    createIncidentMessageFail.style.display = "none";
    userCreateIncidentLoader.style.display = "block";

    const URL_INCIDENT = 'https://ireporter-challenge-two.herokuapp.com/api/v1/' + incidents;
    // const URL_INCIDENT = 'http://localhost:5000/api/v1/' + incidents;
    var accessToken = getCookie("jwtAccessToken");

    myLocation = document.getElementById("modal-add-incident-geocoordinates-field").value,
        myVideos = document.getElementById("modal-create-new-report-videos").value.toString().split(','),
        myImages = document.getElementById("modal-create-new-report-images").value.toString().split(',')
    if (myVideos[0].trim().length == 0) {
        myVideos = ["novideo"];
    }

    if (myImages[0].trim().length == 0) {
        myImages = ["noimage"];
    }

    if (myLocation.length == 0) {
        myLocation = "0.32358400000000004, 32.5967872";
    }

    var newIncident = {
        title: document.getElementById("modal-create-new-report-title").value,
        comment: document.getElementById("modal-create-new-report-comment").value,
        location: myLocation,
        videos: myVideos,
        images: myImages
    }
    let fetchData = {
        method: 'POST',
        body: JSON.stringify(newIncident),
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + accessToken
        }
    }

    // var createNewIncidentPrompt = confirm("Continue and create a new incident!");
    // if (createNewIncidentPrompt == true) {
    fetch(URL_INCIDENT, fetchData)
        .then(function (response) {
            return response.json();
        }).then(function (myJson) {
            if (myJson.status == 201) {
                createIncidentMessageSuccess.innerHTML = myJson.message;
                createIncidentMessageSuccess.style.display = "inline-block";
                console.log(myJson.message);
                setTimeout(openHomePage, 2000);
                userCreateIncidentLoader.style.display = "none";
            } else {
                createIncidentMessageFail.innerHTML = myJson.error;
                createIncidentMessageFail.style.display = "inline-block";
                console.log(myJson.error);
                userCreateIncidentLoader.style.display = "none";
            }
        }).catch((myError) => {
            createIncidentMessageFail.innerHTML = myError.message;
            createIncidentMessageFail.style.display = "inline-block";
            console.log("Create Error: " + myError.message);
        });
}
// }

function getAllIncidents(incidents, tableId) {
    let adminIncidentsListLoader = document.getElementById("view-admin-incidents-loader");
    adminIncidentsListLoader.style.display = "block";
    const URL_INCIDENTS = 'https://ireporter-challenge-two.herokuapp.com/api/v1/' + incidents;
    // const URL_INCIDENTS = 'http://localhost:5000/api/v1/' + incidents;
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
                var tableRowIndex = 1;
                for (tableRowIndex; tableRowIndex < incidentsTable.rows.length; tableRowIndex++) {
                    incidentsTable.rows[tableRowIndex].innerHTML = "";
                }
                let noRecordsContainer = document.getElementById("no-records-message-container-id");
                if (jsonData.data.length < 1) {
                    noRecordsContainer.style.display = "block"
                } else {
                    noRecordsContainer.style.display = "none"
                }

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
                    let numberOfImages = incident.images.toString().split(",").length
                    let numberOfVideos = incident.videos.toString().split(",").length
                    imagesCell4.innerHTML = numberOfImages;
                    videosCell5.innerHTML = numberOfVideos;
                    createdOnCell6.innerHTML = incident.created_on;
                    createdByCell7.innerHTML = incident.created_by;
                    statusCell8.innerHTML = incident.status;
                    viewIncidentCell9.innerHTML = '<button class="view-report-btn" id="but" onclick="getIncidentById( \'' + incidents + '\',this, \'' + tableId + '\')">View </button>';

                }

            } else if (jsonData.status == 401) {
                // alert(jsonData.error);
                openSigninPage();
            } else {
                // alert(jsonData.error);
            }
            adminIncidentsListLoader.style.display = "none";
        });
}

function getAllIncidentsPerUserAdmin(incidents, tableId, userId) {

    var accessToken = getCookie("jwtAccessToken");
    let fetchData = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + accessToken
        }
    }

    // var userId = 3;
    // var usersTable = document.getElementById("users-list-table");
    // myRowIndex = element.parentNode.parentNode.rowIndex;
    // var userId = usersTable.rows[myRowIndex].cells[0].innerHTML
    // alert(userId)
    const URL_INCIDENTS = 'https://ireporter-challenge-two.herokuapp.com/api/v1/users/' + userId + '/' + incidents;
    // const URL_INCIDENTS = 'http://localhost:5000/api/v1/users/' + userId + '/' + incidents;

    let userProfileIncidentsSummary = document.getElementById("table-userprofile-all-incidents-summary-admin-view");


    fetch(URL_INCIDENTS, fetchData)
        .then(function (response) {
            return response.json();
        })
        .then(function (jsonData) {
            if (jsonData.status == 200) {
                var incidentsTable = document.getElementById(tableId);
                var numberOfRows = 1;
                var tableRowIndex = 1
                let numberIncidentsPending = 0;
                let numberIncidentsUnder = 0;
                let numberIncidentsResolved = 0;
                let numberIncidentsRejected = 0;

                for (tableRowIndex; tableRowIndex < incidentsTable.rows.length; tableRowIndex++) {
                    incidentsTable.rows[tableRowIndex].innerHTML = "";
                }
                for (let incident of jsonData.data) {

                    let incidentRow = incidentsTable.insertRow(numberOfRows);

                    let incidentIdCell0 = incidentRow.insertCell(0);
                    let typeCell1 = incidentRow.insertCell(1);
                    let titleCell2 = incidentRow.insertCell(2);
                    let imagesCell3 = incidentRow.insertCell(3);
                    let videosCell4 = incidentRow.insertCell(4);
                    let statusCell5 = incidentRow.insertCell(5);
                    let viewIncidentCell6 = incidentRow.insertCell(6);

                    incidentIdCell0.innerHTML = incident.incident_id;
                    typeCell1.innerHTML = incident.incident_type;
                    titleCell2.innerHTML = incident.title;
                    let numberOfImages = incident.images.toString().split(",").length
                    let numberOfVideos = incident.videos.toString().split(",").length
                    if (incident.images.toString().split(",")[0] == "noimage") {
                        imagesCell3.innerHTML = 0;
                    } else {
                        imagesCell3.innerHTML = numberOfImages;
                    }
                    if (incident.images.toString().split(",")[0] == "noimage") {
                        videosCell4.innerHTML = 0;
                    } else {
                        videosCell4.innerHTML = numberOfVideos;
                    }

                    statusCell5.innerHTML = incident.status;
                    viewIncidentCell6.innerHTML = '<button class="view-report-btn" id="but" onclick="getIncidentById( \'' + incidents + '\',this, \'' + tableId + '\')">View </button>';

                    if (incident.status.toLowerCase() == "pending investigation") {
                        numberIncidentsPending += 1;
                    } else if (incident.status.toLowerCase() == "under investigation") {
                        numberIncidentsUnder += 1;
                    } else if (incident.status.toLowerCase() == "resolved") {
                        numberIncidentsResolved += 1;
                    } else {
                        numberIncidentsRejected += 1;
                    }

                }

                // alert(userProfileIncidentsSummary.rows[0].cells[1].innerHTML)
                if (incidents == "interventions") {
                    userProfileIncidentsSummary.rows[2].cells[1].innerHTML = numberIncidentsPending;
                    userProfileIncidentsSummary.rows[2].cells[2].innerHTML = numberIncidentsUnder;
                    userProfileIncidentsSummary.rows[2].cells[3].innerHTML = numberIncidentsResolved;
                    userProfileIncidentsSummary.rows[2].cells[4].innerHTML = numberIncidentsRejected;
                    userProfileIncidentsSummary.rows[2].cells[5].innerHTML = numberIncidentsPending + numberIncidentsUnder + numberIncidentsResolved + numberIncidentsRejected;
                } else {
                    userProfileIncidentsSummary.rows[1].cells[1].innerHTML = numberIncidentsPending;
                    userProfileIncidentsSummary.rows[1].cells[2].innerHTML = numberIncidentsUnder;
                    userProfileIncidentsSummary.rows[1].cells[3].innerHTML = numberIncidentsResolved;
                    userProfileIncidentsSummary.rows[1].cells[4].innerHTML = numberIncidentsRejected;
                    userProfileIncidentsSummary.rows[1].cells[5].innerHTML = numberIncidentsPending + numberIncidentsUnder + numberIncidentsResolved + numberIncidentsRejected;
                }

                userProfileIncidentsSummary.rows[3].cells[1].innerHTML = parseInt(userProfileIncidentsSummary.rows[1].cells[1].innerHTML) + parseInt(userProfileIncidentsSummary.rows[2].cells[1].innerHTML);
                userProfileIncidentsSummary.rows[3].cells[2].innerHTML = parseInt(userProfileIncidentsSummary.rows[1].cells[2].innerHTML) + parseInt(userProfileIncidentsSummary.rows[2].cells[2].innerHTML);
                userProfileIncidentsSummary.rows[3].cells[3].innerHTML = parseInt(userProfileIncidentsSummary.rows[1].cells[3].innerHTML) + parseInt(userProfileIncidentsSummary.rows[2].cells[3].innerHTML);
                userProfileIncidentsSummary.rows[3].cells[4].innerHTML = parseInt(userProfileIncidentsSummary.rows[1].cells[4].innerHTML) + parseInt(userProfileIncidentsSummary.rows[2].cells[4].innerHTML);
                userProfileIncidentsSummary.rows[3].cells[5].innerHTML = parseInt(userProfileIncidentsSummary.rows[1].cells[5].innerHTML) + parseInt(userProfileIncidentsSummary.rows[2].cells[5].innerHTML);

            } else if (jsonData.status == 401) {
                // alert(jsonData.error);
                openSigninPage();
            } else {
                // alert(jsonData.error);
            }
        }).catch((myError) => {
            console.log("Error Loading User Incidents: " + myError.message);
        });
}

function getIncidentTab(response) {
    return response.json();
}

function getAllIncidentsPerUser(incidents, tabSectionId) {
    let userIncidentsListLoader = document.getElementById("view-user-incidents-loader");
    userIncidentsListLoader.style.display = "block";
    var accessToken = getCookie("jwtAccessToken");
    var userId = getCookie("userIdCookie");
    let fetchData = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + accessToken
        }
    }

    const URL_INCIDENTS = 'https://ireporter-challenge-two.herokuapp.com/api/v1/users/' + userId + '/' + incidents;
    // const URL_INCIDENTS = 'http://localhost:5000/api/v1/users/' + userId + '/' + incidents;

    fetch(URL_INCIDENTS, fetchData)
        .then(function (response) {
            return response.json();
        })
        .then(function (jsonData) {
            if (jsonData.status == 200) {
                let noRecordsContainer = document.getElementById("no-records-message-container-id");
                if (jsonData.data.length < 1) {
                    noRecordsContainer.style.display = "block"
                } else {
                    noRecordsContainer.style.display = "none"
                }
                var gridContainerUserIncidents = document.getElementById(tabSectionId);
                gridContainerUserIncidents.innerHTML = "";
                for (let incident of jsonData.data) {
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
                    gridBoxUl.appendChild(gridBoxLiIncidentId);
                    gridBoxUl.appendChild(gridBoxLiTitle);
                    gridBoxUl.appendChild(gridBoxLiRecordType);
                    gridBoxUl.appendChild(gridBoxLiSubmissionDate);
                    gridBoxUl.appendChild(gridBoxLiStatus);
                    gridBoxUl.appendChild(gridBoxLiButtons);

                    gridBoxContainerDiv.appendChild(gridBoxUl);
                    gridContainerUserIncidents.appendChild(gridBoxContainerDiv);
                }

                userIncidentsListLoader.style.display = "none";

            } else if (jsonData.status == 401) {
                // alert(jsonData.error);
                openSigninPage();
                userIncidentsListLoader.style.display = "none";
            } else {
                // alert(jsonData.error);
                userIncidentsListLoader.style.display = "none";
            }
        })
}

function addOnClickEventToFilterButton() {
    // filterIncidentsPerUser(incidents, tabSectionId)
    if (document.getElementById("dashboard-header-incident-type").innerHTML.toString().toLowerCase() == "red-flags") {
        filterIncidentsPerUser('red-flags', 'view-user-redflags');
    } else if (document.getElementById("dashboard-header-incident-type").innerHTML.toString().toLowerCase() == "interventions") {
        filterIncidentsPerUser('interventions', 'view-user-interventions');
    }
    // filterIncidentsPerUser(incidents, tabSectionId)
}

function addOnClickEventToFilterButtonAdmin() {
    // filterIncidentsPerUser(incidents, tabSectionId)
    if (document.getElementById("dashboard-header-incident-type").innerHTML.toString().toLowerCase() == "red-flags") {
        filterAllIncidents('red-flags', 'redflags-list-table');
    } else if (document.getElementById("dashboard-header-incident-type").innerHTML.toString().toLowerCase() == "interventions") {
        filterAllIncidents('interventions', 'interventions-list-table');
    }
    // filterIncidentsPerUser(incidents, tabSectionId)
}

function filterAllIncidents(incidents, tableId) {
    let adminIncidentsListLoader = document.getElementById("view-admin-incidents-loader");
    adminIncidentsListLoader.style.display = "block";
    let dashBoardSelector = document.getElementById("dashboard-select-filter-incidents");
    const URL_INCIDENTS = 'https://ireporter-challenge-two.herokuapp.com/api/v1/' + incidents;
    // const URL_INCIDENTS = 'http://localhost:5000/api/v1/' + incidents;
    var accessToken = getCookie("jwtAccessToken");
    let fetchData = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + accessToken
        }
    }

    let incidentStatus = "";

    if (dashBoardSelector.selectedIndex == 1) {
        dashBoardSelector.selectedIndex = 1;
        incidentStatus = "pending investigation";
    } else if (dashBoardSelector.selectedIndex == 2) {
        dashBoardSelector.selectedIndex = 2;
        incidentStatus = "under investigation";
    } else if (dashBoardSelector.selectedIndex == 3) {
        dashBoardSelector.selectedIndex = 3;
        incidentStatus = "resolved";
    } else if (dashBoardSelector.selectedIndex == 4) {
        dashBoardSelector.selectedIndex = 4;
        incidentStatus = "rejected";
    } else {
        dashBoardSelector.selectedIndex = 0;
        incidentStatus = "all";
    }

    fetch(URL_INCIDENTS, fetchData)
        .then(function (response) {
            return response.json();
        })
        .then(function (jsonData) {
            if (jsonData.status == 200) {
                var incidentsTable = document.getElementById(tableId);
                var numberOfRows = 1;
                var tableRowIndex = 1;
                for (tableRowIndex; tableRowIndex < incidentsTable.rows.length; tableRowIndex++) {
                    incidentsTable.rows[tableRowIndex].innerHTML = "";
                }
                let noRecordsContainer = document.getElementById("no-records-message-container-id");
                if (jsonData.data.length < 1) {
                    noRecordsContainer.style.display = "block"
                } else {
                    noRecordsContainer.style.display = "none"
                }

                for (let incident of jsonData.data) {
                    if (incidentStatus == "all") {
                        let incidentRow = incidentsTable.insertRow(numberOfRows);
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
                        let numberOfImages = incident.images.toString().split(",").length
                        let numberOfVideos = incident.videos.toString().split(",").length
                        imagesCell4.innerHTML = numberOfImages;
                        videosCell5.innerHTML = numberOfVideos;
                        createdOnCell6.innerHTML = incident.created_on;
                        createdByCell7.innerHTML = incident.created_by;
                        statusCell8.innerHTML = incident.status;
                        viewIncidentCell9.innerHTML = '<button class="view-report-btn" id="but" onclick="getIncidentById( \'' + incidents + '\',this, \'' + tableId + '\')">View </button>';
                        numberOfRows += 1;
                    } else if (incidentStatus == incident.status.toLowerCase()) {
                        let incidentRow = incidentsTable.insertRow(numberOfRows);
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
                        let numberOfImages = incident.images.toString().split(",").length
                        let numberOfVideos = incident.videos.toString().split(",").length
                        imagesCell4.innerHTML = numberOfImages;
                        videosCell5.innerHTML = numberOfVideos;
                        createdOnCell6.innerHTML = incident.created_on;
                        createdByCell7.innerHTML = incident.created_by;
                        statusCell8.innerHTML = incident.status;
                        viewIncidentCell9.innerHTML = '<button class="view-report-btn" id="but" onclick="getIncidentById( \'' + incidents + '\',this, \'' + tableId + '\')">View </button>';
                        numberOfRows += 1;
                    }

                }

                adminIncidentsListLoader.style.display = "none";
                if (numberOfRows < 2) {
                    noRecordsContainer.style.display = "block";
                } else {
                    noRecordsContainer.style.display = "none";
                }

            } else if (jsonData.status == 401) {
                // alert(jsonData.error);
                openSigninPage();
            } else {
                // alert(jsonData.error);
            }
            adminIncidentsListLoader.style.display = "none";
        });
}


function filterIncidentsPerUser(incidents, tabSectionId) {
    let userIncidentsListLoader = document.getElementById("view-user-incidents-loader");
    userIncidentsListLoader.style.display = "block";
    let dashBoardSelector = document.getElementById("dashboard-select-filter-incidents");
    var accessToken = getCookie("jwtAccessToken");
    var userId = getCookie("userIdCookie");
    let fetchData = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + accessToken
        }
    }

    let incidentStatus = "";

    if (dashBoardSelector.selectedIndex == 1) {
        dashBoardSelector.selectedIndex = 1;
        incidentStatus = "pending investigation";
    } else if (dashBoardSelector.selectedIndex == 2) {
        dashBoardSelector.selectedIndex = 2;
        incidentStatus = "under investigation";
    } else if (dashBoardSelector.selectedIndex == 3) {
        dashBoardSelector.selectedIndex = 3;
        incidentStatus = "resolved";
    } else if (dashBoardSelector.selectedIndex == 4) {
        dashBoardSelector.selectedIndex = 4;
        incidentStatus = "rejected";
    } else {
        dashBoardSelector.selectedIndex = 0;
        incidentStatus = "all";
    }

    const URL_INCIDENTS = 'https://ireporter-challenge-two.herokuapp.com/api/v1/users/' + userId + '/' + incidents;
    // const URL_INCIDENTS = 'http://localhost:5000/api/v1/users/' + userId + '/' + incidents;

    fetch(URL_INCIDENTS, fetchData)
        .then(function (response) {
            return response.json();
        })
        .then(function (jsonData) {
            if (jsonData.status == 200) {
                let noRecordsContainer = document.getElementById("no-records-message-container-id");
                if (jsonData.data.length < 1) {
                    noRecordsContainer.style.display = "block"
                } else {
                    noRecordsContainer.style.display = "none"
                }
                var gridContainerUserIncidents = document.getElementById(tabSectionId)
                gridContainerUserIncidents.innerHTML = "";
                let numberOfFIlteredIncidents = 0;
                for (let incident of jsonData.data) {
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
                    gridBoxUl.appendChild(gridBoxLiIncidentId);
                    gridBoxUl.appendChild(gridBoxLiTitle);
                    gridBoxUl.appendChild(gridBoxLiRecordType);
                    gridBoxUl.appendChild(gridBoxLiSubmissionDate);
                    gridBoxUl.appendChild(gridBoxLiStatus);
                    gridBoxUl.appendChild(gridBoxLiButtons);

                    gridBoxContainerDiv.appendChild(gridBoxUl);

                    if (incidentStatus == "all") {
                        gridContainerUserIncidents.appendChild(gridBoxContainerDiv);
                        numberOfFIlteredIncidents += 1;
                    } else if (incidentStatus == incident.status.toLowerCase()) {
                        gridContainerUserIncidents.appendChild(gridBoxContainerDiv);
                        numberOfFIlteredIncidents += 1;
                    }
                }
                userIncidentsListLoader.style.display = "none";
                if (numberOfFIlteredIncidents < 1) {
                    noRecordsContainer.style.display = "block";
                } else {
                    noRecordsContainer.style.display = "none";
                }


            } else if (jsonData.status == 401) {
                // alert(jsonData.error);
                openSigninPage();
                userIncidentsListLoader.style.display = "none";
            } else {
                // alert(jsonData.error);
                userIncidentsListLoader.style.display = "none";
            }
        })
}

function disableFilterPropertiesForMap(){
    if (document.getElementById("dashboard-header-incident-type").innerHTML.toString().toLowerCase() == "map"){
        document.getElementById("id-searchreports").disabled = true;
        document.getElementById("dashboard-select-filter-incidents").disabled = true;
    } else {
        document.getElementById("id-searchreports").disabled = false;
        document.getElementById("dashboard-select-filter-incidents").disabled = false;
    }
    if (document.getElementById("dashboard-header-incident-type").innerHTML.toString().toLowerCase() == "users"){
        document.getElementById("dashboard-select-filter-incidents").disabled = true;
    }
}

function searchIncidentsByWord() {
    let tabName = ""
    if (document.getElementById("dashboard-header-incident-type").innerHTML.toString().toLowerCase() == "red-flags") {
        tabName = 'view-user-redflags';
    } else if (document.getElementById("dashboard-header-incident-type").innerHTML.toString().toLowerCase() == "interventions") {
        tabName = 'view-user-interventions';
    }

    let searchInput = document.getElementById("id-searchreports");
    let filterString = searchInput.value.toLowerCase();

    let incidentsContainer = document.getElementById(tabName);
    let incidentsListed = document.getElementById(tabName).children;
    let newIncidentsListed = 0;

    for (let incidentsCounter = 0; incidentsCounter < incidentsContainer.childElementCount; incidentsCounter++) {
        let listedIncident = incidentsListed.item(incidentsCounter).innerHTML.toString().toLowerCase();
        if (listedIncident.indexOf(filterString) > -1) {
            incidentsListed.item(incidentsCounter).style.display = "";
            newIncidentsListed += 1;
        } else {
            incidentsListed.item(incidentsCounter).style.display = "none";
        }
    }

    let noRecordsContainer = document.getElementById("no-records-message-container-id");
    if (newIncidentsListed < 1) {
        noRecordsContainer.style.display = "block"
    } else {
        noRecordsContainer.style.display = "none"
    }
}

function searchAdminIncidentsByWord() {
    let tableName = ""
    if (document.getElementById("dashboard-header-incident-type").innerHTML.toString().toLowerCase() == "red-flags") {
        tableName = 'redflags-list-table';
    } else if (document.getElementById("dashboard-header-incident-type").innerHTML.toString().toLowerCase() == "interventions") {
        tableName = 'interventions-list-table';
    } else if (document.getElementById("dashboard-header-incident-type").innerHTML.toString().toLowerCase() == "users") {
        tableName = 'users-list-table';
    }
    let searchInput = document.getElementById("id-searchreports");
    let filterString = searchInput.value.toLowerCase();

    let itemsTable = document.getElementById(tableName);
    let tableRows = itemsTable.getElementsByTagName("tr");
    let newIncidentsListed = 0;

    for (let indexOfRow = 1; indexOfRow < tableRows.length; indexOfRow++) {
        let listedIncident = tableRows[indexOfRow].innerHTML.toString().toLowerCase();
        if (listedIncident.indexOf(filterString) > -1) {
            tableRows[indexOfRow].style.display = "";
            newIncidentsListed += 1;
        } else {
            tableRows[indexOfRow].style.display = "none";
        }
    }

    let noRecordsContainer = document.getElementById("no-records-message-container-id");
    if (newIncidentsListed < 1) {
        noRecordsContainer.style.display = "block"
    } else {
        noRecordsContainer.style.display = "none"
    }

    // let incidentsContainer = document.getElementById(tabName);
    // let incidentsListed = document.getElementById(tabName).children;
    // let newIncidentsListed = 0;

    // for (let incidentsCounter = 0; incidentsCounter < incidentsContainer.childElementCount; incidentsCounter++) {
    //     let listedIncident = incidentsListed.item(incidentsCounter).innerHTML.toString().toLowerCase();
    //     if (listedIncident.indexOf(filterString) > -1) {
    //         incidentsListed.item(incidentsCounter).style.display = "";
    //         newIncidentsListed+=1;
    //     } else {
    //         incidentsListed.item(incidentsCounter).style.display = "none";
    //     }
    // }

    // let noRecordsContainer = document.getElementById("no-records-message-container-id");
    // if (newIncidentsListed < 1) {
    //     noRecordsContainer.style.display = "block"
    // } else {
    //     noRecordsContainer.style.display = "none"
    // }
}

function getIncidentById(incidents, element, tableId) {
    var incidentTable = document.getElementById(tableId);
    let incidentId = 0;
    myRowIndex = element.parentNode.parentNode.rowIndex;
    if (typeof (tableId) === "string") {
        incidentId = incidentTable.rows[myRowIndex].cells[0].innerHTML;
    } else if (typeof (tableId) === "number") {
        incidentId = tableId;
    }



    const URL_INCIDENT = 'https://ireporter-challenge-two.herokuapp.com/api/v1/' + incidents + "/" + incidentId;
    // const URL_INCIDENT = 'http://localhost:5000/api/v1/' + incidents + "/" + incidentId;
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
                    var incidentImageAdminDiv = document.getElementById("modal-admin-view-incident-images");
                    var incidentVideoAdminDiv = document.getElementById("modal-admin-view-incident-videos");
                    incidentImageAdminDiv.innerHTML = "";
                    incidentVideoAdminDiv.innerHTML = "";

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

                    let incidentsImageUrlString = incident.images.toString().split(',');
                    if (incidentsImageUrlString[0] != "noimage") {
                        for (let myImageIndex = 0; myImageIndex < incidentsImageUrlString.length; myImageIndex++) {
                            let imageElement = document.createElement('img');
                            imageElement.src = incidentsImageUrlString[myImageIndex];
                            incidentImageAdminDiv.appendChild(imageElement)
                        }
                    }

                    let incidentsVideoUrlString = incident.videos.toString().split(',');
                    for (let myVideoIndex = 0; myVideoIndex < incidentsVideoUrlString.length; myVideoIndex++) {
                        let videoElement = document.createElement('video');
                        videoElement.controls = true;
                        let sourceElement = document.createElement('source');
                        sourceElement.src = incidentsVideoUrlString[myVideoIndex];
                        videoElement.appendChild(sourceElement);

                        if (incidentsVideoUrlString[myVideoIndex] != "novideo") {
                            incidentVideoAdminDiv.appendChild(videoElement);
                        }
                    }


                    incidentBody = document.getElementById("model-update-incident-status-btn");
                    incidentBody.innerHTML = '<button id="update-incident-status" class="modal-contents-item edit-form-btn" onclick="changeIncidentStatus(\'' + incidents + '\',' + incidentId + ')">Update </button>';
                }

            } else if (jsonData.status == 401) {
                // alert(jsonData.error);
                openSigninPage();
            } else {
                // alert(jsonData.error);
            }
        })
}

function getUserIncidentById(incidents, incidentId) {
    const URL_INCIDENT = 'https://ireporter-challenge-two.herokuapp.com/api/v1/' + incidents + "/" + incidentId;
    // const URL_INCIDENT = 'http://localhost:5000/api/v1/' + incidents + "/" + incidentId;
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
                    var incidentImageContainerDiv = document.getElementById("modal-incident-images");
                    var incidentVideoContainerDiv = document.getElementById("modal-incident-videos");
                    var incidentImageEditBox = document.getElementById("modal-edit-report-images");
                    var incidentVideoEditBox = document.getElementById("modal-edit-report-videos")
                    incidentImageContainerDiv.innerHTML = "";
                    incidentVideoContainerDiv.innerHTML = "";


                    incidentLocation.value = incident.location;
                    incidentType.innerHTML = incident.incident_type;
                    incidentId.innerHTML = incident.incident_id;
                    incidentTitle.innerHTML = incident.title;
                    incidentComment.innerHTML = incident.comment;
                    incidentCreateDate.innerHTML = incident.created_on;
                    incidentStatus.innerHTML = incident.status;
                    incidentImageEditBox.value = incident.images;
                    incidentVideoEditBox.value = incident.videos;

                    var incidentsImageUrlString = incident.images.toString().split(',');
                    if (incidentsImageUrlString[0] != "noimage") {
                        for (let myImageIndex = 0; myImageIndex < incidentsImageUrlString.length; myImageIndex++) {
                            var imageElement = document.createElement('img');
                            imageElement.src = incidentsImageUrlString[myImageIndex];
                            incidentImageContainerDiv.appendChild(imageElement)
                        }
                    }

                    var incidentsVideoUrlString = incident.videos.toString().split(',');


                    for (let myVideoIndex = 0; myVideoIndex < incidentsVideoUrlString.length; myVideoIndex++) {
                        var videoElement = document.createElement('video');
                        videoElement.controls = true;
                        var sourceElement = document.createElement('source');
                        sourceElement.src = incidentsVideoUrlString[myVideoIndex];
                        videoElement.appendChild(sourceElement);

                        if (incidentsVideoUrlString[myVideoIndex] != "novideo") {
                            incidentVideoContainerDiv.appendChild(videoElement);
                        }
                    }

                    var incidentUpdateImagesBtnDiv = document.getElementById("model-update-incident-images-btn-div");
                    incidentUpdateImagesBtnDiv.innerHTML = '<button id="update-incident-attribute" class="modal-contents-item edit-form-btn" onclick="uploadMedia(\'' + incidents + '\',' + incidentId.innerHTML + ')">Update Images</button>';
                    var incidentUpdateVideosBtnDiv = document.getElementById("model-update-incident-videos-btn-div");
                    incidentUpdateVideosBtnDiv.innerHTML = '<button id="update-incident-attribute-video" class="modal-contents-item edit-form-btn" onclick="uploadVideo(\'' + incidents + '\',' + incidentId.innerHTML + ')">Update Videos</button>';
                    incidentUpdateBtnDiv = document.getElementById("model-update-incident-attribute-btn");
                    incidentUpdateBtnDiv.innerHTML = '<button id="update-incident-attribute" class="modal-contents-item edit-form-btn" onclick="updateUserIncident(\'' + incidents + '\',' + incidentId.innerHTML + ')">Update </button>';
                    incidentDeleteBtnDiv = document.getElementById("model-delete-incident-attribute-btn");
                    incidentDeleteBtnDiv.innerHTML = '<button id="update-incident-attribute" class="modal-contents-item edit-form-btn" onclick="deleteUserIncident(\'' + incidents + '\',' + incidentId.innerHTML + ')">Delete </button>';
                    locationCoordinates = incident.location.split(',');
                    myLatitude = parseFloat(locationCoordinates[0].trim());
                    myLogitude = parseFloat(locationCoordinates[1].trim());
                    showViewIncidentMap(myLatitude, myLogitude, "modal-incident-view-map-location");
                }

            } else if (jsonData.status == 401) {
                // alert(jsonData.error);
                openSigninPage();
            } else {
                // alert(jsonData.error);
            }
        })
}

function updateUserIncident(incidents, incidentId) {
    let userUpdateIncidentAttributeLoader = document.getElementById("user-update-incident-attribute-loader");
    let updateMessageFail = document.getElementById("modal-id-update-message-fail");
    let updateMessageSuccess = document.getElementById("modal-id-update-message-success");
    updateMessageFail.style.display = "none";
    userUpdateIncidentAttributeLoader.style.display = "block";
    var accessToken = getCookie("jwtAccessToken");
    let data = {};
    var incidentAttribute = "";

    var radioButtonComment = document.getElementById("checkbutton-comment");
    var incidentComment = document.getElementById("modal-incident-comment").value;
    var incidentLocation = document.getElementById('modal-view-incident-geocoordinates-field').value

    if (radioButtonComment.checked) {
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

    const URL_INCIDENT = 'https://ireporter-challenge-two.herokuapp.com/api/v1/' + incidents + '/' + incidentId + '/' + incidentAttribute;
    // const URL_INCIDENT = 'http://localhost:5000/api/v1/' + incidents + '/' + incidentId + '/' + incidentAttribute;

    let fetchData = {
        method: 'PATCH',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + accessToken
        }
    }
    // var changeMessage = confirm("Do you really want to change this incident's " + incidentAttribute + "?");
    // if (changeMessage == true) {
    fetch(URL_INCIDENT, fetchData)
        .then(function (response) {
            return response.json();
        })
        .then(function (myJson) {

            if (myJson.status == 201) {
                updateMessageSuccess.innerHTML = "You have successfully updated this incident's " + incidentAttribute;
                updateMessageSuccess.style.display = "inline-block";
                console.log(myJson.message);
                setTimeout(openHomePage, 2000);
                userUpdateIncidentAttributeLoader.style.display = "none";
            } else {
                updateMessageFail.innerHTML = myJson.error;
                updateMessageFail.style.display = "inline-block";
                console.log(myJson.error);
                userUpdateIncidentAttributeLoader.style.display = "none";
            }
        }).catch((myError) => {
            updateMessageFail.innerHTML = myError.message;
            updateMessageFail.style.display = "inline-block";
            console.log(myError.message);
        });
    // return true;
}
// }

function deleteUserIncident(incidents, incidentId) {
    let userDeleteIncidentLoader = document.getElementById("user-delete-incident-loader");
    let deleteMessageFail = document.getElementById("modal-id-delete-message-fail");
    let deleteMessageSuccess = document.getElementById("modal-id-delete-message-success");
    deleteMessageFail.style.display = "none";
    userDeleteIncidentLoader.style.display = "block";

    const URL_INCIDENT = 'https://ireporter-challenge-two.herokuapp.com/api/v1/' + incidents + '/' + incidentId;
    // const URL_INCIDENT = 'http://localhost:5000/api/v1/' + incidents + '/' + incidentId;
    var accessToken = getCookie("jwtAccessToken");
    let fetchData = {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + accessToken
        }
    }

    // var promptDeleteUserIncident = confirm("Do you really want to delete this incident?");
    // if (promptDeleteUserIncident == true) {
    fetch(URL_INCIDENT, fetchData)
        .then(function (response) {
            return response.json();
        }).then(function (myJson) {
            if (myJson.status == 200) {
                deleteMessageSuccess.innerHTML = myJson.message;
                deleteMessageSuccess.style.display = "inline-block";
                setTimeout(openHomePage, 2000);
                console.log(myJson.message);
                userDeleteIncidentLoader.style.display = "none";
            } else {
                deleteMessageFail.innerHTML = myJson.error;
                deleteMessageFail.style.display = "inline-block";
                console.log(myJson.error);
                userDeleteIncidentLoader.style.display = "none";
            }
        }).catch((myError) => {
            deleteMessageFail.innerHTML = myError.message;
            deleteMessageFail.style.display = "inline-block";
            console.log(myError.message);

        });
}


// }

function changeUserRole(userId) {
    let adminUpdateUserLoader = document.getElementById("admin-update-user-loader");
    let updateRoleMessageFail = document.getElementById("modal-id-update-role-message-fail");
    let updateROleMessageSuccess = document.getElementById("modal-id-update-role-message-success");
    updateRoleMessageFail.style.display = "none";
    adminUpdateUserLoader.style.display = "block";
    const URL_USER = 'https://ireporter-challenge-two.herokuapp.com/api/v1/users/' + userId;
    // const URL_USER = 'http://localhost:5000/api/v1/users/' + userId;
    let modalUserRoleChangeBtn = document.getElementById("btn-user-role-change");
    let btnRoleState = modalUserRoleChangeBtn.innerHTML;
    let newUserRole = true;
    if (btnRoleState.toLowerCase() == "make admin") {
        newUserRole = true;
    } else {
        newUserRole = false;
    }

    var accessToken = getCookie("jwtAccessToken");

    let dataf = {
        is_admin: newUserRole
    }

    let fetchDataf = {
        method: 'PATCH',
        body: JSON.stringify(dataf),
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + accessToken
        }
    }

    // var changeMessage = confirm("Do you really want to change this user's role?");
    // if (changeMessage == true) {
    fetch(URL_USER, fetchDataf).then(function (response) {
        return response.json();
    }).then(function (myJson) {
        if (myJson.status == 201) {
            updateROleMessageSuccess.innerHTML = myJson.message;
            updateROleMessageSuccess.style.display = "inline-block";
            console.log(myJson.message);
            setTimeout(openAdminPage, 2000);
            adminUpdateUserLoader.style.display = "none";
        } else {
            updateRoleMessageFail.innerHTML = myJson.error;
            updateRoleMessageFail.style.display = "inline-block";
            console.log(myJson.error);
            adminUpdateUserLoader.style.display = "none";
        }
    }).catch((myError) => {
        updateRoleMessageFail.innerHTML = myError.error;
        updateRoleMessageFail.style.display = "inline-block";
        console.log("Error updating status: " + myError.message);
    });
}
// }

function changeIncidentStatus(incidents, incidentId) {
    let adminUpdateIncidentLoader = document.getElementById("admin-update-incident-loader");
    let updateStatusMessageFail = document.getElementById("modal-id-update-status-message-fail");
    let updateStatusMessageSuccess = document.getElementById("modal-id-update-status-message-success");
    updateStatusMessageFail.style.display = "none";
    adminUpdateIncidentLoader.style.display = "block";
    let modelUpdateIncidentStatusBtn = document.getElementById("model-update-incident-status-btn");
    modelUpdateIncidentStatusBtn.style.display = "block";
    const URL_INCIDENT = 'https://ireporter-challenge-two.herokuapp.com/api/v1/' + incidents + "/" + incidentId + "/status";
    // const URL_INCIDENT = 'http://localhost:5000/api/v1/' + incidents + "/" + incidentId + "/status";
    incidentStatusSelect = document.getElementById("modal-incident-status-select")
    statusChange = incidentStatusSelect.options[incidentStatusSelect.selectedIndex].text;
    var accessToken = getCookie("jwtAccessToken");
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
    // var changeMessage = confirm("Do you really want to change this incident's status?");
    // if (changeMessage == true) {
    fetch(URL_INCIDENT, fetchData)
        .then(function (response) {
            return response.json();
        })
        .then(function (myJson) {
            if (myJson.status == 201) {
                updateStatusMessageSuccess.innerHTML = myJson.message;
                updateStatusMessageSuccess.style.display = "inline-block";
                console.log(myJson.message);
                setTimeout(openAdminPage, 2000);
                modelUpdateIncidentStatusBtn.style.display = "none";
            } else {
                updateStatusMessageFail.innerHTML = myJson.error;
                updateStatusMessageFail.style.display = "inline-block";
                console.log(myJson.error);
                modelUpdateIncidentStatusBtn.style.display = "none";
            }
        }).catch((myError) => {
            updateStatusMessageFail.innerHTML = myError.message;
            updateStatusMessageFail.style.display = "inline-block";
            console.log(myError.message);
        });
    // return true;
}
// }

function getAllUsers() {
    let adminIncidentsListLoader = document.getElementById("view-admin-incidents-loader");
    adminIncidentsListLoader.style.display = "block";
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
                let usersTable = document.getElementById("users-list-table");
                let numberOfRows = 1;
                let tableRowIndex = 1
                for (tableRowIndex; tableRowIndex < usersTable.rows.length; tableRowIndex++) {
                    usersTable.rows[tableRowIndex].innerHTML = "";
                }
                let noRecordsContainer = document.getElementById("no-records-message-container-id");
                if (myJson.data.length < 1) {
                    noRecordsContainer.style.display = "block"
                } else {
                    noRecordsContainer.style.display = "none"
                }
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
                    var viewUserCell8 = userRow.insertCell(8);

                    // Add data to the new cells:
                    idCell0.innerHTML = user.user_id;
                    fullNameCell1.innerHTML = user.firstname + " " + user.lastname;
                    otherNamesCell2.innerHTML = user.othernames;
                    usernameCell3.innerHTML = user.username;
                    emailCell4.innerHTML = user.email;
                    phoneNumberCell5.innerHTML = user.phonenumber;
                    isAdminCell6.innerHTML = user.is_admin;
                    registeredOnCell7.innerHTML = user.registered_on;
                    viewUserCell8.innerHTML = '<button class="view-user-profile-btn" id="btn-view-user" onclick="getUserById(' + user.user_id + '), openViewUserProfileModal(' + user.user_id + '), getAllIncidentsPerUserAdmin(\'red-flags\', \'modal-userprofile-redflags-list-table\',' + user.user_id + '), getAllIncidentsPerUserAdmin(\'interventions\', \'modal-userprofile-redflags-list-table\',' + user.user_id + ');">View </button>';
                    numberOfRows = numberOfRows + 1;
                }
            } else {
                // alert(myJson.error);
                openSigninPage();
            }
            adminIncidentsListLoader.style.display = "none";
        });
}

function reLoadUserDetails(userId) {
    let refreshUserDetailsBtn = document.getElementById("btn-reload-user-profile");
    let adminUpdateUserLoader = document.getElementById("admin-update-user-loader");
    refreshUserDetailsBtn.onclick = function () {
        adminUpdateUserLoader.style.display = "block";
        getUserById(userId);
        // openViewUserProfileModal(userId);
        getAllIncidentsPerUserAdmin("red-flags", "modal-userprofile-redflags-list-table", userId);
        getAllIncidentsPerUserAdmin("interventions", "modal-userprofile-redflags-list-table", userId);
        adminUpdateUserLoader.style.display = "none";
    }
}

function getUserById(userId) {
    const URL_USER = 'https://ireporter-challenge-two.herokuapp.com/api/v1/users/' + userId;
    // const URL_USER = 'http://localhost:5000/api/v1/users/' + userId;
    // The parameters we are gonna pass to the fetch function
    let accessToken = getCookie("jwtAccessToken")
    let fetchData = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + accessToken
        }
    }

    fetch(URL_USER, fetchData).then(function (response) {
        return response.json();
    }).then(function (myJson) {
        if (myJson.status == 200) {
            for (let user of myJson.data) {
                let modalUserId = document.getElementById("modal-users-userid");
                let modalUserFullname = document.getElementById("modal-users-fullname");
                let modalUserOthername = document.getElementById("modal-users-othername");
                let modalUserUsername = document.getElementById("modal-users-username");
                let modalUserEmail = document.getElementById("modal-users-email");
                let modalUserPhonenumber = document.getElementById("modal-users-phonenumber");
                let modalUserIsAdmin = document.getElementById("modal-users-isadmin");
                let modalUserRegisteredOn = document.getElementById("modal-users-registeredon");
                let modalUserRoleChange = document.getElementById("btn-user-role-change");


                modalUserId.innerHTML = user.user_id;
                modalUserFullname.innerHTML = user.firstname + " " + user.lastname;
                modalUserOthername.innerHTML = user.othernames;
                modalUserUsername.innerHTML = user.username;
                modalUserEmail.innerHTML = user.email;
                modalUserPhonenumber.innerHTML = user.phonenumber;
                modalUserIsAdmin.innerHTML = user.is_admin;
                modalUserRegisteredOn.innerHTML = user.registered_on;

                if (user.user_id == 1 || user.user_id == getCookie("userIdCookie")) {
                    modalUserRoleChange.style.display = "none";
                } else if (Boolean(user.is_admin) == Boolean("true") && user.user_id != 1) {
                    modalUserRoleChange.innerHTML = "Revoke Admin Rights";
                    modalUserRoleChange.style.display = "inline-block";
                } else {
                    modalUserRoleChange.innerHTML = "Make Admin";
                    modalUserRoleChange.style.display = "inline-block";
                }




            }
        }
    });

}

function getUserProfileDetails() {
    let userId = getCookie("userIdCookie");
    getUserById(userId);

    // getAllIncidentsPerUser("red-flags", "modal-userprofile-redflags-list-table", userId)
    // getAllIncidentsPerUser("interventions", "modal-userprofile-redflags-list-table", userId)
    getAllIncidentsPerUserAdmin("red-flags", "modal-userprofile-redflags-list-table", userId);
    getAllIncidentsPerUserAdmin("interventions", "modal-userprofile-redflags-list-table", userId);
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

function showViewIncidentMap(myIncidentlatitude, myIncidentLogitude, modalIncidentViewMapLocation) {
    let modalMap = L.map(modalIncidentViewMapLocation);
    modalMap.setView([myIncidentlatitude, myIncidentLogitude], 13);

    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibGx3YXNhbXBpamphIiwiYSI6ImNqczdkY25wbDB3bm0zeW8zaXljaDN3cWgifQ.7GN9HpLQG2mAC6D-2lxuOg', {
        maxZoom: 18,
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
            '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
            'Imagery © <a href="http://mapbox.com">Mapbox</a>',
        id: 'mapbox.streets'
    }).addTo(modalMap);

    let incidentLocationmarker = L.marker([myIncidentlatitude, myIncidentLogitude]);
    incidentLocationmarker.addTo(modalMap)
        .openPopup();

    // var popup = L.popup();

    function onMapClick(e) {
        var extractedLocation = e.latlng.toString().slice(7, -1);
        document.getElementById('modal-view-incident-geocoordinates-field').value = extractedLocation;
        document.getElementById('modal-add-incident-geocoordinates-field').value = extractedLocation;
    }

    document.addEventListener('click', function (event) {
        if (event.target.classList.contains('modal-view-incident-get-geocoordinates')) {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(function (position) {
                    var positionCoordinates = position.coords.latitude + ", " + position.coords.longitude;
                    modalMap.setView([position.coords.latitude, position.coords.longitude], 13);
                    incidentLocationmarker = L.marker([position.coords.latitude, position.coords.longitude]);
                    document.getElementById('modal-view-incident-geocoordinates-field').value = positionCoordinates;
                    document.getElementById('modal-add-incident-geocoordinates-field').value = positionCoordinates;
                });
            } else {
                // alert("HTML5 Geolocation isn't supported by your current browser.");
            }
        }
    }, false);

    modalMap.on('click', onMapClick);
}

function logoutUser() {
    document.cookie = "jwtAccessToken=; expires=Thu, 31 Jan 2018 00:00:00 UTC; path=/;";
    document.cookie = "isAdmin=; expires=Thu, 31 Jan 2018 00:00:00 UTC; path=/;";
    document.cookie = "userIdCookie=; expires=Thu, 31 Jan 2018 00:00:00 UTC; path=/;";
    openSigninPage();
}

function hideNoRecordsMessage() {
    let noRecordsContainer = document.getElementById("no-records-message-container-id");
    noRecordsContainer.style.display = "none";
}