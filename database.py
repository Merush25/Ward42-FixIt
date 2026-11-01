
# ==========================================
# WARD 42 FIX-IT
# Database Management
# ==========================================

import sqlite3
import uuid

from pathlib import Path
from contextlib import closing


# ==========================================
# DATABASE LOCATION
# ==========================================

DATABASE_PATH = (
    Path(__file__).resolve().parent
    / "instance"
    / "fixit.db"
)


# ==========================================
# CREATE DATABASE AND TABLES
# ==========================================

def create_database():

    # Create database folder if needed
    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # Connect to SQLite
    with sqlite3.connect(DATABASE_PATH) as connection:

        # ==================================
        # REPORTS TABLE
        # ==================================

        connection.execute("""
            CREATE TABLE IF NOT EXISTS reports (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                reference TEXT NOT NULL UNIQUE,

                category TEXT NOT NULL
                    CHECK (category IN (
                        'Pothole',
                        'Water leak',
                        'Streetlight',
                        'Illegal dumping',
                        'Other'
                    )),

                street TEXT NOT NULL,

                description TEXT NOT NULL
                    CHECK (
                        length(description)
                        BETWEEN 10 AND 500
                    ),

                reporter_name TEXT NOT NULL,

                reporter_cell TEXT NOT NULL,

                photo_path TEXT,

                status TEXT NOT NULL DEFAULT 'Open'
                    CHECK (status IN (
                        'Open',
                        'In progress',
                        'Closed'
                    )),

                created_at TEXT NOT NULL
                    DEFAULT CURRENT_TIMESTAMP

            )
        """)

        # ==================================
        # COORDINATORS TABLE
        # ==================================

        connection.execute("""
            CREATE TABLE IF NOT EXISTS coordinators (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                username TEXT NOT NULL UNIQUE
                    COLLATE NOCASE,

                password_hash TEXT NOT NULL,

                created_at TEXT NOT NULL
                    DEFAULT CURRENT_TIMESTAMP

            )
        """)

    print("Database tables created successfully!")


# ==========================================
# SAVE A NEW FAULT REPORT
# ==========================================

def save_report(
    category,
    street,
    description,
    reporter_name,
    reporter_cell,
    photo_path=None
):

    # Create temporary unique reference
    temporary_reference = (
        "TEMP-" + uuid.uuid4().hex
    )

    # Open database connection
    with closing(
        sqlite3.connect(DATABASE_PATH)
    ) as connection:

        # Execute changes in one transaction
        with connection:

            # Insert new report
            cursor = connection.execute("""
                INSERT INTO reports (
                    reference,
                    category,
                    street,
                    description,
                    reporter_name,
                    reporter_cell,
                    photo_path
                )

                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                temporary_reference,
                category,
                street,
                description,
                reporter_name,
                reporter_cell,
                photo_path
            ))

            # Get the new database ID
            report_id = cursor.lastrowid

            # Generate permanent reference
            reference = f"W42-{report_id:04d}"

            # Update the report reference
            connection.execute("""
                UPDATE reports
                SET reference = ?
                WHERE id = ?
            """, (
                reference,
                report_id
            ))

    # Return the generated reference
    return reference


# ==========================================
# LOOK UP REPORT STATUS
# ==========================================

def get_report_status(reference):

    # Clean reference number
    reference = reference.strip().upper()

    # Connect to database
    with closing(
        sqlite3.connect(DATABASE_PATH)
    ) as connection:

        # Retrieve reference and status only
        cursor = connection.execute("""
            SELECT reference, status
            FROM reports
            WHERE reference = ?
        """, (reference,))

        report = cursor.fetchone()

    # Return matching report
    if report:
        return {
            "reference": report[0],
            "status": report[1]
        }

    # No matching report
    return None


# ==========================================
# RUN DATABASE SETUP
# ==========================================

if __name__ == "__main__":
    create_database()
