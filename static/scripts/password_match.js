const password = document.getElementById("password");
const confirm_password = document.getElementById("password_repeat");
const error_message = document.getElementById("password-mismatch-error");


function update_mismatch() {
    let matching = password.value == confirm_password.value;
    let valid_password = password.checkValidity();
    let valid_confirmed_password = confirm_password.checkValidity();
    if (!matching && valid_password && valid_confirmed_password) {
        error_message.style.display = "inherit";
        password.classList.add("invalid");
        confirm_password.classList.add("invalid");
    } else {
        error_message.style.display = "none";
        password.classList.remove("invalid");
        confirm_password.classList.remove("invalid");
    }
};

password.addEventListener("blur", (event) => {
    update_mismatch();
})

confirm_password.addEventListener("blur", (event) => {
    update_mismatch();
})
