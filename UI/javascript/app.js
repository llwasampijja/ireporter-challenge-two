function toggleMobileMenuVisibility() {
    var menu_ = document.getElementById("mobile-menu");
    if (menu_.style.display === "none") {
        menu_.style.display = "block";
    } else {
        menu_.style.display = "none";
    }
}

function checkIfUserIsLoggedIn() {
    if (getCookie("jwtAccessToken") == "") {
        openSigninPage();
    } else {
        return;
    }
}

function avoidLoginSignupPage() {
    if (getCookie("jwtAccessToken") != "" && getCookie("isAdmin") == "true") {
        openAdminPage();
    } else if (getCookie("jwtAccessToken") != "" && getCookie("isAdmin") == "false") {
        openHomePage();
    } else {
        // alert("You have been logged out, Login again to regain access!");
        return;
    }
}

function avoidAdminPanelForNonAdmins() {
    if (getCookie("isAdmin") == "false") {
        openHomePage();
    }
}

function avoidDashBoardForAdmins() {
    if (getCookie("isAdmin") == "true") {
        openAdminPage();
    }
}

function homePageNotSignedIn() {
    var signedInLInks = document.getElementsByClassName("logged-user-link");
    var mainNavSignInLInk = document.getElementById("main-nav-signin-link");
    var nonAdminLinks = document.getElementsByClassName("non-admin-link");
    var adminLinks = document.getElementsByClassName("admin-link");
    var nonMemberPromptPhrase = document.getElementById("non-member-prompt-phrase");
    var tableUserprofileAllIncidents = document.getElementById("table-userprofile-all-incidents");
    var tableUserprofileAllIncidentsSummary = document.getElementById("table-userprofile-all-incidents-summary");
    var nonMemberPromptButton = document.getElementById("non-member-prompt-button");
    var signedMemberPromptPhrase = document.getElementById("signed-member-prompt-phrase");

    if (getCookie("jwtAccessToken") == "") {
        signedMemberPromptPhrase.style.display = "none"
        mainNavSignInLInk.style.display = "inline-block";
        nonMemberPromptButton.style.display = "block";
        nonMemberPromptPhrase.style.display = "block";
    } else if (getCookie("isAdmin") === "true") {
        for (let signedLink of signedInLInks) {
            signedLink.style.display = "inline-block";
        }

        for (let adminLink of adminLinks) {
            adminLink.style.display = "inline-block";
        }

        if (mainNavSignInLInk != null) {
            mainNavSignInLInk.style.display = "none";
        }

        if (signedMemberPromptPhrase != null) {
            signedMemberPromptPhrase.style.display = "block"
        }

        if (nonMemberPromptButton != null) {
            nonMemberPromptButton.style.display = "none"
        }

        if (nonMemberPromptPhrase != null) {
            nonMemberPromptPhrase.style.display = "none"
        }

    } else {
        for (let signedLink of signedInLInks) {
            signedLink.style.display = "inline-block";
        }
        for (let nonAdminLink of nonAdminLinks) {
            nonAdminLink.style.display = "inline-block";
        }
        if (mainNavSignInLInk != null) {
            mainNavSignInLInk.style.display = "none";
        }
        if (signedMemberPromptPhrase != null) {
            signedMemberPromptPhrase.style.display = "block";
        }
        if (nonMemberPromptButton != null) {
            nonMemberPromptButton.style.display = "none";
        }
        if (nonMemberPromptPhrase != null) {
            nonMemberPromptPhrase.style.display = "none";
        }

        if (tableUserprofileAllIncidentsSummary != null) {
            tableUserprofileAllIncidentsSummary.style.display = "inline-block";
        }

        if (tableUserprofileAllIncidents != null) {
            tableUserprofileAllIncidents.style.display = "inline-block";
        }
    }
}

function openSignupPage() {
    location.href = 'signup.html'
}

function openSigninPage() {
    location.href = 'login.html'
}

function openHomePage() {
    location.href = 'my_reports.html'
}

function openAdminPage() {
    location.href = 'admin_panel.html'
}

function openViewReportsModal() {
    let modalViewReport = document.getElementById('view-report-details-modal');
    // var modalUser = document.getElementById('view-user-profile-modal');
    let mapIncidents = document.getElementById("user-incidents-map");

    document.addEventListener('click', function (event) {
        if (event.target.classList.contains('view-report-btn')) {
            modalViewReport.style.display = "block";
            mapIncidents.style.zIndex = 0;
            // modalUser.style.display = "none";
        }
    }, false);

    // var span = document.getElementsByClassName("close")[0];
    let spanViewReport = document.getElementById("modal-close-profile-view");

    spanViewReport.onclick = function () {
        modalViewReport.style.display = "none";
    }

    window.onclick = function (event) {
        if (event.target == modalViewReport) {
            modalViewReport.style.display = "none";
        }
    }
}

