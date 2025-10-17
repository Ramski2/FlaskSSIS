import { handleFormSubmit } from "../utils/handleSubmit.js";

export function editModal(modalSelector= "#editModal") {
    const modalElement = document.querySelector(modalSelector);
    if (!modalElement) {
        console.warn("Modal not found:", modalSelector);
        return;
    }
     console.log("Modal Element:", modalElement);

        modalElement.addEventListener('show.bs.modal', event => {
            const container = modalElement.querySelector(".modal-body");
            const button = event.relatedTarget;

            const formSelector = button.getAttribute('data-bs-form');
            const url = button.getAttribute('data-bs-url');
            const name = button.getAttribute('data-bs-name');
            const id = button.getAttribute('data-bs-id')

            console.log(id);

            const modalTitle = modalElement.querySelector('.modal-title');
            modalTitle.textContent = name;
            console.log(`Opening modal for URL: ${url}, Form: ${formSelector}`);

            fetch(url)
            .then(response => {
                if(!response.ok) throw new Error("Failed to load form");
                return response.text();
            })
            .then(html => {
                container.innerHTML = html;
                console.log('changed');
                const form = modalElement.querySelector(formSelector);
                
                if (!form) {
                    console.warn(`Form not found in modal: ${formSelector}`);
                return;
                }

                const modalInstance = bootstrap.Modal.getOrCreateInstance(modalElement);

                const submitHandler = (e) => {
                    e.preventDefault();
                    console.log("Submitting");
                    handleFormSubmit(form, url, "PUT", modalInstance);
                };

                form.addEventListener("submit", submitHandler);
                modalElement.addEventListener('hide.bs.modal', ev =>{
                    form.removeEventListener("submit", submitHandler);
                });
            }) 
        });
    }