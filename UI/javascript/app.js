function toggleMobileMenuVisibility() {
    var menu_ = document.getElementById("mobile-menu");
    if (menu_.style.display === "none") {
        menu_.style.display = "block";
    } else {
        menu_.style.display = "none";
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

function confirmDelete() {
    var deleteMessage = confirm("Do you really want to delete this Item?");
    if (deleteMessage == true) {
        window.location.replace("my_reports.html");
        return true;
    }
}


function openViewReportsModal() {
    var modal = document.getElementById('view-report-details-modal');

    // var btn_ = document.getElementsByClassName("view-report-btn");

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
    var cancel_edit_report = document.getElementById("cancel-edit-report")
    var save_edit_report = document.getElementById("save-edit-report")

    span.onclick = function () {
        modal.style.display = "none";
    }

    cancel_edit_report.onclick = function () {
        modal.style.display = "none";
    }

    save_edit_report.onclick = function () {
        modal.style.display = "none";
    }

    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
}

function createNewReportsModal() {
    var modal = document.getElementById('create-new-report-modal');

    var create_new_report = document.getElementById('new-report-btn')

    create_new_report.addEventListener('click', function (event) {
        modal.style.display = "block"
    });

    var span = document.getElementsByClassName("close")[2];
    var cancel_create_report = document.getElementById("cancel-create-report")
    var save_create_report = document.getElementById("save-create-report")

    span.onclick = function () {
        modal.style.display = "none";
    }

    cancel_create_report.onclick = function () {
        modal.style.display = "none";
    }

    save_create_report.onclick = function () {
        modal.style.display = "none";
    }

    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
}

function openRedFlagsSummaryModal() {
    var modal = document.getElementById('redflags-summary-modal');
    var btn = document.getElementById("redflags-summary-btn");
    var span = document.getElementsByClassName("close")[0];

    btn.onclick = function () {
        modal.style.display = "block";
    }

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
    var btn = document.getElementById("interventions-summary-btn");
    var span = document.getElementsByClassName("close")[1];

    btn.onclick = function () {
        modal.style.display = "block";
    }

    span.onclick = function () {
        modal.style.display = "none";
    }

    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
}

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        x.innerHTML = "Geolocation is not supported by your current browser.";
    }
}

function showPosition(position) {

    document.getElementById('geocoordinates-field').innerHTML = position.coords.latitude + "," + position.coords.longitude;
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
    openEditReportsModal();
    createNewReportsModal();
} 

function runAdminScripts(){
    openRedFlagsSummaryModal()
    openInterventionsSummaryModal() 
}