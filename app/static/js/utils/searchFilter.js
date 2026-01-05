import { fetchTable } from "./fetch_table_filtered.js";

export function filter(formSelector = "form[role='search']"){
    const search_form = document.querySelector(formSelector)

    if (!search_form) {
        console.warn(`No form found for selector: ${formSelector}`);
        return;
    }

    function getParams(){
        return new URLSearchParams(new FormData(search_form)).toString();
    }

    function reloadTable(){
        const params = getParams();
        fetchTable(params);
    }

    search_form.addEventListener("submit", (e) => {
        e.preventDefault();
        reloadTable();
    });

    const searchInput = search_form.querySelector("input[type='search']");
    let debounceTimer;

    if (searchInput) {
        searchInput.addEventListener("input", () => {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                reloadTable();
            }, 400);
        });
    }

    const autoFilters = search_form.querySelectorAll("select");

    autoFilters.forEach(filter => {
        filter.addEventListener("change", () => {
            reloadTable();
        });
    });
}