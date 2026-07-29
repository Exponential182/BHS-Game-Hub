const back_button = document.getElementById("back-button");
const seperator = document.getElementById("error-button-seperator")
const referrer = document.referrer
const self = window.location.origin

if (referrer.startsWith(self) != true) {
    back_button.disabled = true
    back_button.style.display = "none"
    seperator.style.display = "none"
}

back_button.addEventListener("click", () => {
    if (referrer.startsWith(self)) {
        history.back()
    }
});