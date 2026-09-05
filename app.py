from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from database import init_db, get_db_connection
# pyrefly: ignore [missing-import]
from dao.user_dao import UserDAO
# pyrefly: ignore [missing-import]
from dao.customer_dao import CustomerDAO
# pyrefly: ignore [missing-import]
from dao.vehicle_dao import VehicleDAO
# pyrefly: ignore [missing-import]
from dao.policy_dao import PolicyDAO
# pyrefly: ignore [missing-import]
from dao.claim_dao import ClaimDAO
# pyrefly: ignore [missing-import]
from model.user import User
# pyrefly: ignore [missing-import]
from model.customer import Customer
# pyrefly: ignore [missing-import]
from model.vehicle import Vehicle
# pyrefly: ignore [missing-import]
from model.policy import Policy
# pyrefly: ignore [missing-import]
from model.claim import Claim

app = Flask(__name__)
app.secret_key = "replace_this_with_a_secure_random_value"

init_db()
user_dao = UserDAO()
customer_dao = CustomerDAO()
vehicle_dao = VehicleDAO()
policy_dao = PolicyDAO()
claim_dao = ClaimDAO()

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if len(username) < 3:
            flash("Username must be at least 3 characters.", "error")
            return redirect(url_for("login"))

        if not email.endswith("@gmail.com") or "@gmail.com" not in email:
            flash("Please enter a valid Gmail address.", "error")
            return redirect(url_for("login"))

        if len(password) < 6:
            flash("Password must be at least 6 characters.", "error")
            return redirect(url_for("login"))

        existing_user = user_dao.find_by_email(email)
        if existing_user:
            if existing_user.password != password:
                flash("Invalid Password", "error")
                return redirect(url_for("login"))
            user = existing_user
        else:
            user = User(username=username, email=email, password=password)
            user_dao.create_user(user)

        session["user_id"] = user.id
        session["username"] = user.username
        session["email"] = user.email
        return redirect(url_for("dashboard"))

    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if len(username) < 3:
            flash("Full name must be at least 3 characters.", "error")
            return redirect(url_for("register"))

        if not email.endswith("@gmail.com") or "@gmail.com" not in email:
            flash("Please enter a valid Gmail address.", "error")
            return redirect(url_for("register"))

        if len(password) < 6:
            flash("Password must be at least 6 characters.", "error")
            return redirect(url_for("register"))

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for("register"))

        existing_user = user_dao.find_by_email(email)
        if existing_user:
            flash("An account already exists with that email.", "error")
            return redirect(url_for("register"))

        user = User(username=username, email=email, password=password)
        user_dao.create_user(user)
        session["user_id"] = user.id
        session["username"] = user.username
        session["email"] = user.email
        return redirect(url_for("dashboard"))

    return render_template("register.html")

from datetime import date, datetime

UPLOAD_FOLDER = BASE_DIR / "static" / "uploads"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

ALLOWED_UPLOAD_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "pdf"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_UPLOAD_EXTENSIONS


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    today = date.today().strftime("%A, %B %d, %Y")
    customers = customer_dao.get_all_customers()
    vehicles = vehicle_dao.get_all_vehicles()
    policies = policy_dao.get_all_policies()
    claims = claim_dao.get_all_claims()

    total_customers = len(customers)
    total_vehicles = len(vehicles)
    active_policies = sum(1 for p in policies if (p.status or "").strip().lower() == "active")
    pending_claims = sum(1 for c in claims if (c.status or "").strip().lower() == "pending")

    return render_template(
        "dashboard.html",
        username=session.get("username"),
        today=today,
        customers=customers,
        total_customers=total_customers,
        total_vehicles=total_vehicles,
        active_policies=active_policies,
        pending_claims=pending_claims,
    )


@app.route("/reports")
def reports():
    if "user_id" not in session:
        return redirect(url_for("login"))

    customers = customer_dao.get_all_customers()
    vehicles = vehicle_dao.get_all_vehicles()
    policies = policy_dao.get_all_policies()
    claims = claim_dao.get_all_claims()

    total_premium = 0.0
    for p in policies:
        try:
            total_premium += float(p.premium)
        except (ValueError, TypeError):
            continue

    return render_template(
        "reports.html",
        username=session.get("username"),
        customer_count=len(customers),
        vehicle_count=len(vehicles),
        policy_count=len(policies),
        claim_count=len(claims),
        total_premium=total_premium,
        recent_claims=claims[:5],
    )


