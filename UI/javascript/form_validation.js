function validateName(inputId, messageContainerId) {
    var fNameInput = document.getElementById(inputId);
    var wrongFirstNameMsg = document.getElementById(messageContainerId);

    var letters = /^[A-Za-z]+$/;
    if (!fNameInput.value.match(letters)) {
        wrongFirstNameMsg.style.display = "inline-block"
    }
}

function validateOtherName(inputId, messageContainerId) {
    var oNameInput = document.getElementById("reg-othernames");
    var wrongOtherNameMsg = document.getElementById(messageContainerId);
    let otherName = oNameInput.value;

    var letters = /^[A-Za-z]+$/;
    if (otherName != null && !fNameInput.value.match(letters)) {
    // if (!fNameInput.value.match(letters)) {
        wrongFirstNameMsg.style.display = "inline-block"
    }
}