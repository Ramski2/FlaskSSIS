import { addModal } from "./crud/addModal.js";
import { deleteData } from "./crud/delete.js";
import { editModal } from "./crud/editModal.js";
import { fetchTable } from "./utils/fetch_table_filtered.js";
import { handlePagination } from "./utils/pagination.js";
import { filter } from "./utils/searchFilter.js";
import { showToast } from "./utils/toast.js";


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

    const toastData = sessionStorage.getItem("toast");

    if (!toastData) return;

    const { message, type } = JSON.parse(toastData);

    showToast(message, type);

    sessionStorage.removeItem("toast");
});