@app.route("/customers")
def customers():
    if "user_id" not in session:
        return redirect(url_for("login"))

    q = request.args.get("q", "").strip().lower()
    all_customers = customer_dao.get_all_customers()
    all_vehicles = vehicle_dao.get_all_vehicles()
    vehicle_counts = {}
    for v in all_vehicles:
        vehicle_counts[v.customer_id] = vehicle_counts.get(v.customer_id, 0) + 1

    if q:
        filtered = [
            c for c in all_customers
            if q in (c.name or "").lower()
            or q in (c.customer_id or "").lower()
            or q in (c.email or "").lower()
        ]
    else:
        filtered = all_customers

    return render_template(
        "customers.html",
        username=session.get("username"),
        customers=filtered,
        query=q,
        vehicle_counts=vehicle_counts,
    )


@app.route("/customers/<customer_id>")
def view_customer(customer_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    customer = customer_dao.find_by_customer_id(customer_id)
    if not customer:
        flash("Customer not found.", "error")
        return redirect(url_for("dashboard"))

    # find related policies for this customer
    policies = [p for p in policy_dao.get_all_policies() if p.customer_id == customer.customer_id]

    return render_template("view_customer.html", username=session.get("username"), customer=customer, policies=policies)

@app.route("/policies/add", methods=["GET", "POST"])
def add_policy():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        policy = Policy(
            policy_id=request.form.get("policy_id", "").strip(),
            customer_id=request.form.get("customer_id", "").strip(),
            vehicle_id=request.form.get("vehicle_id", "").strip(),
            policy_type=request.form.get("policy_type", "").strip(),
            premium=request.form.get("premium", "").strip(),
            start_date=request.form.get("start_date", "").strip(),
            end_date=request.form.get("end_date", "").strip(),
            coverage=request.form.get("coverage", "").strip(),
            status=request.form.get("status", "").strip(),
        )

        if not all([
            policy.policy_id,
            policy.customer_id,
            policy.vehicle_id,
            policy.policy_type,
            policy.premium,
            policy.start_date,
            policy.end_date,
            policy.coverage,
            policy.status,
        ]):
            flash("Please fill in all policy fields.", "error")
            return redirect(url_for("add_policy"))

        if policy_dao.create_policy(policy):
            flash("Policy added successfully.", "success")
        else:
            flash("Policy ID already exists.", "error")
        return redirect(url_for("dashboard"))

    return render_template("add_policy.html", username=session.get("username"))

@app.route("/policies")
def policies():
    if "user_id" not in session:
        return redirect(url_for("login"))

    q = request.args.get("q", "").strip().lower()
    status_filter = request.args.get("status", "").strip().lower()
    all_policies = policy_dao.get_all_policies()
    if q:
        filtered = [
            p for p in all_policies
            if q in (p.policy_id or "").lower()
            or q in (p.customer_id or "").lower()
            or q in (p.vehicle_id or "").lower()
            or q in (p.policy_type or "").lower()
        ]
    else:
        filtered = all_policies

    if status_filter:
        filtered = [
            p for p in filtered
            if (p.status or "").strip().lower() == status_filter
        ]

    return render_template(
        "policies.html",
        username=session.get("username"),
        policies=filtered,
        query=q,
        status_filter=status_filter,
    )

@app.route("/payments")
def payments():
    if "user_id" not in session:
        return redirect(url_for("login"))

    q = request.args.get("q", "").strip().lower()
    all_policies = policy_dao.get_all_policies()
    payments = [
        {
            "policy_id": p.policy_id,
            "customer_id": p.customer_id,
            "vehicle_id": p.vehicle_id,
            "amount": p.premium,
            "due_date": p.end_date,
            "payment_date": p.start_date,
            "status": "Paid" if p.status.lower() != "active" else "Due",
            "method": "Online",
        }
        for p in all_policies
    ]

    if q:
        payments = [
            p for p in payments
            if q in p["policy_id"].lower()
            or q in p["customer_id"].lower()
            or q in p["vehicle_id"].lower()
            or q in p["status"].lower()
        ]

    pending_count = sum(1 for p in payments if p["status"].lower() == "due")
    completed_count = sum(1 for p in payments if p["status"].lower() != "due")
    total_revenue = 0.0
    for p in payments:
        try:
            total_revenue += float(p["amount"])
        except (ValueError, TypeError):
            continue

    return render_template(
        "payments.html",
        username=session.get("username"),
        payments=payments,
        query=q,
        pending_count=pending_count,
        completed_count=completed_count,
        total_revenue=total_revenue,
    )

@app.route("/policies/<policy_id>")
def view_policy(policy_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    policy = policy_dao.find_by_policy_id(policy_id)
    if not policy:
        flash("Policy not found.", "error")
        return redirect(url_for("policies"))

    customer = customer_dao.find_by_customer_id(policy.customer_id)
    vehicle = vehicle_dao.find_by_vehicle_id(policy.vehicle_id)
    claims = [c for c in claim_dao.get_all_claims() if c.policy_id == policy.policy_id]

    return render_template(
        "view_policy.html",
        username=session.get("username"),
        policy=policy,
        customer=customer,
        vehicle=vehicle,
        claims=claims,
    )

@app.route("/claims/view")
def view_claims():
    if "user_id" not in session:
        return redirect(url_for("login"))

    claims = claim_dao.get_all_claims()
    pending_count = sum(1 for c in claims if (c.status or "").strip().lower() == "pending")
    approved_count = sum(1 for c in claims if (c.status or "").strip().lower() == "approved")
    rejected_count = sum(1 for c in claims if (c.status or "").strip().lower() == "rejected")

    return render_template(
        "view_claims.html",
        username=session.get("username"),
        claims=claims,
        pending_count=pending_count,
        approved_count=approved_count,
        rejected_count=rejected_count,
    )

@app.route("/claims/add", methods=["GET", "POST"])
def add_claim():
    if "user_id" not in session:
        return redirect(url_for("login"))

    policies = policy_dao.get_all_policies()
    if request.method == "POST":
        claim_id = request.form.get("claim_id", "").strip()
        if not claim_id:
            existing_claims = claim_dao.get_all_claims()
            next_num = 1001 + len(existing_claims)
            claim_id = f"CLM{next_num}"

        claim_date = request.form.get("claim_date", "").strip()
        if not claim_date:
            claim_date = date.today().strftime("%Y-%m-%d")

        accident_date = request.form.get("accident_date", "").strip() or request.form.get("incident_date", "").strip()
        insurance_company = request.form.get("insurance_company", "").strip() or "Standard Insurance Co."
        status = request.form.get("status", "").strip() or "Pending"

        claim = Claim(
            claim_id=claim_id,
            policy_id=request.form.get("policy_id", "").strip(),
            customer_name=request.form.get("customer_name", "").strip(),
            vehicle_number=request.form.get("vehicle_number", "").strip(),
            insurance_company=insurance_company,
            accident_date=accident_date,
            incident_location=request.form.get("incident_location", "").strip(),
            claim_date=claim_date,
            claim_amount=request.form.get("claim_amount", "").strip(),
            reason=request.form.get("claim_type", "").strip() or request.form.get("reason", "").strip(),
            description=request.form.get("description", "").strip(),
            status=status,
            documents="",
        )

        if not all([
            claim.policy_id,
            claim.customer_name,
            claim.vehicle_number,
            claim.accident_date,
            claim.claim_amount,
            claim.reason,
            claim.description,
        ]):
            flash("Please fill in all required claim fields.", "error")
            return redirect(url_for("add_claim"))

        uploaded_files = []
        claim_folder = UPLOAD_FOLDER / claim.claim_id
        claim_folder.mkdir(parents=True, exist_ok=True)

        for file in request.files.getlist("documents"):
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                target_path = claim_folder / filename
                file.save(target_path)
                uploaded_files.append(str(target_path.relative_to(BASE_DIR)))

        claim.documents = ",".join(uploaded_files)

        if claim_dao.create_claim(claim):
            flash(f"Claim {claim.claim_id} submitted successfully.", "success")
            return redirect(url_for("view_claims"))
        else:
            flash(f"Claim ID '{claim.claim_id}' already exists.", "error")
            return redirect(url_for("add_claim"))

    today_str = date.today().strftime("%Y-%m-%d")
    return render_template("add_claim.html", username=session.get("username"), policies=policies, today_str=today_str)

@app.route("/vehicles/add", methods=["GET", "POST"])
def add_vehicle():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        vehicle = Vehicle(
            vehicle_id=request.form.get("vehicle_id", "").strip(),
            customer_id=request.form.get("customer_id", "").strip(),
            vehicle_number=request.form.get("vehicle_number", "").strip(),
            brand=request.form.get("brand", "").strip(),
            model=request.form.get("model", "").strip(),
            year=request.form.get("year", "").strip(),
            engine_no=request.form.get("engine_no", "").strip(),
            chassis_no=request.form.get("chassis_no", "").strip(),
        )

        if not all([
            vehicle.vehicle_id,
            vehicle.customer_id,
            vehicle.vehicle_number,
            vehicle.brand,
            vehicle.model,
            vehicle.year,
            vehicle.engine_no,
            vehicle.chassis_no,
        ]):
            flash("Please fill in all vehicle fields.", "error")
            return redirect(url_for("add_vehicle"))

        if vehicle_dao.create_vehicle(vehicle):
            flash("Vehicle added successfully.", "success")
        else:
            flash("Vehicle ID already exists.", "error")
        return redirect(url_for("dashboard"))

    return render_template("add_vehicle.html", username=session.get("username"))

@app.route("/vehicles")
def vehicles():
    if "user_id" not in session:
        return redirect(url_for("login"))

    q = request.args.get("q", "").strip().lower()
    all_vehicles = vehicle_dao.get_all_vehicles()
    if q:
        filtered = [
            v for v in all_vehicles
            if q in (v.vehicle_id or "").lower()
            or q in (v.vehicle_number or "").lower()
            or q in (v.brand or "").lower()
            or q in (v.model or "").lower()
            or q in (v.customer_id or "").lower()
        ]
    else:
        filtered = all_vehicles

    return render_template("vehicles.html", username=session.get("username"), vehicles=filtered, query=q)

@app.route("/vehicles/<vehicle_id>")
def view_vehicle(vehicle_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    vehicle = vehicle_dao.find_by_vehicle_id(vehicle_id)
    if not vehicle:
        flash("Vehicle not found.", "error")
        return redirect(url_for("vehicles"))

    customer = None
    if vehicle.customer_id:
        customer = customer_dao.find_by_customer_id(vehicle.customer_id)

    policies = [p for p in policy_dao.get_all_policies() if p.vehicle_id == vehicle.vehicle_id]

    return render_template(
        "view_vehicle.html",
        username=session.get("username"),
        vehicle=vehicle,
        customer=customer,
        policies=policies,
    )

@app.route("/customers/add", methods=["GET", "POST"])
def add_customer():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        customer = Customer(
            customer_id=request.form.get("customer_id", "").strip(),
            name=request.form.get("name", "").strip(),
            email=request.form.get("email", "").strip(),
            phone=request.form.get("phone", "").strip(),
            address=request.form.get("address", "").strip(),
            dob=request.form.get("dob", "").strip(),
            license_no=request.form.get("license_no", "").strip(),
        )

        if not all([customer.customer_id, customer.name, customer.email, customer.phone, customer.address, customer.dob, customer.license_no]):
            flash("Please fill in all customer fields.", "error")
            return redirect(url_for("add_customer"))

        if customer_dao.create_customer(customer):
            flash("Customer added successfully.", "success")
            return redirect(url_for("customers"))
        else:
            flash("Customer ID already exists.", "error")
            return redirect(url_for("add_customer"))

    return render_template("add_customer.html", username=session.get("username"))

@app.route("/settings")
def settings():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("settings.html", username=session.get("username"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

