# ==========================================
# WARD 42 FIX-IT - Report Management Functions
# ==========================================

import sqlite3
from contextlib import closing
from database import DATABASE_PATH

ALLOWED_CATEGORIES = {
    "Pothole", "Water leak", "Streetlight", "Illegal dumping", "Other"
}
ALLOWED_STATUSES = {"Open", "In progress", "Closed"}


def get_all_reports(category="", status=""):
    if category not in ALLOWED_CATEGORIES:
        category = ""
    if status not in ALLOWED_STATUSES:
        status = ""

    query = """
        SELECT id, reference, category, street, description,
               reporter_name, reporter_cell, photo_path, status, created_at
        FROM reports
        WHERE 1 = 1
    """
    parameters = []

    if category:
        query += " AND category = ?"
        parameters.append(category)
    if status:
        query += " AND status = ?"
        parameters.append(status)

    query += " ORDER BY created_at DESC, id DESC"

    with closing(sqlite3.connect(DATABASE_PATH)) as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.execute(query, parameters)
        return [dict(row) for row in cursor.fetchall()]


def get_report_by_id(report_id):
    """Fetch a single report using a parameterised query."""
    if not isinstance(report_id, int) or isinstance(report_id, bool) or report_id <= 0:
        return None

    with closing(sqlite3.connect(DATABASE_PATH)) as connection:
        connection.row_factory = sqlite3.Row
        row = connection.execute("""
            SELECT id, reference, category, street, description,
                   reporter_name, reporter_cell, photo_path, status, created_at
            FROM reports
            WHERE id = ?
        """, (report_id,)).fetchone()
    return dict(row) if row else None


def update_report_status(report_id, new_status):
    if new_status not in ALLOWED_STATUSES:
        raise ValueError("Invalid report status.")
    if not isinstance(report_id, int) or isinstance(report_id, bool) or report_id <= 0:
        raise ValueError("Invalid report ID.")

    with closing(sqlite3.connect(DATABASE_PATH)) as connection:
        with connection:
            cursor = connection.execute("""
                UPDATE reports
                SET status = ?
                WHERE id = ?
            """, (new_status, report_id))
            report_found = cursor.rowcount > 0
    return report_found
