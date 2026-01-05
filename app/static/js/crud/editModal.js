import { handleFormSubmit } from "../utils/handleSubmit.js";
import { showToast } from "../utils/toast.js";

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

                const imageInput = form.querySelector("#imageInput");
                const imagePreview = form.querySelector("#imagePreview");

                imageInput.addEventListener("change", function () {
                    const file = this.files[0];
                    const maxSizeBytes = 5 * 1024 * 1024;

                    if (!file) return;

                    if (!file.type.startsWith("image/")) {
                        showToast("Only image files are allowed.", "danger");

                        this.value = ""; // clear file input
                        imagePreview.src = "/static/noimage.png";
                        return;
                    }
                    if  (file.size > maxSizeBytes) {
                        showToast("Image exceeds max valid size. (5mb)", "danger")
                        this.value = ""; // clear file input
                        imagePreview.src = "/static/noimage.png";
                        return;
                    }

                    const reader = new FileReader();
                    reader.onload = () => {
                        imagePreview.src = reader.result;
                    };
                    reader.readAsDataURL(file);
                });

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