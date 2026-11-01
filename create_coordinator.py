
# ==========================================
# WARD 42 FIX-IT
# Create Coordinator Account
# ==========================================

import re
import sqlite3

from getpass import getpass
from werkzeug.security import generate_password_hash

from database import DATABASE_PATH, create_database


# ==========================================
# CREATE COORDINATOR
# ==========================================

def create_coordinator():

    # Ensure the database tables exist
    create_database()

    print("\nWARD 42 FIX-IT")
    print("Create Coordinator Account")
    print("--------------------------")

    # Ask for a username
    username = input(
        "Enter coordinator username: "
    ).strip()

    # Validate the username
    if not re.fullmatch(
        r"[A-Za-z0-9_.-]{3,30}",
        username
    ):
        print(
            "Username must contain 3 to 30 characters. "
            "Use letters, numbers, dots, "
            "underscores or hyphens."
        )
        return

    # Ask for a password without displaying it
    password = getpass(
        "Enter coordinator password: "
    )

    # Require a sufficiently long password
    if len(password) < 12:
        print(
            "Password must contain at least "
            "12 characters."
        )
        return

    # Ask the user to confirm the password
    confirm_password = getpass(
        "Confirm coordinator password: "
    )

    if password != confirm_password:
        print("Passwords do not match.")
        return

    # Securely hash the password
    password_hash = generate_password_hash(
        password,
        method="scrypt"
    )

    # Save the coordinator account
    try:
        with sqlite3.connect(DATABASE_PATH) as connection:

            connection.execute("""
                INSERT INTO coordinators (
                    username,
                    password_hash
                )
                VALUES (?, ?)
            """, (
                username,
                password_hash
            ))

    except sqlite3.IntegrityError:
        print(
            "This username already exists. "
            "Please choose another."
        )
        return

    print("\nCoordinator account created successfully!")
    print("Username:", username)
    print("Password stored securely as a hash.")


# ==========================================
# RUN ACCOUNT SETUP
# ==========================================

if __name__ == "__main__":
    create_coordinator()
