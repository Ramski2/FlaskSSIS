import { fetchTable } from "./fetch_table_filtered.js";
import { showToast } from "./toast.js";

export function handleFormSubmit(form, url, methods = "POST", modalInstance = null, next= null) {
    const formData = new FormData(form);

    console.log(formData)

    const existingErrors = form.querySelectorAll(".text-danger.mt-1");
    existingErrors.forEach(el => el.remove());

    fetch(url, {
        method: methods,
        body: formData,
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            form.reset();
            showToast(data.message, "success");
            if(modalInstance?.hide){
                modalInstance.hide();
                const searchForm = document.querySelector("form[role='search']");
                const params = searchForm
                    ? new URLSearchParams(new FormData(searchForm)).toString()
                    : "";

                fetchTable(params);
            } else if(!next) {
                window.location.href = "/student";
            } else {
                window.location.href = next;
            }
        } else if (data.errors) {
                for (const fieldName in data.errors) {
                    const field = form.querySelector(`[name="${fieldName}"]`);
                    if (field) {
                        const errorDiv = document.createElement("div");
                        errorDiv.className = "text-danger mt-1";
                        errorDiv.textContent = data.errors[fieldName][0];
                        field.after(errorDiv);
                    }
                }
        } else if (data.error){
            showToast("Someting went wrong: " + data.error, "danger")
        }
    })
    .catch(error => showToast("Error submitting form: " + error, "danger"));
}