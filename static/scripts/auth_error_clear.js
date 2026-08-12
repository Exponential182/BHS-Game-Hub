const input_fields = document.getElementsByClassName("w3-input")

function hideErrorMessages(event) {
    console.log("hiding")
    let input_element = event.currentTarget;
    let input_container = input_element.parentNode;
    let errors = input_container.querySelectorAll(".error-message");
    if (input_element.checkValidity()) {
        for (const error_message of errors) {
            error_message.style.display = "none";
        };
        input_element.removeEventListener("blur", hideErrorMessages);
    };
};

for (const input of input_fields) {
    input.addEventListener("blur", hideErrorMessages)
};