import { fetchTable } from "../utils/fetch_table.js";
import { showToast } from "../utils/toast.js";

export function deleteData(modalSelector = "#confirmDeleteModal"){
    const modalElement = document.querySelector(modalSelector);
    const confirmButton = modalElement.querySelector('#confirm-delete-btn');

    if (!modalElement) {
        console.warn("Modal not found:", modalSelector);
        return;
    }

    if (!confirmButton) {
        console.warn("Confirm Button not found");
        return;
    }
    console.log("Modal Element:", modalElement);
    console.log("Confirm Button:", confirmButton);

    modalElement.addEventListener('show.bs.modal', event => {
        const button = event.relatedTarget;

        

        const url = button.getAttribute('data-bs-url');
        const id = button.getAttribute('data-bs-id');
        const csrfToken = button.getAttribute('data-csrf-token');

        const modalBody = modalElement.querySelector('.modal-body');
        modalBody.textContent = `Are you sure you want to delete [${id}]?`;

        console.log(`Opening modal for URL: ${url}`);
        
        const modalInstance = bootstrap.Modal.getOrCreateInstance(modalElement);

        const confirmDeleteHandler = (e) => {
            e.preventDefault();

            fetch(url, {
                method: "DELETE",
                headers: {
                    'X-CSRFToken': csrfToken
                } })
                .then(res => res.json())
                .then(data => {
                    if(data.success) {
                        modalInstance.hide();
                        showToast(data.message, "success");
                    
                        const search_form = document.querySelector("form[role='search']");
                        const params = search_form
                            ? new URLSearchParams(new FormData(search_form)).toString()
                            : "";
                                                
                        fetchTable(params);
                    } else {
                        modalInstance.hide();
                        showToast("Error deleting: " + (data.error || JSON.stringify(data.errors)), "danger");
                    }
                })
                .catch(err => showToast("Error: " + err));
        };

        confirmButton.removeEventListener("click", confirmDeleteHandler);
        confirmButton.addEventListener("click", confirmDeleteHandler, { once: true});
    });
}