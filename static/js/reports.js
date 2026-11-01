
/*
==========================================
WARD 42 FIX-IT
Live Report Searching and Filtering
==========================================
*/

document.addEventListener("DOMContentLoaded", function () {

    const searchInput = document.getElementById("live-report-search");
    const categoryFilter = document.getElementById("category");
    const statusFilter = document.getElementById("status");

    const reportRows = document.querySelectorAll("[data-report-row]");
    const resultCount = document.getElementById("live-result-count");
    const emptyMessage = document.getElementById("live-empty-message");

    // Only run on the All Reports page.
    if (!searchInput || !categoryFilter || !statusFilter || !resultCount) {
        return;
    }

    function filterReports() {

        const searchText = searchInput.value.trim().toLowerCase();
        const selectedCategory = categoryFilter.value.trim().toLowerCase();
        const selectedStatus = statusFilter.value.trim().toLowerCase();

        let visibleCount = 0;

        reportRows.forEach(function (row) {

            const reportText = (row.dataset.searchText || "").toLowerCase();

            const category = row.cells[1].textContent.trim().toLowerCase();
            const status = row.cells[3].textContent.trim().toLowerCase();

            const matchesSearch = reportText.includes(searchText);

            const matchesCategory =
                !selectedCategory || category === selectedCategory;

            const matchesStatus =
                !selectedStatus || status === selectedStatus;

            const matchesAll =
                matchesSearch && matchesCategory && matchesStatus;

            row.style.display = matchesAll ? "" : "none";

            if (matchesAll) {
                visibleCount++;
            }
        });

        resultCount.textContent = visibleCount;

        if (emptyMessage) {
            emptyMessage.style.display =
                visibleCount === 0 ? "" : "none";
        }
    }

    // Filter immediately without reloading.
    searchInput.addEventListener("input", filterReports);
    categoryFilter.addEventListener("change", filterReports);
    statusFilter.addEventListener("change", filterReports);

    // Prevent the existing filter form from reloading the page.
    const filterForm = categoryFilter.closest("form");

    if (filterForm) {
        filterForm.addEventListener("submit", function (event) {
            event.preventDefault();
            filterReports();
        });
    }

    // Display the correct count on initial page load.
    filterReports();
});
