
/*
==========================================
WARD 42 FIX-IT
Live Report Searching
==========================================
*/

document.addEventListener("DOMContentLoaded", function () {

    const searchInput = document.getElementById(
        "live-report-search"
    );

    const reportRows = document.querySelectorAll(
        "[data-report-row]"
    );

    const resultCount = document.getElementById(
        "live-result-count"
    );

    const emptyMessage = document.getElementById(
        "live-empty-message"
    );

    // Only run on the All Reports page
    if (!searchInput || !resultCount) {
        return;
    }


    // Search the currently displayed reports
    function filterReports() {

        const searchText = searchInput.value
            .trim()
            .toLowerCase();

        let visibleCount = 0;

        reportRows.forEach(function (row) {

            // Search only actual report details,
            // not the status dropdown options
            const reportText = (
                row.dataset.searchText || ""
            ).toLowerCase();

            const matches = reportText.includes(
                searchText
            );

            // Show or hide the report
            row.style.display = matches ? "" : "none";

            if (matches) {
                visibleCount++;
            }

        });


        // Update the visible report count
        resultCount.textContent = visibleCount;


        // Show an empty-state message if necessary
        if (emptyMessage) {

            emptyMessage.style.display =
                visibleCount === 0 ? "" : "none";

        }

    }


    // Update immediately as the user types
    searchInput.addEventListener(
        "input",
        filterReports
    );


    // Initialise the results when the page loads
    filterReports();

});
