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
        alert(getCookie("jwtAccessToken"));
        alert(getCookie("isAdmin"));
        openSigninPage();
    } else {
        alert(getCookie("jwtAccessToken"));
        alert(getCookie("isAdmin"));
    }
}

function avoidLoginSignupPage() {
    if (getCookie("isAdmin") == "true") {
        alert(getCookie("jwtAccessToken"));
        alert(getCookie("isAdmin"));
        openAdminPage();
    } else if (getCookie("isAdmin") == "false"){
        alert(getCookie("jwtAccessToken"));
        alert(getCookie("isAdmin"));
        openHomePage();
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
    } else if (getCookie("isAdmin")==="true"){
        for (let signedLink of signedInLInks){
            signedLink.style.display = "inline-block";
        }

        for (let adminLink of adminLinks){
            adminLink.style.display = "inline-block";
        }
        // signedInLInks.style.display = "block";
        if (mainNavSignInLInk != null){
            mainNavSignInLInk.style.display = "none";
        }
        
        if (signedMemberPromptPhrase != null){
            signedMemberPromptPhrase.style.display = "block"
        }

        if (nonMemberPromptButton != null){
            nonMemberPromptButton.style.display = "none"
        }

        if (nonMemberPromptPhrase != null){
            nonMemberPromptPhrase.style.display = "none"
        }
    
    } else {
        for (let signedLink of signedInLInks){
            signedLink.style.display = "inline-block";
        }
        for (let nonAdminLink of nonAdminLinks){
            nonAdminLink.style.display = "inline-block";
        }
        if (mainNavSignInLInk != null){
            mainNavSignInLInk.style.display = "none";
        }
        if (signedMemberPromptPhrase != null){
            signedMemberPromptPhrase.style.display = "block";
        }
        if (nonMemberPromptButton != null){
            nonMemberPromptButton.style.display = "none";
        }
        if (nonMemberPromptPhrase != null){
            nonMemberPromptPhrase.style.display = "none";
        }

        if (tableUserprofileAllIncidentsSummary != null){
            tableUserprofileAllIncidentsSummary.style.display = "inline-block";
        }

        if (tableUserprofileAllIncidents!= null){
            tableUserprofileAllIncidents.style.display = "inline-block";
        }
    }
}

function toggleAccountMenuVisibility() {
    var menu_ = document.getElementById("account-menu");
    if (menu_.style.display === "none") {
        menu_.style.display = "block";
    } else {
        menu_.style.display = "none";
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

function confirmDelete() {
    var deleteMessage = confirm("Do you really want to delete this Item?");
    if (deleteMessage == true) {
        window.location.replace("my_reports.html");
        return true;
    }
}


function openViewReportsModal() {
    var modal = document.getElementById('view-report-details-modal');

    document.addEventListener('click', function (event) {
        if (event.target.classList.contains('view-report-btn')) {
            modal.style.display = "block";
        }
    }, false);

    var span = document.getElementsByClassName("close")[0];

    span.onclick = function () {
        modal.style.display = "none";
    }

    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
}

function openEditReportsModal() {
    var modal = document.getElementById('edit-report-details-modal');

    document.addEventListener('click', function (event) {
        if (event.target.classList.contains('edit-report-btn')) {
            modal.style.display = "block";
        }
    }, false);

    var span = document.getElementsByClassName("close")[1];

    span.onclick = function () {
        modal.style.display = "none";
    }

    // cancel_edit_report.onclick = function () {
    //     modal.style.display = "none";
    // }

    // save_edit_report.onclick = function () {
    //     modal.style.display = "none";
    // }

    // window.onclick = function (event) {
    //     if (event.target == modal) {
    //         modal.style.display = "none";
    //     }
    // }
}

// function createNewReportsModal() {
//     var modal = document.getElementById('create-new-report-modal');

//     var create_new_report = document.getElementById('new-report-btn')

//     create_new_report.addEventListener('click', function (event) {
//         modal.style.display = "block"
//     });

//     var span = document.getElementsByClassName("close")[2];
//     var cancel_create_report = document.getElementById("cancel-create-report")
//     var save_create_report = document.getElementById("save-create-report")

//     span.onclick = function () {
//         modal.style.display = "none";
//     }

//     cancel_create_report.onclick = function () {
//         modal.style.display = "none";
//     }

//     save_create_report.onclick = function () {
//         modal.style.display = "none";
//     }

//     window.onclick = function (event) {
//         if (event.target == modal) {
//             modal.style.display = "none";
//         }
//     }
// }

function openRedFlagsSummaryModal() {
    var modal = document.getElementById('redflags-summary-modal');
    // var btn = document.getElementById("redflags-summary-btn");
    var span = document.getElementsByClassName("close")[0];

    // btn.onclick = function () {
    //     modal.style.display = "block";
    // }

    span.onclick = function () {
        modal.style.display = "none";
    }

    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
}

function openInterventionsSummaryModal() {
    var modal = document.getElementById('interventions-summary-modal');
    // var btn = document.getElementById("interventions-summary-btn");
    var span = document.getElementsByClassName("close")[1];

    // btn.onclick = function () {
    //     modal.style.display = "block";
    // }

    span.onclick = function () {
        modal.style.display = "none";
    }

    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
}

function showPosition(){
    if(navigator.geolocation){
        navigator.geolocation.getCurrentPosition(function(position){
            var positionCoordinates = position.coords.latitude + ", " + position.coords.longitude
            document.getElementById('modal-view-incident-geocoordinates-field').value = positionCoordinates;
        });
    } else{
        alert("HTML5 Geolocation isn't supported by your current browser.");
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


function runAllJavaScript() {
    openViewReportsModal();
    // openEditReportsModal();
    // createNewReportsModal();
    // getIncidentById("red-flags");
}

function runAdminScripts() {
    openRedFlagsSummaryModal()
    openInterventionsSummaryModal()
}
