document.addEventListener("DOMContentLoaded", () => {
    function fetch_Table(tableBodySelector="#table-body", table) {
        const tableBody = document.querySelectorAll(tableBodySelector);
    
        if (tableBody.length === 0) {
            console.warn(`Tables not found: ${tableBodySelector}`);
            return;
        }
        console.log(tableBody)

        tableBody.forEach(tablebody => {
            const url = tablebody.dataset.url;

            if (!url) {
                console.warn(`Missing data-url on: ${tablebody}`);
                return;
            }

            console.log('Fetching: ', url);

            fetch(url)
            .then(response => {
                if(!response.ok) throw new Error("Failed to load table data");
                return response.json();
            })
            .then(data => {
                tablebody.innerHTML = data.table;
                console.log("done")
            })
            .catch(err => {
                console.error("Error loading table: ", err)
            })
        })
    }

    fetch_Table();
})

