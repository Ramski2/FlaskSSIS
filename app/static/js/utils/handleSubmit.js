import { fetchTable } from "./fetch_table_filtered.js";
import { showToast } from "./toast.js";

export function handleFormSubmit(form, url, methods = "POST", modalInstance = null, next= null) {
    const formData = new FormData(form);

    console.log(formData)

    Array.from(form.elements).forEach(element => {
        element.disabled = true
    })

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

            sessionStorage.setItem("toast", JSON.stringify({
                message: data.message,
                type: "success"
            }));

            Array.from(form.elements).forEach(element => {
                element.disabled = false
            })
            
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
            Array.from(form.elements).forEach(element => {
                element.disabled = false
            })
            showToast(data.message, "success")
        } else if (data.errors) {
            Array.from(form.elements).forEach(element => {
                element.disabled = false
            })
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
            Array.from(form.elements).forEach(element => {
                element.disabled = false
            })
            showToast("Someting went wrong", "danger")
            sessionStorage.setItem("toast", JSON.stringify({
                message: "Something went wrong",
                type: "danger"
            }));
        }
    })
    .catch(error => {
        sessionStorage.setItem("toast", JSON.stringify({
                message: "Error submitting form: " + error,
                type: "danger"
        }))
    });
}