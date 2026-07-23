iframe = document.getElementById("game");
fullscreen_button = document.getElementById("fullscreen");

fullscreen_button.addEventListener("click", () => {
    if (iframe.requestFullscreen) {
        iframe.requestFullscreen()
    }
});

iframe.addEventListener("click", () => {
    if (iframe.requestPointerLock) {
        iframe.requestPointerLock();
    }
});
