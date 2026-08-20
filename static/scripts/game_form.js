const max_image_size = 5 * 1024 * 1024; // 5MB
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

cover_image.addEventListener("change", update_cover_image);

document.addEventListener("DOMContentLoaded", (event) => {
    update_cover_image(event);
});