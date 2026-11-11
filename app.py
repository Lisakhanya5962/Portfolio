
from flask import (
    Flask,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    send_from_directory
)
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os
import re

# Load environment variables
load_dotenv()

app = Flask(__name__)

# ---------------- Security Configuration ----------------

app.secret_key = os.getenv("SECRET_KEY")

if not app.secret_key:
    raise RuntimeError("SECRET_KEY is missing from your .env file.")

# ---------------- Flask-Mail Configuration ----------------

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = os.getenv("EMAIL_USER")
app.config["MAIL_PASSWORD"] = os.getenv("EMAIL_PASS")
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("EMAIL_USER")

mail = Mail(app)

# ---------------- Portfolio Projects ----------------

projects = [
    {
        "name": "StayServe",
        "category": "Web Application",
        "description": (
            "A guesthouse management system designed to help "
            "accommodation businesses manage rooms and reservations."
        ),
        "technologies": ["Python", "Flask", "SQLite", "HTML", "CSS"],
        "features": [
            "Room management",
            "Room descriptions and image uploads",
            "Accommodation administration",
            "Dashboard interface"
        ],
        "status": "In Development",
        "image": "projects/stayserve.png",
        "repository": "Private repository — source code available on request"
    },
    {
        "name": "SalonSaaS",
        "category": "SaaS Platform",
        "description": (
            "A salon and barbershop management platform designed "
            "to support business owners, employees and customers."
        ),
        "technologies": ["Python", "Django", "SQLite", "HTML", "CSS"],
        "features": [
            "Business management",
            "Customer management",
            "Appointment scheduling",
            "Employee and role management"
        ],
        "status": "In Development",
        "image": "projects/salonsaas.png",
        "repository": "Private repository — source code available on request"
    },
    {
        "name": "Flask Shop Manager",
        "category": "Inventory Management",
        "description": (
            "An inventory and shop management application "
            "for managing stock, sales and user roles."
        ),
        "technologies": ["Python", "Flask", "SQLite", "HTML", "CSS"],
        "features": [
            "Inventory management",
            "Stock tracking",
            "Sales management",
            "Admin and seller dashboards"
        ],
        "status": "Project Showcase",
        "image": "projects/shop-manager.png",
        "repository": "Private repository — source code available on request"
    }
]


# ---------------- Main Routes ----------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/projects")
def projects_page():
    return render_template("projects.html", projects=projects)


# ---------------- Contact Form ----------------

@app.route("/contact", methods=["POST"])
def contact():

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()

    if not name or not email or not message:
        flash("Please complete all contact form fields.", "error")
        return redirect(url_for("index") + "#contact")

    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        flash("Please enter a valid email address.", "error")
        return redirect(url_for("index") + "#contact")

    if not os.getenv("EMAIL_USER") or not os.getenv("EMAIL_PASS"):
        flash("The contact service is temporarily unavailable.", "error")
        return redirect(url_for("index") + "#contact")

    msg = Message(
        subject=f"Portfolio enquiry from {name}",
        recipients=[os.getenv("EMAIL_USER")],
        reply_to=email
    )

    msg.body = (
        f"New portfolio contact message\n\n"
        f"Name: {name}\n"
        f"Email: {email}\n\n"
        f"Message:\n{message}"
    )

    try:
        mail.send(msg)
        flash("Thank you! Your message has been sent successfully.", "success")

    except Exception:
        app.logger.exception("Portfolio contact email failed.")
        flash(
            "Sorry, your message could not be sent. Please try again later.",
            "error"
        )

    return redirect(url_for("index") + "#contact")


# ---------------- CV Download ----------------

@app.route("/download-cv")
def download_cv():

    return send_from_directory(
        directory=os.path.join(app.root_path, "static", "files"),
        path="Lisakhanya_CV.pdf",
        as_attachment=True
    )


# ---------------- CCNA Certificate Download ----------------

@app.route("/download-ccna")
def download_ccna():

    return send_from_directory(
        directory=os.path.join(app.root_path, "static", "files"),
        path="CCNA_Certificate.pdf",
        as_attachment=True
    )


# ---------------- Run Application ----------------

if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "False").lower() == "true")
