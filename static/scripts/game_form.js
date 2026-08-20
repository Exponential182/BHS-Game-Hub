const max_image_size = 5 * 1024 * 1024; // 5MB
const max_web_game_size = 512 * 1024 * 1024 // 512 MB
const max_game_size = 1024 * 1024 * 1024 // 1GB

const cover_image = document.getElementById("cover-image");
const web_game_upload = document.getElementById("web-game-upload");
const downloadable_game_upload = document.getElementById("downloadable-game-upload");

function update_cover_image(event) {
    const display_name = document.getElementById("cover-image-name");
    const display_image = document.getElementById("cover-image-image");

    if (cover_image.files[0]?.size > max_image_size) {
        cover_image.value = ""
        display_name.textContent = "File too large.";
        return
    }

    if (cover_image.files && cover_image.files.length > 0) {
        display_name.textContent = cover_image.files[0].name;
        display_image.src = URL.createObjectURL(cover_image.files[0])
    } else {
        display_name.textContent = "No file selected.";
    }
}

function update_web_game(event) {
    const display_name = document.getElementById("web-game-name");

    if (web_game_upload.files[0]?.size > max_web_game_size) {
        web_game_upload.value = ""
        display_name.textContent = "File too large.";
        return
    }

    if (web_game_upload.files && web_game_upload.files.length > 0) {
        display_name.textContent = web_game_upload.files[0].name;
    } else {
        display_name.textContent = "No file selected.";
    }
}

function update_downloadable_game(event) {
    const display_name = document.getElementById("downloadable-game-name");

    if (downloadable_game_upload.files[0]?.size > max_game_size) {
        downloadable_game_upload.value = ""
        display_name.textContent = "File too large.";
        return
    }

    if (downloadable_game_upload.files && downloadable_game_upload.files.length > 0) {
        display_name.textContent = downloadable_game_upload.files[0].name;
    } else {
        display_name.textContent = "No file selected.";
    }
}

cover_image.addEventListener("change", update_cover_image);
web_game_upload.addEventListener("change", update_web_game);
downloadable_game_upload.addEventListener("change", update_downloadable_game);

document.addEventListener("DOMContentLoaded", (event) => {
    update_cover_image(event);
    update_web_game(event);
    update_downloadable_game(event);
});