
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


## Application Testing

The following tests can be used to verify the main
features of Ward 42 Fix-It.

### 1. Start the Application

Install the dependencies:

    pip install -r requirements.txt

Start Flask:

    python -m flask --app app run

Open http://127.0.0.1:5000/

### 2. Resident Functionality

- Open the Report a Fault page.
- Submit a report using fictitious test information.
- Attach a JPEG, PNG or WebP photograph.
- Confirm that a unique reference number is generated.
- Use Check Status to retrieve the report status.
- Verify that an invalid cellphone number is rejected.
- Verify that photographs larger than 2 MB are rejected.

### 3. Coordinator Functionality

- Create a test coordinator using create_coordinator.py.
- Log in using the test credentials.
- Open the All Reports page.
- Test the live category and status filters.
- Update a report from Open to In progress.
- Open the Dashboard and verify the report totals.

### 4. Security Testing

The security_tests.http file contains requests for
testing application security.

Security controls include:

- Server-side input validation
- CSRF protection
- Parameterised SQL queries
- Authentication and password hashing
- Protected coordinator pages
- Photograph validation

### 5. PWA and Offline Testing

- Open the application in Google Chrome.
- Inspect the manifest in Developer Tools.
- Check the Service Worker registration.
- Inspect the application Cache Storage.
- Disable network access and verify the offline page.
- Restore the network connection.

### Offline Limitations

The PWA supports limited offline functionality.

Residents can recover previously saved text drafts.
However, submitting new reports and retrieving updated
report statuses requires an internet connection.

### Test Data and Privacy

Only fictitious personal information should be used
during testing.

Do not commit the SQLite database, uploaded photographs,
passwords or application secret keys to GitHub.


## Windows Startup Troubleshooting

During development, the standard `flask run` command
did not start the application successfully in PowerShell.

The application was successfully started using:

    python -m flask --app app run

This command runs Flask through the active Python
environment and explicitly identifies app.py as the
application entry point.

### Steps if Flask Does Not Start

1. Open the Ward42-FixIt project in VS Code.
2. Open a new PowerShell terminal.
3. Activate the virtual environment:

       .\venv\Scripts\Activate.ps1

4. Install the project dependencies:

       python -m pip install -r requirements.txt

5. Start the Flask application:

       python -m flask --app app run

6. Open the following address in Chrome:

       http://127.0.0.1:5000/

### Development Environment

The application uses Flask's development server
for local testing only.

A production deployment requires HTTPS and a
production-ready WSGI server.
