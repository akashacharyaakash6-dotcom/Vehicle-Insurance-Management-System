from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import sys
import random
from pathlib import Path
from datetime import date, datetime

BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from database import init_db, get_db_connection
from src.dao.user_dao import UserDAO
from src.dao.customer_dao import CustomerDAO
from src.dao.vehicle_dao import VehicleDAO
from src.dao.policy_dao import PolicyDAO
from src.dao.claim_dao import ClaimDAO
from src.dao.payment_dao import PaymentDAO
from src.model.user import User
from src.model.customer import Customer
from src.model.vehicle import Vehicle
from src.model.policy import Policy
from src.model.claim import Claim
from src.model.payment import Payment
from src.rbac import is_allowed

app = Flask(__name__)
app.secret_key = "vehicle_insurance_management_secret_key"

init_db()
user_dao = UserDAO()
customer_dao = CustomerDAO()
vehicle_dao = VehicleDAO()
policy_dao = PolicyDAO()
claim_dao = ClaimDAO()
payment_dao = PaymentDAO()


@app.before_request
def enforce_rbac():
    path = request.path
    is_rbac_route = (
        path == "/customer" or path.startswith("/customer/") or
        path == "/agent" or path.startswith("/agent/") or
        path == "/admin" or path.startswith("/admin/")
    )
    if is_rbac_route:
        role = session.get("role", "")
        username = session.get("username", "")
        if not is_allowed(role, username, path):
            flash("Access Denied: You do not have permission to access this resource.", "error")
            return redirect(url_for("dashboard"))




def generate_user_id():
    conn = get_db_connection()
    count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    conn.close()
    return f"USR{1001 + count}"


import re
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


def is_valid_email(email: str) -> bool:
    return bool(EMAIL_REGEX.match(email.strip()))


def get_active_portal():
    return session.get("active_portal", session.get("role", "customer"))


@app.context_processor
def inject_portal_context():
    return {
        "active_portal": get_active_portal(),
        "user_role": session.get("role", "customer"),
        "user_id": session.get("user_id", ""),
    }


