
import re


# Categories allowed by our application
ALLOWED_CATEGORIES = {
    "Pothole",
    "Water leak",
    "Streetlight",
    "Illegal dumping",
    "Other"
}


def validate_report(form):

    errors = {}

    # Read the information submitted by the resident
    category = form.get("category", "").strip()
    street = form.get("street", "").strip()
    description = form.get("description", "").strip()
    reporter_name = form.get("reporter_name", "").strip()
    reporter_cell = form.get("reporter_cell", "").strip()

    # Validate the problem category
    if category not in ALLOWED_CATEGORIES:
        errors["category"] = "Please select a valid category."

    # Validate the street name or landmark
    if not 1 <= len(street) <= 150:
        errors["street"] = (
            "Enter a street name or landmark "
            "of no more than 150 characters."
        )

    # Validate the problem description
    if not 10 <= len(description) <= 500:
        errors["description"] = (
            "The description must contain "
            "between 10 and 500 characters."
        )

    # Validate the reporter's name
    if not 1 <= len(reporter_name) <= 100:
        errors["reporter_name"] = (
            "Enter your name using "
            "no more than 100 characters."
        )

    # Validate the cellphone number
    if not re.fullmatch(r"0[0-9]{9}", reporter_cell):
        errors["reporter_cell"] = (
            "Enter a valid 10-digit cellphone "
            "number starting with 0."
        )

    return errors
