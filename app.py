
import re
import secrets
import sqlite3

from io import BytesIO
from pathlib import Path, PurePosixPath
from datetime import timedelta
from contextlib import closing

from PIL import Image, ImageOps, UnidentifiedImageError

from flask import (
    Flask, render_template, request, redirect,
    url_for, session, flash, jsonify,
    send_from_directory, send_file, abort
)

from flask_wtf.csrf import CSRFProtect
from werkzeug.security import check_password_hash

from validators import validate_report
from database import DATABASE_PATH, save_report, get_report_status
from photo_utils import save_photo, UPLOAD_FOLDER

from report_management import (
    get_all_reports,
    get_report_by_id,
    update_report_status,
    ALLOWED_CATEGORIES,
    ALLOWED_STATUSES
)

from dashboard_data import get_dashboard_summary


# ==========================================
# FLASK APPLICATION
# ==========================================

app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = 3 * 1024 * 1024

secret_file = Path(app.instance_path) / "secret.key"
secret_file.parent.mkdir(parents=True, exist_ok=True)

if not secret_file.exists():
    secret_file.write_text(
        secrets.token_hex(32),
        encoding="utf-8"
    )

app.config["SECRET_KEY"] = secret_file.read_text(
    encoding="utf-8"
).strip()

app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

# False for local HTTP testing; True for production HTTPS.
app.config["SESSION_COOKIE_SECURE"] = False

app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(
    minutes=30
)

csrf = CSRFProtect(app)


# ==========================================
# SECURITY HEADERS
# ==========================================

@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = (
        "strict-origin-when-cross-origin"
    )
    response.headers["X-Frame-Options"] = "DENY"
    return response


# ==========================================
# SERVICE WORKER
# ==========================================

@app.route("/service-worker.js")
def service_worker():
    response = send_from_directory(
        app.static_folder,
        "service-worker.js",
        mimetype="text/javascript"
    )
    response.headers["Cache-Control"] = "no-cache"
    return response


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():
    return render_template("home.html")


# ==========================================
# CHECK REPORT STATUS
# ==========================================

@app.route("/check-status", methods=["GET", "POST"])
def check_status():
    report = None
    error = None

    if request.method == "POST":
        reference = request.form.get(
            "reference", ""
        ).strip().upper()

        if not re.fullmatch(r"W42-[0-9]{4,}", reference):
            error = (
                "Please enter a valid reference number, "
                "for example W42-0001."
            )
        else:
            report = get_report_status(reference)

            if report is None:
                error = (
                    "No report was found with that "
                    "reference number."
                )

    return render_template(
        "check_status.html",
        report=report,
        error=error
    )


# ==========================================
# REPORT A FAULT
# ==========================================

@app.route("/report", methods=["GET", "POST"])
def report_fault():
    errors = {}

    if request.method == "POST":
        errors = validate_report(request.form)

        if not errors:
            photo_path = None

            try:
                photo = request.files.get("photo")
                photo_path = save_photo(photo)

            except ValueError as error:
                errors["photo"] = str(error)

            except OSError:
                app.logger.exception("Photo upload failed")
                errors["photo"] = (
                    "The photograph could not be saved."
                )

            if not errors:
                try:
                    reference = save_report(
                        category=request.form.get(
                            "category", ""
                        ).strip(),
                        street=request.form.get(
                            "street", ""
                        ).strip(),
                        description=request.form.get(
                            "description", ""
                        ).strip(),
                        reporter_name=request.form.get(
                            "reporter_name", ""
                        ).strip(),
                        reporter_cell=request.form.get(
                            "reporter_cell", ""
                        ).strip(),
                        photo_path=photo_path
                    )

                except sqlite3.Error:
                    app.logger.exception(
                        "Database report saving failed"
                    )

                    if photo_path:
                        (
                            UPLOAD_FOLDER / Path(photo_path).name
                        ).unlink(missing_ok=True)

                    errors["form"] = (
                        "Your report could not be saved. "
                        "Please try again."
                    )

                else:
                    session["last_report_reference"] = reference

                    return redirect(
                        url_for("report_success")
                    )

        return render_template(
            "report_fault.html",
            errors=errors
        ), 400

    return render_template(
        "report_fault.html",
        errors=errors
    )


