from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = "transport_secret_key"

# =========================
# DATABASE SETUP
# =========================

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, "transport.db")

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# =========================
# MODELS
# =========================

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_no = db.Column(db.String(50), nullable=False)
    vehicle_type = db.Column(db.String(50))
    status = db.Column(db.String(50))


class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    mobile = db.Column(db.String(20))
    license_no = db.Column(db.String(50))


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    mobile = db.Column(db.String(20))
    address = db.Column(db.Text)


class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(100))
    destination = db.Column(db.String(100))
    amount = db.Column(db.Float)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    full_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    mobile = db.Column(db.String(20))
    address = db.Column(db.Text)

@app.context_processor
def inject_user():

    user = None

    if session.get("user_id"):
        user = User.query.get(session["user_id"])

    return dict(current_user=user)
# =========================
# HOME
# =========================

@app.route("/")
def home():
    return redirect(url_for("login"))

# =========================
# LOGIN
# =========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(
            username=username,
            password=password
        ).first()

        if user:

            session["user_id"] = user.id

            if not user.full_name:
                return redirect(url_for("profile"))

            return redirect(url_for("dashboard"))

        return "Invalid Username or Password"

    return render_template("login.html")

@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():

    message = ""

    if request.method == "POST":

        username = request.form.get("username")
        new_password = request.form.get("new_password")

        user = User.query.filter_by(username=username).first()

        if user:
            user.password = new_password
            db.session.commit()
            message = "Password Updated Successfully!"
        else:
            message = "Username Not Found!"

    return render_template(
        "forgot_password.html",
        message=message
    )

# =========================
# REGISTER
# =========================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        existing_user = User.query.filter_by(
            username=username
        ).first()

        if existing_user:
            return "Username already exists"

        new_user = User(
            username=username,
            password=password
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")

# =========================
# DASHBOARD
# =========================

@app.route("/dashboard")
def dashboard():

    return render_template(
        "dashboard.html",
        vehicle_count=Vehicle.query.count(),
        driver_count=Driver.query.count(),
        customer_count=Customer.query.count(),
        trip_count=Trip.query.count()
    )

# =========================
# VEHICLES
# =========================

@app.route("/vehicles")
def vehicles():
    return render_template(
        "vehicles.html",
        vehicles=Vehicle.query.all()
    )

# =========================
# DRIVERS
# =========================

@app.route("/drivers")
def drivers():
    return render_template(
        "drivers.html",
        drivers=Driver.query.all()
    )

# =========================
# CUSTOMERS
# =========================

@app.route("/customers")
def customers():
    return render_template(
        "customers.html",
        customers=Customer.query.all()
    )

# =========================
# TRIPS
# =========================

@app.route("/trips")
def trips():
    return render_template(
        "trips.html",
        trips=Trip.query.all()
    )

# =========================
# REPORTS
# =========================

@app.route("/reports")
def reports():
    return render_template("reports.html")

# =========================
# PROFILE MENU PAGES
# =========================

@app.route("/profile", methods=["GET", "POST"])
def profile():

    user = User.query.get(session.get("user_id"))

    if not user:
        return redirect(url_for("login"))

    if request.method == "POST":

        user.full_name = request.form.get("full_name")
        user.email = request.form.get("email")
        user.mobile = request.form.get("mobile")
        user.address = request.form.get("address")

        db.session.commit()

        return redirect(url_for("dashboard"))
    return render_template("profile.html", user=user)
    return render_template(
        "profile.html",
        user=user
    )

@app.route("/settings")
def settings():
    return render_template("settings.html")


@app.route("/support")
def support():
    return render_template("support.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/change-password")
def change_password():
    return render_template("change_password.html")

# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))
# =========================
# CREATE DATABASE & SAMPLE DATA
# =========================

if __name__ == "__main__":

    with app.app_context():

        db.create_all()

        # Admin User
        if User.query.count() == 0:
            db.session.add(
                User(
                    username="admin",
                    password="admin123"
                )
            )

        # Sample Vehicle
        if Vehicle.query.count() == 0:
            db.session.add(
                Vehicle(
                    vehicle_no="MH40AB1234",
                    vehicle_type="Truck",
                    status="Available"
                )
            )

        # Sample Driver
        if Driver.query.count() == 0:
            db.session.add(
                Driver(
                    name="Rahul Sharma",
                    mobile="9876543210",
                    license_no="DL12345"
                )
            )

        # Sample Customer
        if Customer.query.count() == 0:
            db.session.add(
                Customer(
                    name="ABC Traders",
                    mobile="9999999999",
                    address="Nagpur"
                )
            )

        # Sample Trip
        if Trip.query.count() == 0:
            db.session.add(
                Trip(
                    source="Nagpur",
                    destination="Pune",
                    amount=25000
                )
            )

        db.session.commit()

    app.run(debug=True)