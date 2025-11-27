import { fetchTable } from "./fetch_table_filtered.js";

export function handlePagination(paginationSelector = ".pagination") {
    const container = document.querySelector(paginationSelector);

    if (!container) {
        console.warn("Paging container not found");
        return;
    }

    container.addEventListener("click", function (e) {
        const link = e.target.closest(".page-link");

        if (link && link.tagName === "A" && link.href) {
            e.preventDefault();

            const url = new URL(link.href);
            const queryParams = url.searchParams.toString();

            fetchTable(queryParams);
        }
    });
}