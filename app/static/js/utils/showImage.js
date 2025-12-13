document.addEventListener("DOMContentLoaded", () => {
    function editModal(modalSelector = "#showImage") {
        const modalElement = document.querySelector(modalSelector);
        if (!modalElement) {
            console.warn("Modal not found:", modalSelector);
            return;
        }
        console.log("Modal Element:", modalElement);

        modalElement.addEventListener('show.bs.modal', event => {
            const container = modalElement.querySelector(".modal-body");
            const button = event.relatedTarget;

            const url = button.getAttribute('data-bs-url');
            console.log(url)

            fetch(url)
            .then(response => {
                if(!response.ok) throw new Error("Failed to load form");
                return response.text();
            })
            .then(html => {
                container.innerHTML = html;
                console.log('changed');
            }) 
            .catch(e => {
                alert("Something went wrong: " + e, "danger")
            })
        });
    }

    editModal()
})