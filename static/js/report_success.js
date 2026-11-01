
/*
==========================================
WARD 42 FIX-IT
Clear Draft After Successful Submission
==========================================
*/

document.addEventListener("DOMContentLoaded", function () {

    // Only run on the successful submission page
    const successPage = document.getElementById(
        "report-success"
    );

    if (!successPage) {
        return;
    }

    // Use the same key as report_form.js
    const DRAFT_KEY = "ward42_report_draft_v1";

    try {

        // Remove the completed report's saved draft
        localStorage.removeItem(DRAFT_KEY);

        console.log(
            "Completed report draft cleared successfully."
        );

    } catch (error) {

        console.warn(
            "Saved draft could not be cleared:",
            error
        );

    }

});
