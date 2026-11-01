
/*
==========================================
WARD 42 FIX-IT
Form Validation and Draft Saving
==========================================
*/

document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("report-fault-form");

    if (!form) {
        return;
    }

    const DRAFT_KEY = "ward42_report_draft_v1";

    const category = document.getElementById("category");
    const street = document.getElementById("street");
    const description = document.getElementById("description");
    const reporterName = document.getElementById("reporter_name");
    const reporterCell = document.getElementById("reporter_cell");

    const draftMessage = document.getElementById("draft-message");
    const clearButton = document.getElementById("clear-draft");

    const allowedCategories = [
        "Pothole",
        "Water leak",
        "Streetlight",
        "Illegal dumping",
        "Other"
    ];

    const fields = [
        category,
        street,
        description,
        reporterName,
        reporterCell
    ];


    // =====================================
    // VALIDATE AN INDIVIDUAL FIELD
    // =====================================

    function validateField(field) {

        const value = field.value.trim();
        let error = "";

        if (field.id === "category") {

            if (!allowedCategories.includes(value)) {
                error = "Please select a valid category.";
            }

        } else if (field.id === "street") {

            if (value.length < 1 || value.length > 150) {
                error = "Enter a street or landmark (maximum 150 characters).";
            }

        } else if (field.id === "description") {

            if (value.length < 10 || value.length > 500) {
                error = "Description must contain 10 to 500 characters.";
            }

        } else if (field.id === "reporter_name") {

            if (value.length < 1 || value.length > 100) {
                error = "Enter your name (maximum 100 characters).";
            }

        } else if (field.id === "reporter_cell") {

            if (!/^0[0-9]{9}$/.test(value)) {
                error = "Enter a 10-digit number starting with 0.";
            }
        }

        const errorElement = document.getElementById(
            field.id + "-client-error"
        );

        if (errorElement) {
            errorElement.textContent = error;
        }

        field.setAttribute(
            "aria-invalid",
            error ? "true" : "false"
        );

        return error === "";
    }


    // =====================================
    // SAVE AN UNFINISHED DRAFT
    // =====================================

    function saveDraft() {

        // Do not store names, phone numbers
        // or photographs in localStorage.

        const draft = {
            category: category.value,
            street: street.value,
            description: description.value
        };

        try {

            localStorage.setItem(
                DRAFT_KEY,
                JSON.stringify(draft)
            );

            draftMessage.textContent =
                "Draft saved on this device.";

        } catch (error) {

            draftMessage.textContent =
                "Draft could not be saved on this device.";
        }
    }


    // =====================================
    // RESTORE A SAVED DRAFT
    // =====================================

    function restoreDraft() {

        try {

            const saved = localStorage.getItem(DRAFT_KEY);

            if (!saved) {
                return;
            }

            const draft = JSON.parse(saved);

            // Do not overwrite information returned
            // after an unsuccessful server submission.
            if (form.dataset.previousSubmit === "true") {
                return;
            }

            category.value = draft.category || "";
            street.value = draft.street || "";
            description.value = draft.description || "";

            draftMessage.textContent =
                "Your saved draft has been restored.";

        } catch (error) {

            draftMessage.textContent =
                "Saved draft could not be restored.";
        }
    }


    // =====================================
    // CLEAR A SAVED DRAFT
    // =====================================

    clearButton.addEventListener("click", function () {

        try {
            localStorage.removeItem(DRAFT_KEY);
        } catch (error) {
            // The user can still clear the fields.
        }

        category.value = "";
        street.value = "";
        description.value = "";

        draftMessage.textContent =
            "Saved draft cleared.";

    });


    // =====================================
    // LIVE VALIDATION
    // =====================================

    fields.forEach(function (field) {

        const eventName =
            field.tagName === "SELECT" ? "change" : "input";

        field.addEventListener(eventName, function () {

            validateField(field);

            if (
                field === category ||
                field === street ||
                field === description
            ) {
                saveDraft();
            }

        });

    });


    // =====================================
    // VALIDATE BEFORE SUBMITTING
    // =====================================

    form.addEventListener("submit", function (event) {

        let valid = true;
        let firstInvalid = null;

        fields.forEach(function (field) {

            if (!validateField(field)) {

                valid = false;

                if (!firstInvalid) {
                    firstInvalid = field;
                }
            }
        });

        if (!valid) {

            event.preventDefault();

            draftMessage.textContent =
                "Please correct the highlighted errors.";

            if (firstInvalid) {
                firstInvalid.focus();
            }
        }

    });


    // Restore saved information on page load
    restoreDraft();

});
