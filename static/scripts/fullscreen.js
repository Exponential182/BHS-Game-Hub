iframe = document.getElementById("game");
fullscreen_button = document.getElementById("fullscreen");

fullscreen_button.addEventListener("click", () => {
    console.log("deteccted")
    if (iframe.requestFullscreen) {
        iframe.requestFullscreen()
    }
}
);