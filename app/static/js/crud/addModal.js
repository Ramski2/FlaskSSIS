    import { handleFormSubmit } from "../utils/handleSubmit.js";

    export function addModal(modalSelector= "#addModal") {
        const modalElement = document.querySelector(modalSelector);
        if (!modalElement) {
            console.warn("Modal not found:", modalSelector);
            return;
        }
        console.log("Modal Element:", modalElement);

            modalElement.addEventListener('show.bs.modal', event => {
                const button = event.relatedTarget;

                const formSelector = button.getAttribute('data-bs-form');
                const url = button.getAttribute('data-bs-url');
                const name = button.getAttribute('data-bs-name');

                console.log(url);

                const modalTitle = modalElement.querySelector('.modal-title');
                modalTitle.textContent = name;
                console.log(`Opening modal for URL: ${url}, Form: ${formSelector}`);

                const form = modalElement.querySelector(formSelector);
                if (!form) {
                    console.warn(`Form not found in modal: ${formSelector}`);
                    return;
                }

                console.log(form)

                const modalInstance = bootstrap.Modal.getOrCreateInstance(modalElement);

                const submitHandler = (e) => {
                    e.preventDefault();
                    handleFormSubmit(form, url, "POST", modalInstance);
                };

                form.addEventListener("submit", submitHandler);

                const imagePreview = form.querySelector("#imagePreview");
                const defaultImageSrc = imagePreview ? imagePreview.src : "";

                modalElement.addEventListener('hide.bs.modal', () =>{
                    form.reset();
                    console.log("Form Reset")
                    if (imagePreview) {
                        imagePreview.src = defaultImageSrc;
                    }
                    form.removeEventListener("submit", submitHandler);
                });
                
            });
        }