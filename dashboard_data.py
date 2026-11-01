
# ==========================================
# WARD 42 FIX-IT
# Dashboard Data and Statistics
# ==========================================

import sqlite3

from contextlib import closing
from database import DATABASE_PATH


# ==========================================
# REPORT CATEGORIES AND STATUSES
# ==========================================

CATEGORIES = [
    "Pothole",
    "Water leak",
    "Streetlight",
    "Illegal dumping",
    "Other"
]

STATUSES = [
    "Open",
    "In progress",
    "Closed"
]


# ==========================================
# GET DASHBOARD STATISTICS
# ==========================================

def get_dashboard_summary():

    # Start every category and status at zero
    category_counts = {
        category: 0 for category in CATEGORIES
    }

    status_counts = {
        status: 0 for status in STATUSES
    }

    # Connect to our SQLite database
    with closing(
        sqlite3.connect(DATABASE_PATH)
    ) as connection:

        # Count all submitted reports
        total_reports = connection.execute("""
            SELECT COUNT(*)
            FROM reports
        """).fetchone()[0]

        # Count reports by category
        category_results = connection.execute("""
            SELECT category, COUNT(*)
            FROM reports
            GROUP BY category
        """).fetchall()

        # Count reports by status
        status_results = connection.execute("""
            SELECT status, COUNT(*)
            FROM reports
            GROUP BY status
        """).fetchall()

    # Store the category totals
    for category, count in category_results:
        if category in category_counts:
            category_counts[category] = count

    # Store the status totals
    for status, count in status_results:
        if status in status_counts:
            status_counts[status] = count

    # Return our dashboard information
    return {
        "total_reports": total_reports,
        "by_category": category_counts,
        "by_status": status_counts
    }


# ==========================================
# TEST DASHBOARD DATA
# ==========================================

if __name__ == "__main__":

    summary = get_dashboard_summary()

    print("\nWARD 42 FIX-IT DASHBOARD")
    print("-------------------------")

    print(
        "Total Reports:",
        summary["total_reports"]
    )

    print("\nReports by Category:")

    for category, count in summary["by_category"].items():
        print(f"{category}: {count}")

    print("\nReports by Status:")

    for status, count in summary["by_status"].items():
        print(f"{status}: {count}")
