
/*
==========================================
WARD 42 FIX-IT
Dashboard JavaScript
==========================================
*/

// Update the dashboard using JSON information
function updateDashboard(data) {

    // Update the Total Reports card
    const totalElement = document.getElementById(
        "total-reports"
    );

    const total = Number(data.total_reports);

    if (!Number.isFinite(total) || total < 0) {
        throw new Error("Invalid total reports value.");
    }

    totalElement.textContent = total;


    // Update the status KPI cards
    const statusCards = document.querySelectorAll(
        "[data-status-card]"
    );

    statusCards.forEach(function (card) {

        const status = card.dataset.statusCard;
        const count = data.by_status[status] ?? 0;

        card.textContent = count;

    });


    // Update the category and status progress bars
    const dashboardRows = document.querySelectorAll(
        "[data-dashboard-group]"
    );

    dashboardRows.forEach(function (row) {

        const group = row.dataset.dashboardGroup;
        const key = row.dataset.dashboardKey;

        const count = Number(data[group][key] ?? 0);

        if (!Number.isFinite(count) || count < 0) {
            throw new Error("Invalid dashboard count.");
        }

        // Display the count
        const countElement = row.querySelector(
            ".dashboard-count"
        );

        countElement.textContent = count;

        // Calculate the percentage
        const percentage = total > 0
            ? Math.min(100, (count / total) * 100)
            : 0;

        // Update the progress bar
        const progress = row.querySelector(
            ".progress"
        );

        const bar = row.querySelector(
            ".dashboard-bar"
        );

        bar.style.width = percentage + "%";

        progress.setAttribute(
            "aria-valuenow",
            count
        );

        progress.setAttribute(
            "aria-valuemax",
            Math.max(total, 1)
        );

    });

}


// Retrieve statistics from the Flask API
async function loadDashboard() {

    const message = document.getElementById(
        "dashboard-update-message"
    );

    try {

        // Request JSON information
        const response = await fetch(
            "/api/reports/summary",
            {
                method: "GET",
                credentials: "same-origin",
                headers: {
                    "Accept": "application/json"
                },
                cache: "no-store"
            }
        );

        // Check whether the request succeeded
        if (!response.ok) {
            throw new Error(
                "API request failed: " + response.status
            );
        }

        // Convert the JSON response to JavaScript data
        const data = await response.json();

        if (
            !data.by_category ||
            !data.by_status
        ) {
            throw new Error(
                "Incomplete dashboard information."
            );
        }

        // Update the dashboard
        updateDashboard(data);

        // Display a success message
        message.textContent =
            "Dashboard statistics loaded successfully.";

    } catch (error) {

        console.error(
            "Dashboard loading error:",
            error
        );

        // Keep the server-rendered figures visible
        message.textContent =
            "Could not refresh statistics from the API. " +
            "Showing figures from when the page opened.";

    }

}


// Load API statistics when the page opens
document.addEventListener(
    "DOMContentLoaded",
    loadDashboard
);
