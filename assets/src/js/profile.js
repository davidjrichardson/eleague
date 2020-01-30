function showChangePassword(infoContainer, passContainer, changePassword, contactInfo) {
    infoContainer.classList.add("is-hidden");
    passContainer.classList.remove("is-hidden");
    changePassword.classList.add("is-hidden");
    contactInfo.classList.remove("is-hidden");
}

function showContactInfo(infoContainer, passContainer, changePassword, contactInfo) {
    passContainer.classList.add("is-hidden");
    infoContainer.classList.remove("is-hidden");
    contactInfo.classList.add("is-hidden");
    changePassword.classList.remove("is-hidden");
}

function passwordFormCallback(infoContainer, passContainer, changePassword, contactInfo) {
    // Add cancel button functionality
    let cancelButton = document.getElementById("form-cancel");
    cancelButton.addEventListener('click', function () {
        showContactInfo(infoContainer, passContainer, changePassword, contactInfo);
        passContainer.innerHTML = "";
    });

    // Change the visible view
    showChangePassword(infoContainer, passContainer, changePassword, contactInfo);
    // In case any notifications are added by the new HTML
    refreshNotificationButtons();
    // Add functionality to the form
    resgisterPasswordForm(infoContainer, passContainer, changePassword, contactInfo);
}

function resgisterPasswordForm(infoContainer, passContainer, changePassword, contactInfo) {
    const passwordForm = document.getElementById("password-form");
    let isLoadingForm = false;

    passwordForm.addEventListener("submit", function (ev) {
        ev.preventDefault();

        if (!isLoadingForm) {
            let formData = new FormData(passwordForm);
            let formXHRequest = new XMLHttpRequest();
            formXHRequest.addEventListener("load", function (ev) {
                passContainer.innerHTML = formXHRequest.responseText;
                isLoadingForm = true;

                passwordFormCallback(infoContainer, passContainer, changePassword, contactInfo);
            });
            formXHRequest.open("POST", passwordForm.action);
            formXHRequest.send(formData);
        }

        return false;
    });
}

document.addEventListener('DOMContentLoaded', function () {
    const changePassword = document.getElementById("change-password");
    const contactInfo = document.getElementById("contact-info");
    const infoContainer = document.getElementById("info-container");
    const passContainer = document.getElementById("password-container");

    let isLoadingForm = false;

    changePassword.addEventListener("click", function () {
        if (!isLoadingForm) {
            isLoadingForm = true;
            // Get the data from the other page
            changePassword.classList.add("is-disabled");
            let pageRequest = new XMLHttpRequest();
            pageRequest.addEventListener("load", function (ev) {
                passContainer.innerHTML = pageRequest.responseText;
                changePassword.classList.remove("is-disabled");
                isLoadingForm = false;

                passwordFormCallback(infoContainer, passContainer, changePassword, contactInfo);
            });
            pageRequest.open('GET', formUrl);
            pageRequest.send();
        }
    });

    contactInfo.addEventListener("click", function () {
        showContactInfo(infoContainer, passContainer, changePassword, contactInfo);
        passContainer.innerHTML = "";
    });
});