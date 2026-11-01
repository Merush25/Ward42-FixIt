
# Ward 42 Fix-It

## Project Overview

Ward 42 Fix-It is a community service-reporting web application developed for the Mamelodi East Residents' Association in Tshwane.

The application allows residents to report municipal service problems and track their progress using a unique reference number.

## Main Features

- Submit municipal service reports
- Upload photographs of reported problems
- Track reports using reference numbers
- Secure coordinator login
- View and filter submitted reports
- Update report statuses
- Dashboard showing report statistics
- Responsive design for mobile and desktop
- Progressive Web App (PWA) functionality
- Custom offline page
- Tutorial video with caption support
- JSON API for dashboard statistics

## Technologies Used

- Python
- Flask
- SQLite
- HTML5
- CSS3
- Bootstrap 5
- JavaScript
- Flask-WTF
- Progressive Web App technologies

## Installation

1. Download or clone the repository.
2. Open the project folder in VS Code.
3. Open a terminal.
4. Create a Python virtual environment:

   python -m venv venv

5. Activate the virtual environment on Windows:

   .\venv\Scripts\Activate.ps1

6. Install the required packages:

   pip install -r requirements.txt

7. Create a test coordinator account:

   python create_coordinator.py

8. Start the application:

   flask run

9. Open the application in a browser:

   http://127.0.0.1:5000

## Test Coordinator Login

Run the following command to create a test coordinator:

python create_coordinator.py

Enter a test username and a password containing at least 12 characters.

The password is stored as a secure hash.

## Application Pages

- Home
- Report a Fault
- Check Status
- Coordinator Login
- Coordinator Panel
- All Reports
- Report Details
- Dashboard

## Security Features

- Password hashing
- CSRF protection
- Server-side input validation
- Parameterised SQL queries
- Secure photo upload validation
- Session-based authentication
- Security response headers

## Privacy

The application was developed using fictitious test information.

Database records, uploaded photographs, virtual environments and secret keys are excluded from the GitHub repository.

## Academic Project

Module: WST262 - Web Systems and Technologies

Assignment: Summative Project (SS3)

Institution: STADIO

Project: Ward 42 Fix-It