# ==========================================
# REPORT SUCCESS
# ==========================================

@app.route("/report/success")
def report_success():
    reference = session.get("last_report_reference")

    if not reference:
        return redirect(url_for("home"))

    response = app.make_response(
        render_template(
            "report_success.html",
            reference=reference
        )
    )

    response.headers["Cache-Control"] = "no-store"
    return response


# ==========================================
# COORDINATOR LOGIN
# ==========================================

@app.route("/coordinator/login", methods=["GET", "POST"])
def coordinator_login():
    if session.get("coordinator_id"):
        return redirect(url_for("coordinator_panel"))

    error = None

    if request.method == "POST":
        username = request.form.get(
            "username", ""
        ).strip()

        password = request.form.get("password", "")
        coordinator = None

        try:
            with closing(
                sqlite3.connect(DATABASE_PATH)
            ) as connection:
                coordinator = connection.execute(
                    """
                    SELECT id, username, password_hash
                    FROM coordinators
                    WHERE username = ?
                    """,
                    (username,)
                ).fetchone()

        except sqlite3.Error:
            app.logger.exception(
                "Coordinator login database error"
            )
            error = "Login is temporarily unavailable."

        if error is None:
            if coordinator and check_password_hash(
                coordinator[2],
                password
            ):
                session.clear()
                session.permanent = True

                session["coordinator_id"] = coordinator[0]
                session["coordinator_username"] = coordinator[1]

                return redirect(
                    url_for("coordinator_panel")
                )

            error = "Invalid username or password."

    response = app.make_response(
        render_template(
            "coordinator_login.html",
            error=error
        )
    )

    response.headers["Cache-Control"] = "no-store"
    return response


# ==========================================
# COORDINATOR PANEL
# ==========================================

@app.route("/coordinator")
def coordinator_panel():
    if not session.get("coordinator_id"):
        return redirect(url_for("coordinator_login"))

    response = app.make_response(
        render_template(
            "coordinator_home.html",
            username=session["coordinator_username"]
        )
    )

    response.headers["Cache-Control"] = "no-store"
    return response


# ==========================================
# ALL REPORTS
# ==========================================

@app.route("/coordinator/reports")
def all_reports():
    if not session.get("coordinator_id"):
        return redirect(url_for("coordinator_login"))

    category = request.args.get("category", "").strip()
    status = request.args.get("status", "").strip()

    if category not in ALLOWED_CATEGORIES:
        category = ""

    if status not in ALLOWED_STATUSES:
        status = ""

    reports = get_all_reports(
        category=category,
        status=status
    )

    response = app.make_response(
        render_template(
            "all_reports.html",
            reports=reports,
            categories=sorted(ALLOWED_CATEGORIES),
            statuses=["Open", "In progress", "Closed"],
            selected_category=category,
            selected_status=status
        )
    )

    response.headers["Cache-Control"] = "no-store"
    return response


# ==========================================
# PROTECTED REPORT AND PHOTO HELPERS
# ==========================================

def require_report_for_coordinator(report_id):
    if not session.get("coordinator_id"):
        abort(401)

    report = get_report_by_id(report_id)

    if report is None:
        abort(404)

    return report


def safe_photo_filename(report):
    stored_path = report.get("photo_path")

    if not stored_path:
        abort(404)

    parts = PurePosixPath(
        stored_path.replace("\\", "/")
    ).parts

    if len(parts) != 2 or parts[0] != "uploads":
        abort(404)

    filename = parts[1]

    if filename in (".", "..") or not filename:
        abort(404)

    photo_file = UPLOAD_FOLDER / filename

    if not photo_file.is_file():
        abort(404)

    return filename


# ==========================================
# REPORT DETAIL PAGE
# ==========================================