@app.route("/switch-portal/<portal_type>")
def switch_portal(portal_type):
    if portal_type in ["agent", "customer"]:
        session["active_portal"] = portal_type
        flash(f"Switched to {portal_type.title()} Portal View.", "success")
    return redirect(url_for("dashboard"))


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        selected_role = request.form.get("role", "customer").strip().lower()

        if len(username) < 3:
            flash("Username must be at least 3 characters.", "error")
            return redirect(url_for("login"))

        if not is_valid_email(email):
            flash("Please enter a valid email address.", "error")
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
            user_id = generate_user_id()
            user = User(user_id=user_id, username=username, email=email, password=password, role=selected_role)
            user_dao.create_user(user)

        user_id_val = user.user_id or f"USR{user.id}"
        session["user_id"] = user_id_val
        session["username"] = user.username
        session["email"] = user.email
        session["mobile"] = user.mobile or ""
        session["address"] = user.address or ""
        session["role"] = user.role or selected_role or "customer"
        session["active_portal"] = session["role"]
        return redirect(url_for("dashboard"))

    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip()
        mobile = request.form.get("mobile", "").strip()
        address = request.form.get("address", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        role = request.form.get("role", "customer").strip().lower()

        if len(username) < 3:
            flash("Full name must be at least 3 characters.", "error")
            return redirect(url_for("register"))

        if not is_valid_email(email):
            flash("Please enter a valid email address.", "error")
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

        user_id = generate_user_id()
        user = User(user_id=user_id, username=username, email=email, mobile=mobile, address=address, password=password, role=role)
        user_dao.create_user(user)

        if role == "customer":
            customer_dao.create_customer(
                Customer(
                    customer_id=user_id,
                    name=username,
                    email=email,
                    phone=mobile or "N/A",
                    address=address or "N/A",
                    dob="1995-01-01",
                    license_no=f"DL-{user_id}",
                )
            )

        session["user_id"] = user_id
        session["username"] = user.username
        session["email"] = user.email
        session["mobile"] = user.mobile
        session["address"] = user.address
        session["role"] = user.role
        session["active_portal"] = role
        return redirect(url_for("dashboard"))

    return render_template("register.html")


UPLOAD_FOLDER = BASE_DIR / "static" / "uploads"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
ALLOWED_UPLOAD_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "pdf"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_UPLOAD_EXTENSIONS


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session.get("user_id")
    portal = get_active_portal()
    today = date.today().strftime("%A, %B %d, %Y")

    if portal == "agent":
        all_customers = customer_dao.get_all_customers()
        all_vehicles = vehicle_dao.get_all_vehicles()
        all_policies = policy_dao.get_all_policies()
        all_claims = claim_dao.get_all_claims()
        all_payments = payment_dao.get_all_payments()

        total_revenue = 0.0
        for p in all_payments:
            if (p.status or "").strip().lower() == "paid":
                try:
                    total_revenue += float(p.amount)
                except (ValueError, TypeError):
                    continue

        active_policies = sum(1 for p in all_policies if (p.status or "").strip().lower() == "active")
        pending_claims = sum(1 for c in all_claims if (c.status or "").strip().lower() == "pending")

        return render_template(
            "agent_dashboard.html",
            username=session.get("username"),
            today=today,
            total_customers=len(all_customers),
            total_vehicles=len(all_vehicles),
            total_policies=len(all_policies),
            active_policies=active_policies,
            pending_claims=pending_claims,
            total_revenue=total_revenue,
            recent_claims=all_claims[:5],
            recent_customers=all_customers[:5],
            recent_policies=all_policies[:5],
        )
    else:
        my_vehicles = vehicle_dao.get_vehicles_by_user_id(user_id)
        my_policies = policy_dao.get_policies_by_user_id(user_id)
        my_claims = claim_dao.get_claims_by_user_id(user_id)
        my_payments = payment_dao.get_payments_by_user_id(user_id)

        active_policies = sum(1 for p in my_policies if (p.status or "").strip().lower() == "active")
        pending_claims = sum(1 for c in my_claims if (c.status or "").strip().lower() == "pending")

        # Determine pending payments/dues for this customer
        paid_policy_ids = {p.policy_id for p in my_payments if (p.status or "").lower() == "paid"}
        due_policies = [p for p in my_policies if p.policy_id not in paid_policy_ids]

        return render_template(
            "customer_dashboard.html",
            username=session.get("username"),
            user_id=user_id,
            today=today,
            vehicles=my_vehicles,
            policies=my_policies,
            claims=my_claims,
            payments=my_payments,
            due_policies=due_policies,
            total_vehicles=len(my_vehicles),
            active_policies=active_policies,
            pending_claims=pending_claims,
        )



@app.route("/reports")
def reports():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session.get("user_id")
    vehicles = vehicle_dao.get_vehicles_by_user_id(user_id)
    policies = policy_dao.get_policies_by_user_id(user_id)
    claims = claim_dao.get_claims_by_user_id(user_id)
    payments = payment_dao.get_payments_by_user_id(user_id)

    total_premium = 0.0
    for p in policies:
        try:
            total_premium += float(p.premium)
        except (ValueError, TypeError):
            continue

    return render_template(
        "reports.html",
        username=session.get("username"),
        customer_count=1,
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
            c
            for c in all_customers
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

    policies = [p for p in policy_dao.get_all_policies() if p.customer_id == customer.customer_id]

    return render_template("view_customer.html", username=session.get("username"), customer=customer, policies=policies)


@app.route("/policies/apply", methods=["GET", "POST"])
def apply_policy():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session.get("user_id")
    user_vehicles = vehicle_dao.get_vehicles_by_user_id(user_id)

    if request.method == "POST":
        vehicle_id = request.form.get("vehicle_id", "").strip()
        policy_type = request.form.get("policy_type", "Comprehensive").strip()
        coverage = request.form.get("coverage", "Full Body & Engine Protection").strip()

        premium_map = {
            "Comprehensive": "7500",
            "Third Party": "3200",
            "Zero Depreciation": "9800",
            "Commercial Vehicle": "12500",
        }
        premium = premium_map.get(policy_type, "5000")

        pol_id = f"POL{random.randint(1000, 9999)}"
        pol_num = f"POL-NO-{random.randint(10000, 99999)}"
        today_str = date.today().strftime("%Y-%m-%d")
        next_year_str = (date.today().replace(year=date.today().year + 1)).strftime("%Y-%m-%d")

        policy = Policy(
            policy_id=pol_id,
            policy_number=pol_num,
            customer_id=user_id,
            vehicle_id=vehicle_id,
            policy_type=policy_type,
            premium=premium,
            start_date=today_str,
            end_date=next_year_str,
            expiry_date=next_year_str,
            coverage=coverage,
            status="Active",
        )

        if not vehicle_id:
            flash("Please select a registered vehicle for insurance coverage.", "error")
            return redirect(url_for("apply_policy"))

        if policy_dao.create_policy(policy):
            flash(f"Policy '{pol_num}' successfully registered & activated!", "success")
            return redirect(url_for("policies"))
        else:
            flash("Failed to register policy.", "error")
            return redirect(url_for("apply_policy"))

    return render_template("apply_policy.html", username=session.get("username"), vehicles=user_vehicles)


@app.route("/policies/add", methods=["GET", "POST"])
def add_policy():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session.get("user_id")
    portal = get_active_portal()

    if portal == "agent":
        customers = customer_dao.get_all_customers()
        vehicles = vehicle_dao.get_all_vehicles()
    else:
        customers = [customer_dao.find_by_customer_id(user_id)] if customer_dao.find_by_customer_id(user_id) else []
        vehicles = vehicle_dao.get_vehicles_by_user_id(user_id)

    if request.method == "POST":
        pol_id = request.form.get("policy_id", "").strip() or f"POL{random.randint(1000, 9999)}"
        pol_num = request.form.get("policy_number", "").strip() or f"POL-NO-{random.randint(10000, 99999)}"
        target_customer_id = request.form.get("customer_id", "").strip() or user_id

        policy = Policy(
            policy_id=pol_id,
            policy_number=pol_num,
            customer_id=target_customer_id,
            vehicle_id=request.form.get("vehicle_id", "").strip(),
            policy_type=request.form.get("policy_type", "").strip(),
            premium=request.form.get("premium", "").strip(),
            start_date=request.form.get("start_date", "").strip(),
            end_date=request.form.get("end_date", "").strip(),
            expiry_date=request.form.get("end_date", "").strip(),
            coverage=request.form.get("coverage", "").strip(),
            status=request.form.get("status", "Active").strip(),
        )

        if not all([
            policy.policy_id,
            policy.vehicle_id,
            policy.policy_type,
            policy.premium,
            policy.start_date,
            policy.end_date,
        ]):
            flash("Please fill in all policy fields.", "error")
            return redirect(url_for("add_policy"))

        if policy_dao.create_policy(policy):
            flash(f"Policy '{policy.policy_number}' issued successfully.", "success")
            return redirect(url_for("policies"))
        else:
            flash("Policy ID already exists.", "error")
            return redirect(url_for("add_policy"))

    today_str = date.today().strftime("%Y-%m-%d")
    return render_template("add_policy.html", username=session.get("username"), vehicles=vehicles, customers=customers, today_str=today_str)


@app.route("/policies")
def policies():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session.get("user_id")
    portal = get_active_portal()
    q = request.args.get("q", "").strip().lower()
    status_filter = request.args.get("status", "").strip().lower()

    if portal == "agent":
        all_policies = policy_dao.get_all_policies()
    else:
        all_policies = policy_dao.get_policies_by_user_id(user_id)

    if q:
        filtered = [
            p
            for p in all_policies
            if q in (p.policy_id or "").lower()
            or q in (p.policy_number or "").lower()
            or q in (p.vehicle_id or "").lower()
            or q in (p.customer_id or "").lower()
            or q in (p.policy_type or "").lower()
        ]
    else:
        filtered = all_policies

    if status_filter:
        filtered = [p for p in filtered if (p.status or "").strip().lower() == status_filter]

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

    user_id = session.get("user_id")
    portal = get_active_portal()
    q = request.args.get("q", "").strip().lower()

    if portal == "agent":
        target_payments = payment_dao.get_all_payments()
        target_policies = policy_dao.get_all_policies()
    else:
        target_payments = payment_dao.get_payments_by_user_id(user_id)
        target_policies = policy_dao.get_policies_by_user_id(user_id)

    payment_list = []
    paid_policy_ids = {p.policy_id for p in target_payments if p.status.lower() == "paid"}

    for p in target_payments:
        payment_list.append(
            {
                "payment_id": p.payment_id,
                "policy_id": p.policy_id,
                "user_id": p.user_id,
                "amount": p.amount,
                "payment_date": p.payment_date,
                "transaction_id": p.transaction_id,
                "status": p.status,
            }
        )

    for pol in target_policies:
        if pol.policy_id not in paid_policy_ids:
            payment_list.append(
                {
                    "payment_id": f"DUE-{pol.policy_id}",
                    "policy_id": pol.policy_id,
                    "user_id": pol.customer_id,
                    "amount": pol.premium,
                    "payment_date": pol.end_date,
                    "transaction_id": "PENDING",
                    "status": "Due",
                }
            )

    if q:
        payment_list = [
            p
            for p in payment_list
            if q in p["policy_id"].lower()
            or q in p["transaction_id"].lower()
            or q in p["status"].lower()
            or q in str(p["user_id"]).lower()
        ]

    pending_count = sum(1 for p in payment_list if p["status"].lower() == "due")
    completed_count = sum(1 for p in payment_list if p["status"].lower() == "paid")
    total_revenue = 0.0
    for p in payment_list:
        if p["status"].lower() == "paid":
            try:
                total_revenue += float(p["amount"])
            except (ValueError, TypeError):
                continue

    return render_template(
        "payments.html",
        username=session.get("username"),
        payments=payment_list,
        query=q,
        pending_count=pending_count,
        completed_count=completed_count,
        total_revenue=total_revenue,
        user_policies=target_policies,
    )



@app.route("/payments/pay/<policy_id>", methods=["POST"])
def process_payment(policy_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session.get("user_id")
    policy = policy_dao.find_by_policy_id(policy_id)
    amount = request.form.get("amount", policy.premium if policy else "5000").strip()

    payment_id = f"PAY{random.randint(1000, 9999)}"
    txn_id = f"TXN{random.randint(100000, 999999)}"
    today_str = date.today().strftime("%Y-%m-%d")

    payment = Payment(
        payment_id=payment_id,
        user_id=user_id,
        policy_id=policy_id,
        amount=amount,
        payment_date=today_str,
        transaction_id=txn_id,
        status="Paid",
    )

    if payment_dao.create_payment(payment):
        flash(f"Payment of ₹{amount} successful! Ref: {txn_id}", "success")
    else:
        flash("Payment processing failed.", "error")

    return redirect(url_for("payments"))


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


@app.route("/claims/action/<claim_id>/<action>", methods=["GET", "POST"])
def claim_action(claim_id, action):
    if "user_id" not in session:
        return redirect(url_for("login"))

    status_map = {
        "approve": "Approved",
        "reject": "Rejected",
        "pending": "Pending",
    }
    target_status = status_map.get(action.lower(), "Pending")

    if claim_dao.update_claim_status(claim_id, target_status):
        flash(f"Claim '{claim_id}' updated to status: {target_status}.", "success")
    else:
        flash("Failed to update claim status.", "error")

    return redirect(url_for("view_claims"))


@app.route("/claims/view")
def view_claims():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = str(session.get("user_id", ""))
    portal = get_active_portal()

    if portal == "agent":
        claims = claim_dao.get_all_claims()
    else:
        claims = claim_dao.get_claims_by_user_id(user_id)

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

    user_id = session.get("user_id")
    portal = get_active_portal()

    if portal == "agent":
        user_policies = policy_dao.get_all_policies()
    else:
        user_policies = policy_dao.get_policies_by_user_id(user_id)

    if request.method == "POST":
        claim_id = request.form.get("claim_id", "").strip() or f"CLM{random.randint(1000, 9999)}"
        claim_date = request.form.get("claim_date", "").strip() or date.today().strftime("%Y-%m-%d")
        accident_date = request.form.get("accident_date", "").strip() or claim_date

        policy_id = request.form.get("policy_id", "").strip()
        policy = policy_dao.find_by_policy_id(policy_id)
        vehicle_id = policy.vehicle_id if policy else ""

        claim = Claim(
            claim_id=claim_id,
            user_id=user_id,
            policy_id=policy_id,
            vehicle_id=vehicle_id,
            customer_name=request.form.get("customer_name", "").strip() or session.get("username", "Customer"),
            vehicle_number=request.form.get("vehicle_number", "").strip(),
            insurance_company="Standard Insurance Co.",
            accident_date=accident_date,
            incident_location=request.form.get("incident_location", "").strip(),
            claim_date=claim_date,
            claim_amount=request.form.get("claim_amount", "").strip(),
            reason=request.form.get("claim_type", "").strip() or request.form.get("reason", "").strip(),
            description=request.form.get("description", "").strip(),
            status="Pending",
            documents="",
        )

        if not all([claim.policy_id, claim.accident_date, claim.claim_amount, claim.description]):
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
            flash(f"Claim '{claim.claim_id}' submitted successfully.", "success")
            return redirect(url_for("view_claims"))
        else:
            flash(f"Claim ID '{claim.claim_id}' already exists.", "error")
            return redirect(url_for("add_claim"))

    today_str = date.today().strftime("%Y-%m-%d")
    return render_template("add_claim.html", username=session.get("username"), policies=user_policies, today_str=today_str)


@app.route("/vehicles/add", methods=["GET", "POST"])
def add_vehicle():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session.get("user_id")

    if request.method == "POST":
        v_id = request.form.get("vehicle_id", "").strip() or f"VEH{random.randint(1000, 9999)}"
        vehicle = Vehicle(
            vehicle_id=v_id,
            customer_id=user_id,
            vehicle_number=request.form.get("vehicle_number", "").strip(),
            brand=request.form.get("brand", "").strip(),
            model=request.form.get("model", "").strip(),
            year=request.form.get("year", "").strip(),
            engine_no=request.form.get("engine_no", "").strip(),
            chassis_no=request.form.get("chassis_no", "").strip(),
            vehicle_type=request.form.get("vehicle_type", "Car").strip(),
            registration_date=request.form.get("registration_date", date.today().strftime("%Y-%m-%d")).strip(),
        )

        if not all([
            vehicle.vehicle_id,
            vehicle.vehicle_number,
            vehicle.brand,
            vehicle.model,
            vehicle.year,
        ]):
            flash("Please fill in all required vehicle fields.", "error")
            return redirect(url_for("add_vehicle"))

        if vehicle_dao.create_vehicle(vehicle):
            flash(f"Vehicle '{vehicle.vehicle_number}' added successfully.", "success")
            return redirect(url_for("vehicles"))
        else:
            flash("Vehicle ID or Number already exists.", "error")
            return redirect(url_for("add_vehicle"))

    return render_template("add_vehicle.html", username=session.get("username"), user_id=user_id)


@app.route("/vehicles")
def vehicles():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session.get("user_id")
    portal = get_active_portal()
    q = request.args.get("q", "").strip().lower()

    if portal == "agent":
        target_vehicles = vehicle_dao.get_all_vehicles()
    else:
        target_vehicles = vehicle_dao.get_vehicles_by_user_id(user_id)

    if q:
        filtered = [
            v
            for v in target_vehicles
            if q in (v.vehicle_id or "").lower()
            or q in (v.vehicle_number or "").lower()
            or q in (v.brand or "").lower()
            or q in (v.model or "").lower()
            or q in (v.customer_id or "").lower()
        ]
    else:
        filtered = target_vehicles

    return render_template("vehicles.html", username=session.get("username"), vehicles=filtered, query=q)



@app.route("/vehicles/<vehicle_id>")
def view_vehicle(vehicle_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    vehicle = vehicle_dao.find_by_vehicle_id(vehicle_id)
    if not vehicle:
        flash("Vehicle not found.", "error")
        return redirect(url_for("vehicles"))

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
    return render_template(
        "settings.html",
        username=session.get("username"),
        email=session.get("email"),
        mobile=session.get("mobile"),
        address=session.get("address"),
        user_id=session.get("user_id"),
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
