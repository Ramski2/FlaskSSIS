export function fetchTable(queryParams, tableBodySelector="#table-body", paginationSelector = ".pagination") {
    const tableBody = document.querySelector(tableBodySelector);
    const pagination = document.querySelector(paginationSelector);

    if(!tableBody) {
        console.warn(`Table not found:  ${tableBodySelector}`);
        return;
    }

    if (!pagination) {
        console.warn(`Pagination element not found: ${paginationSelector}`);
    }

    const url = tableBody.dataset.url;

    if (!url) {
        console.warn(`Missing data-url on: ${tableBodySelector}`);
        return;
    }

    const fullUrl = `${url}?${queryParams}`;

    console.log('Fetching: ', fullUrl);

    fetch(fullUrl)
    .then(response => {
        if(!response.ok) throw new Error("Failed to load table data");
        return response.json();
    })
    .then(data => {
        tableBody.innerHTML = data.table;
        if(data.pagination){
            pagination.innerHTML = data.pagination;
        }
        console.log("done")
    })
    .catch(err => {
        console.error("Error loading table: ", err)
    })
}