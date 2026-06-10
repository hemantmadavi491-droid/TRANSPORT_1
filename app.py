from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# =========================
# DATABASE SETUP
# =========================

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# database file (safe path)
db_path = os.path.join(BASE_DIR, "transport.db")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path
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

# =========================
# LOGIN SYSTEM
# =========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "admin123":
            return redirect(url_for("dashboard"))

        return "Invalid Login"

    return render_template("login.html")

# =========================
# HOME -> LOGIN
# =========================

@app.route("/")
def home():
    return redirect(url_for("login"))

# =========================
# DASHBOARD
# =========================

@app.route("/dashboard")
def dashboard():

    vehicle_count = Vehicle.query.count()
    driver_count = Driver.query.count()
    customer_count = Customer.query.count()
    trip_count = Trip.query.count()

    return render_template(
        "dashboard.html",
        vehicle_count=vehicle_count,
        driver_count=driver_count,
        customer_count=customer_count,
        trip_count=trip_count
    )

# =========================
# VEHICLES
# =========================

@app.route("/vehicles")
def vehicles():
    data = Vehicle.query.all()
    return render_template("vehicles.html", vehicles=data)

# =========================
# DRIVERS
# =========================

@app.route("/drivers")
def drivers():
    data = Driver.query.all()
    return render_template("drivers.html", drivers=data)

# =========================
# CUSTOMERS
# =========================

@app.route("/customers")
def customers():
    data = Customer.query.all()
    return render_template("customers.html", customers=data)

# =========================
# TRIPS
# =========================

@app.route("/trips")
def trips():
    data = Trip.query.all()
    return render_template("trips.html", trips=data)

# =========================
# REPORTS
# =========================

@app.route("/reports")
def reports():
    return render_template("reports.html")

# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():
    return redirect(url_for("login"))

# =========================
# CREATE DB + SAMPLE DATA
# =========================

if __name__ == "__main__":

    with app.app_context():
        db.create_all()

        # Sample Vehicles
        if Vehicle.query.count() == 0:
            db.session.add_all([
                Vehicle(vehicle_no="MH40AB1234", vehicle_type="Truck", status="Available"),
                Vehicle(vehicle_no="MH31XY5678", vehicle_type="Container", status="On Trip")
            ])

        # Sample Drivers
        if Driver.query.count() == 0:
            db.session.add_all([
                Driver(name="Rahul Sharma", mobile="9876543210", license_no="DL12345"),
                Driver(name="Amit Patil", mobile="9876500000", license_no="DL67890")
            ])

        # Sample Customers
        if Customer.query.count() == 0:
            db.session.add(
                Customer(name="ABC Traders", mobile="9999999999", address="Nagpur")
            )

        # Sample Trips
        if Trip.query.count() == 0:
            db.session.add(
                Trip(source="Nagpur", destination="Pune", amount=25000)
            )

        db.session.commit()

    app.run(debug=True)