function openViewUserProfileModal(userId) {
    var modal = document.getElementById('view-user-profile-modal');
    

    document.addEventListener('click', function (event) {
        if (event.target.classList.contains('view-user-profile-btn')) {
            modal.style.display = "block";
        }
    }, false);

    var span = document.getElementsByClassName("close")[0];
    // let span = document.getElementById("close-user-profile");

    span.onclick = function () {
        modal.style.display = "none";
    }
    reLoadUserDetails(userId);
    let modalUserRoleChange = document.getElementById("btn-user-role-change");
    modalUserRoleChange.onclick = function () {
        changeUserRole(userId)
    }

    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
}

function createNewReportsModal(incidentTypes) {

    var modal = document.getElementById('create-new-report-modal');
    var mapIncidents = document.getElementById("user-incidents-map");
    // var adminTabLinks = document.getElementsByClassName("admin-tab");
    // if (document.getElementById("dashboard-header-incident-type").innerHTML === "Map") {
    //     openAdminManageTab(event, 'view-user-redflags');
    //     setDashBoardHeaderIncidedentType('Red-flags');

    //     var tabIndex, tabContent, adminTabLinks;
    //     tabContent = document.getElementsByClassName("section-manage-content");

    //     // for (tabIndex = 0; tabIndex < tabContent.length; tabIndex++) {
    //     //     tabContent[tabIndex].style.display = "none";
    //     // }

    //     adminTabLinks = document.getElementsByClassName("admin-tab");

    //     // for (tabIndex = 0; tabIndex < adminTabLinks.length; tabIndex++) {
    //         adminTabLinks[0].className = adminTabLinks[0].className.replace(" active", "");
    //     // }

    //     document.getElementById('view-user-redflags').style.display = "block";
    //     tabEvent.currentTarget.className += " active";
    // }

    showViewIncidentMap(0.3236, 32.5978, "modal-incident-new-map-location");

    document.addEventListener('click', function (event) {
        if (event.target.classList.contains('new-report-btn')) {
            modal.style.display = "block";
            mapIncidents.style.zIndex = 0;
        }
    }, false);

    var span = document.getElementById("close-create-incident-modal");
    var cancel_create_report = document.getElementById("cancel-create-report")
    var save_create_report = document.getElementById("save-create-report")

    span.onclick = function () {
        modal.style.display = "none";
        // mapIncidents.style.display = "block"
    }

    cancel_create_report.onclick = function () {
        modal.style.display = "none";
        // mapIncidents.style.display = "block"
    }

    save_create_report.onclick = function () {
        var incidentType = "";
        var incidentTypeSelect = document.getElementById("modal-incident-type-select");
        if (incidentTypeSelect.selectedIndex == 0) {
            incidentType = "red-flags";
        } else {
            incidentType = "interventions";
        }
        createIncident(incidentType);

    }

    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
            // mapIncidents.style.display = "block";
        }
    }
}

function showPosition() {

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            var positionCoordinates = position.coords.latitude + ", " + position.coords.longitude;
            // alert(positionCoordinates);
            document.getElementById('modal-view-incident-geocoordinates-field').value = positionCoordinates;
            document.getElementById('modal-add-incident-geocoordinates-field').value = positionCoordinates;
        });
    } else {
        // alert("HTML5 Geolocation isn't supported by your current browser.");
    }
}

function openAdminManageTab(tabEvent, tabName) {
    var tabIndex, tabContent, adminTabLinks;
    tabContent = document.getElementsByClassName("section-manage-content");

    for (tabIndex = 0; tabIndex < tabContent.length; tabIndex++) {
        tabContent[tabIndex].style.display = "none";
    }

    adminTabLinks = document.getElementsByClassName("admin-tab");

    for (tabIndex = 0; tabIndex < adminTabLinks.length; tabIndex++) {
        adminTabLinks[tabIndex].className = adminTabLinks[tabIndex].className.replace(" active", "");
    }

    document.getElementById(tabName).style.display = "block";
    tabEvent.currentTarget.className += " active";
}

function setDashBoardHeaderIncidedentType(incidentType) {
    document.getElementById("dashboard-header-incident-type").innerHTML = incidentType;
}

function runAllJavaScript() {
    openViewReportsModal();
    // openViewUserProfileModal();
}
