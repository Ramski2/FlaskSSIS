import { addModal } from "./crud/addModal.js";
import { deleteData } from "./crud/delete.js";
import { editModal } from "./crud/editModal.js";
import { fetchTable } from "./utils/fetch_table.js";
import { handlePagination } from "./utils/pagination.js";
import { filter } from "./utils/searchFilter.js";


document.addEventListener("DOMContentLoaded", () => {
    console.log("main.js loaded");
    filter();
    handlePagination();
    addModal();
    editModal();
    deleteData();

    const form = document.querySelector("form[role='search']");
      if (form) {
        const params = new URLSearchParams(new FormData(form)).toString();
        fetchTable(params);
      }
});