@app.route("/coordinator/reports/<int:report_id>/detail")
def report_detail(report_id):
    if not session.get("coordinator_id"):
        return redirect(url_for("coordinator_login"))

    report = get_report_by_id(report_id)

    if report is None:
        abort(404)

    response = app.make_response(
        render_template(
            "report_detail.html",
            report=report
        )
    )

    response.headers["Cache-Control"] = "no-store"
    return response


# ==========================================
# FULL PHOTOGRAPH
# ==========================================

@app.route("/coordinator/reports/<int:report_id>/photo")
def coordinator_report_photo(report_id):
    report = require_report_for_coordinator(report_id)
    filename = safe_photo_filename(report)

    response = send_from_directory(
        str(UPLOAD_FOLDER),
        filename,
        as_attachment=False
    )

    response.headers["Cache-Control"] = "no-store"
    return response


# ==========================================
# PHOTOGRAPH THUMBNAIL
# ==========================================

@app.route("/coordinator/reports/<int:report_id>/thumbnail")
def coordinator_report_thumbnail(report_id):
    report = require_report_for_coordinator(report_id)
    filename = safe_photo_filename(report)

    try:
        with Image.open(UPLOAD_FOLDER / filename) as raw_image:
            image = ImageOps.exif_transpose(raw_image)
            image.thumbnail(
                (180, 140),
                Image.Resampling.LANCZOS
            )

            if image.mode != "RGB":
                image = image.convert("RGB")

            data = BytesIO()

            image.save(
                data,
                format="JPEG",
                quality=70,
                optimize=True
            )

            data.seek(0)

    except (OSError, ValueError, UnidentifiedImageError):
        app.logger.exception(
            "Unable to produce report thumbnail"
        )
        abort(404)

    response = send_file(
        data,
        mimetype="image/jpeg"
    )

    response.headers["Cache-Control"] = "private, no-store"
    return response


# ==========================================
# UPDATE REPORT STATUS
# ==========================================

@app.route(
    "/coordinator/reports/<int:report_id>/status",
    methods=["POST"]
)
def update_status(report_id):
    if not session.get("coordinator_id"):
        return redirect(url_for("coordinator_login"))

    new_status = request.form.get(
        "status", ""
    ).strip()

    if new_status not in ALLOWED_STATUSES:
        flash("Invalid report status selected.", "danger")
        return redirect(url_for("all_reports"))

    try:
        report_found = update_report_status(
            report_id,
            new_status
        )

    except (ValueError, sqlite3.Error):
        app.logger.exception(
            "Report status update failed"
        )

        flash(
            "The report status could not be updated.",
            "danger"
        )

        return redirect(url_for("all_reports"))

    if report_found:
        flash(
            "Report status updated successfully!",
            "success"
        )
    else:
        flash(
            "The selected report could not be found.",
            "warning"
        )

    return redirect(url_for("all_reports"))


# ==========================================
# COORDINATOR DASHBOARD
# ==========================================

@app.route("/coordinator/dashboard")
def coordinator_dashboard():
    if not session.get("coordinator_id"):
        return redirect(url_for("coordinator_login"))

    summary = get_dashboard_summary()

    response = app.make_response(
        render_template(
            "dashboard.html",
            summary=summary
        )
    )

    response.headers["Cache-Control"] = "no-store"
    return response


# ==========================================
# JSON API
# ==========================================

@app.route("/api/reports/summary", methods=["GET"])
def reports_summary_api():
    if not session.get("coordinator_id"):
        response = jsonify({
            "error": "Authentication required"
        })
        response.status_code = 401
    else:
        summary = get_dashboard_summary()
        response = jsonify(summary)

    response.headers["Cache-Control"] = "no-store"
    return response


# ==========================================
# COORDINATOR LOGOUT
# ==========================================

@app.route("/coordinator/logout", methods=["POST"])
def coordinator_logout():
    session.clear()
    return redirect(url_for("coordinator_login"))


# ==========================================
# OVERSIZED FILE ERROR HANDLING
# ==========================================

@app.errorhandler(413)
def file_too_large(error):
    return (
        "The upload is too large. "
        "Please use a photograph no larger than 2 MB. "
        "Return to the Report a Fault page and try again.",
        413
    )


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":
    app.run()
