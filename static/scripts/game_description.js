const toolbar_options = [
  [{ 'header': [false, 1, 2, 3, 4, 5, 6] }],
  ['bold', 'italic', 'underline'],
  ['link'], // 'image'], Add later if time

  [{ 'list': 'ordered'}, { 'list': 'bullet' }],
  [{ 'indent': '-1'}, { 'indent': '+1' }],

  [{ 'align': [] }],
];

const quill = new Quill('#quill-description', {
  modules: {
    toolbar: toolbar_options,
  },
  theme: 'snow',
});

const game_form = document.getElementById("game-edit-form");
game_form.addEventListener("submit", (event) => {
  const true_description = document.getElementById("wtform-description");
  true_description.value = quill.root.innerHTML;
});

document.addEventListener("DOMContentLoaded", (event) => {
  const true_description = document.getElementById("wtform-description");
  quill.root.innerHTML = true_description.value;
})