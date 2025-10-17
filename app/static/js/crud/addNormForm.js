import { handleFormSubmit } from "../utils/handleSubmit.js";

document.addEventListener("DOMContentLoaded", function (){
    const formSelector = "#addingForm"
    console.log("addForm Running");
    const form = document.querySelector(formSelector);

    if (!form) {
        console.warn("Form not found:", formSelector);
        return;
    }

    const url = form.getAttribute('data-url');
    const nextUrl = form.getAttribute('data-next');

    console.log(url, nextUrl);

    form.addEventListener("submit", (e) => {
        e.preventDefault();
        console.log(url, nextUrl);
        handleFormSubmit(form, url, "POST", null, nextUrl);
    })
});

    
