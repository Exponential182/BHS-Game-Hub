back_button = document.getElementById("back-button");

back_button.addEventListener("click", () => {
    if (window.history.length > 1) {
        history.back()
    }
});