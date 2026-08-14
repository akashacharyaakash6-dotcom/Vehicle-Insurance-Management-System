from pathlib import Path

BASE = Path(__file__).resolve().parent
TEMPLATES = {
    'templates/dashboard.html': """{% extends \"layout.html\" %}

{% block title %}Dashboard - Vehicle Insurance{% endblock %}
{% block breadcrumb %}Dashboard{% endblock %}
{% block page_heading %}Welcome back, {{ username }}{% endblock %}

{% block content %}
<div class=\"panel-card\">
    <div class=\"panel-card-header\">
        <div>
            <p class=\"eyebrow\">Overview</p>
            <h2>Premium Vehicle Insurance Dashboard</h2>
        </div>
        <span class=\"status-badge badge-secondary\">Operational Metrics</span>
    </div>
    <p class=\"text-muted\">Monitor active policies, claims, customers, and vehicles with a polished enterprise-grade interface.</p>
</div>

<div class=\"stats-grid\">
    <article class=\"metric-card\">
        <div class=\"metric-title\"><p>Total Customers</p><span>👥</span></div>
        <p class=\"metric-value\">{{ total_customers }}</p>
        <div class=\"metric-meta\"><span class=\"metric-badge\">Registered</span><span>Customers</span></div>
    </article>
    <article class=\"metric-card\">
        <div class=\"metric-title\"><p>Total Vehicles</p><span>🚗</span></div>
        <p class=\"metric-value\">{{ total_vehicles }}</p>
        <div class=\"metric-meta\"><span class=\"metric-badge\">Insured</span><span>Vehicles</span></div>
    </article>
    <article class=\"metric-card\">
        <div class=\"metric-title\"><p>Active Policies</p><span>🛡️</span></div>
        <p class=\"metric-value\">{{ active_policies }}</p>
        <div class=\"metric-meta\"><span class=\"metric-badge\">Current</span><span>Policies</span></div>
    </article>
    <article class=\"metric-card\">
        <div class=\"metric-title\"><p>Pending Claims</p><span>📋</span></div>
        <p class=\"metric-value\">{{ pending_claims }}</p>
        <div class=\"metric-meta\"><span class=\"metric-badge\">Review</span><span>Pending</span></div>
    </article>
</div>

<div class=\"chart-grid\">
    <section class=\"chart-panel\">
        <div class=\"panel-card-header\"><div><h3>Policy Overview</h3><p class=\"text-muted\">Active versus expired coverage snapshot.</p></div></div>
        <div class=\"chart-bars\">
            <div class=\"chart-bar bar-2\"></div>
            <div class=\"chart-bar bar-1\"></div>
            <div class=\"chart-bar bar-4\"></div>
            <div class=\"chart-bar bar-3\"></div>
        </div>
        <div class=\"chart-legend\"><span><span class=\"chart-dot\"></span>Active</span><span><span class=\"chart-dot\" style=\"background:#E8DFD0\"></span>Expired</span></div>
    </section>
    <section class=\"chart-panel\">
        <div class=\"panel-card-header\"><div><h3>Claims Workflow</h3><p class=\"text-muted\">Pending cases versus approved progress.</p></div></div>
        <div class=\"chart-bars\">
            <div class=\"chart-bar bar-4\" style=\"background:rgba(30,41,59,0.92)\"></div>
            <div class=\"chart-bar bar-3\" style=\"background:rgba(91,124,153,0.9)\"></div>
            <div class=\"chart-bar bar-2\" style=\"background:rgba(232,223,208,0.9)\"></div>
            <div class=\"chart-bar bar-1\" style=\"background:rgba(255,253,248,0.9)\"></div>
        </div>
        <div class=\"chart-legend\"><span><span class=\"chart-dot\" style=\"background:#1E293B\"></span>Pending</span><span><span class=\"chart-dot\" style=\"background:#5B7C99\"></span>Processed</span></div>
    </section>
</div>
{% endblock %}
""",
    'templates/reports.html': """{% extends \"layout.html\" %}

{% block title %}Reports - Vehicle Insurance{% endblock %}
{% block breadcrumb %}Reports{% endblock %}
{% block page_heading %}Analytics & Reports{% endblock %}

{% block content %}
<div class=\"stats-grid\">
    <article class=\"metric-card\"><div class=\"metric-title\"><p>Customers</p><span>👥</span></div><p class=\"metric-value\">{{ customer_count }}</p><div class=\"metric-meta\"><span class=\"metric-badge\">Total</span><span>Profiles</span></div></article>
    <article class=\"metric-card\"><div class=\"metric-title\"><p>Vehicles</p><span>🚗</span></div><p class=\"metric-value\">{{ vehicle_count }}</p><div class=\"metric-meta\"><span class=\"metric-badge\">Total</span><span>Fleet</span></div></article>
    <article class=\"metric-card\"><div class=\"metric-title\"><p>Policies</p><span>🛡️</span></div><p class=\"metric-value\">{{ policy_count }}</p><div class=\"metric-meta\"><span class=\"metric-badge\">Active</span><span>Coverage</span></div></article>
    <article class=\"metric-card\"><div class=\"metric-title\"><p>Claims</p><span>📋</span></div><p class=\"metric-value\">{{ claim_count }}</p><div class=\"metric-meta\"><span class=\"metric-badge\">Reported</span><span>Updates</span></div></article>
</div>

<div class=\"panel-card\">
    <div class=\"panel-card-header\"><div><h2>Reports summary</h2><p class=\"text-muted\">Export or review high-level policy, claims, and payment metrics.</p></div></div>
    <div class=\"form-actions\">
        <button class=\"btn btn-secondary\">Export PDF</button>
        <button class=\"btn btn-secondary\">Export Excel</button>
        <button class=\"btn btn-ghost\">Print</button>
    </div>
</div>

<div class=\"table-panel\">
    <h3>Recent Claims</h3>
    <table class=\"data-table\">
        <thead><tr><th>Claim ID</th><th>Policy</th><th>Date</th><th>Status</th></tr></thead>
        <tbody>
            {% if recent_claims %}
                {% for claim in recent_claims %}
                    <tr><td>{{ claim.claim_id }}</td><td>{{ claim.policy_id }}</td><td>{{ claim.claim_date }}</td><td><span class=\"status-pill {{ claim.status|lower }}\">{{ claim.status }}</span></td></tr>
                {% endfor %}
            {% else %}
                <tr><td colspan=\"4\">No recent claims available.</td></tr>
            {% endif %}
        </tbody>
    </table>
</div>
{% endblock %}
""",
    'templates/customers.html': """{% extends \"layout.html\" %}

{% block title %}Customers - Vehicle Insurance{% endblock %}
{% block breadcrumb %}Customers{% endblock %}
{% block page_heading %}Customer Management{% endblock %}

{% block content %}
<div class=\"panel-card\">
    <div class=\"panel-card-header\">
        <div><p class=\"eyebrow\">Customers</p><h2>Customer Records</h2></div>
        <a href=\"{{ url_for('add_customer') }}\" class=\"btn btn-primary\">Add Customer</a>
    </div>
    <form action=\"{{ url_for('customers') }}\" method=\"get\" class=\"search-form\">
        <input type=\"search\" name=\"q\" value=\"{{ query }}\" placeholder=\"Search by name, ID or email\" />
        <button type=\"submit\" class=\"btn btn-secondary\">Search</button>
    </form>
</div>

<div class=\"table-panel\">
    <table class=\"data-table\">
        <thead>
            <tr><th>Customer ID</th><th>Name</th><th>Email</th><th>Phone</th><th>Vehicles</th><th>Status</th><th>Actions</th></tr>
        </thead>
        <tbody>
            {% if customers %}
                {% for c in customers %}
                    <tr>
                        <td>{{ c.customer_id }}</td>
                        <td>{{ c.name }}</td>
                        <td>{{ c.email }}</td>
                        <td>{{ c.phone }}</td>
                        <td>{{ vehicle_counts.get(c.customer_id, 0) }}</td>
                        <td><span class=\"status-pill active\">Active</span></td>
                        <td><a href=\"{{ url_for('view_customer', customer_id=c.customer_id) }}\" class=\"btn btn-secondary\">View</a></td>
                    </tr>
                {% endfor %}
            {% else %}
                <tr><td colspan=\"7\">No customers found.</td></tr>
            {% endif %}
        </tbody>
    </table>
</div>
{% endblock %}
""",
    'templates/add_customer.html': """{% extends \"layout.html\" %}

{% block title %}Add Customer - Vehicle Insurance{% endblock %}
{% block breadcrumb %}Customers / Add{% endblock %}
{% block page_heading %}Add New Customer{% endblock %}

{% block content %}
<div class=\"form-panel\">
    <form class=\"form-grid\" method=\"post\" action=\"{{ url_for('add_customer') }}\">
        <div class=\"form-group\"><label for=\"customer_id\">Customer ID</label><input id=\"customer_id\" type=\"text\" name=\"customer_id\" class=\"form-control\" placeholder=\"C-1001\" required /></div>
        <div class=\"form-group\"><label for=\"name\">Full Name</label><input id=\"name\" type=\"text\" name=\"name\" class=\"form-control\" placeholder=\"John Doe\" required /></div>
        <div class=\"form-group\"><label for=\"email\">Email Address</label><input id=\"email\" type=\"email\" name=\"email\" class=\"form-control\" placeholder=\"john@example.com\" required /></div>
        <div class=\"form-group\"><label for=\"phone\">Phone Number</label><input id=\"phone\" type=\"text\" name=\"phone\" class=\"form-control\" placeholder=\"9876543210\" required /></div>
        <div class=\"form-group full-width\"><label for=\"address\">Address</label><input id=\"address\" type=\"text\" name=\"address\" class=\"form-control\" placeholder=\"123 Main Street, City\" required /></div>
        <div class=\"form-group\"><label for=\"dob\">Date of Birth</label><input id=\"dob\" type=\"date\" name=\"dob\" class=\"form-control\" required /></div>
        <div class=\"form-group\"><label for=\"license_no\">License Number</label><input id=\"license_no\" type=\"text\" name=\"license_no\" class=\"form-control\" placeholder=\"LIC12345\" required /></div>
        <div class=\"form-group full-width\" style=\"display:flex; justify-content:flex-end; gap:1rem;\">
            <button type=\"submit\" class=\"btn btn-primary\">Save Customer</button>
            <a href=\"{{ url_for('dashboard') }}\" class=\"btn btn-ghost\">Cancel</a>
        </div>
    </form>
</div>
{% endblock %}
""",
    'templates/vehicles.html': """{% extends \"layout.html\" %}

{% block title %}Vehicles - Vehicle Insurance{% endblock %}
{% block breadcrumb %}Vehicles{% endblock %}
{% block page_heading %}Vehicle Management{% endblock %}

{% block content %}
<div class=\"panel-card\">
    <div class=\"panel-card-header\">
        <div><p class=\"eyebrow\">Vehicles</p><h2>All Registered Vehicles</h2></div>
        <a href=\"{{ url_for('add_vehicle') }}\" class=\"btn btn-primary\">Add Vehicle</a>
    </div>
    <form action=\"{{ url_for('vehicles') }}\" method=\"get\" class=\"search-form\">
        <input type=\"search\" name=\"q\" value=\"{{ query }}\" placeholder=\"Search by vehicle, brand, model or owner\" />
        <button type=\"submit\" class=\"btn btn-secondary\">Search</button>
    </form>
</div>

<div class=\"table-panel\">
    <table class=\"data-table\">
        <thead>
            <tr><th>Vehicle ID</th><th>Number</th><th>Brand</th><th>Model</th><th>Owner ID</th><th>Action</th></tr>
        </thead>
        <tbody>
            {% if vehicles %}
                {% for v in vehicles %}
                    <tr>
                        <td>{{ v.vehicle_id }}</td>
                        <td>{{ v.vehicle_number }}</td>
                        <td>{{ v.brand }}</td>
                        <td>{{ v.model }}</td>
                        <td>{{ v.customer_id }}</td>
                        <td><a href=\"{{ url_for('view_vehicle', vehicle_id=v.vehicle_id) }}\" class=\"btn btn-secondary\">Details</a></td>
                    </tr>
                {% endfor %}
            {% else %}
                <tr><td colspan=\"6\">No vehicles found.</td></tr>
            {% endif %}
        </tbody>
    </table>
</div>
{% endblock %}
""",
    'templates/add_vehicle.html': """{% extends \"layout.html\" %}

{% block title %}Add Vehicle - Vehicle Insurance{% endblock %}
{% block breadcrumb %}Vehicles / Add{% endblock %}
{% block page_heading %}Add New Vehicle{% endblock %}

{% block content %}
<div class=\"form-panel\">
    <form class=\"form-grid\" method=\"post\" action=\"{{ url_for('add_vehicle') }}\">
        <div class=\"form-group\"><label for=\"vehicle_id\">Vehicle ID</label><input id=\"vehicle_id\" type=\"text\" name=\"vehicle_id\" class=\"form-control\" placeholder=\"V-1001\" required /></div>
        <div class=\"form-group\"><label for=\"customer_id\">Customer ID</label><input id=\"customer_id\" type=\"text\" name=\"customer_id\" class=\"form-control\" placeholder=\"C-1001\" required /></div>
        <div class=\"form-group\"><label for=\"vehicle_number\">Vehicle Number</label><input id=\"vehicle_number\" type=\"text\" name=\"vehicle_number\" class=\"form-control\" placeholder=\"MH12AB1234\" required /></div>
        <div class=\"form-group\"><label for=\"brand\">Brand</label><input id=\"brand\" type=\"text\" name=\"brand\" class=\"form-control\" placeholder=\"Toyota\" required /></div>
        <div class=\"form-group\"><label for=\"model\">Model</label><input id=\"model\" type=\"text\" name=\"model\" class=\"form-control\" placeholder=\"Corolla\" required /></div>
        <div class=\"form-group\"><label for=\"year\">Year</label><input id=\"year\" type=\"number\" name=\"year\" class=\"form-control\" placeholder=\"2024\" min=\"1900\" max=\"2100\" required /></div>
        <div class=\"form-group\"><label for=\"engine_no\">Engine No</label><input id=\"engine_no\" type=\"text\" name=\"engine_no\" class=\"form-control\" placeholder=\"ENG123456\" required /></div>
        <div class=\"form-group\"><label for=\"chassis_no\">Chassis No</label><input id=\"chassis_no\" type=\"text\" name=\"chassis_no\" class=\"form-control\" placeholder=\"CHS123456\" required /></div>
        <div class=\"form-group full-width\" style=\"display:flex; justify-content:flex-end; gap:1rem;\">
            <button type=\"submit\" class=\"btn btn-primary\">Save Vehicle</button>
            <a href=\"{{ url_for('dashboard') }}\" class=\"btn btn-ghost\">Cancel</a>
        </div>
    </form>
</div>
{% endblock %}
""",
    'templates/policies.html': """{% extends \"layout.html\" %}

{% block title %}Policies - Vehicle Insurance{% endblock %}
{% block breadcrumb %}Policies{% endblock %}
{% block page_heading %}Policy Management{% endblock %}

{% block content %}
<div class=\"panel-card\">
    <div class=\"panel-card-header\">
        <div><p class=\"eyebrow\">Policies</p><h2>Policy Records</h2></div>
        <a href=\"{{ url_for('add_policy') }}\" class=\"btn btn-primary\">Add Policy</a>
    </div>
    <form action=\"{{ url_for('policies') }}\" method=\"get\" class=\"search-form\">
        <input type=\"search\" name=\"q\" value=\"{{ query }}\" placeholder=\"Search by policy, customer, vehicle or type\" />
        <select name=\"status\" class=\"form-control\">
            <option value=\"\">All Statuses</option>
            <option value=\"active\" {% if status_filter == 'active' %}selected{% endif %}>Active</option>
            <option value=\"pending\" {% if status_filter == 'pending' %}selected{% endif %}>Pending</option>
            <option value=\"expired\" {% if status_filter == 'expired' %}selected{% endif %}>Expired</option>
            <option value=\"cancelled\" {% if status_filter == 'cancelled' %}selected{% endif %}>Cancelled</option>
        </select>
        <button type=\"submit\" class=\"btn btn-secondary\">Filter</button>
    </form>
</div>

<div class=\"table-panel\">
    <table class=\"data-table\">
        <thead>
            <tr><th>Policy Number</th><th>Customer</th><th>Vehicle</th><th>Type</th><th>Start Date</th><th>Expiry Date</th><th>Premium</th><th>Status</th><th>Actions</th></tr>
        </thead>
        <tbody>
            {% if policies %}
                {% for p in policies %}
                    <tr>
                        <td>{{ p.policy_id }}</td>
                        <td>{{ p.customer_id }}</td>
                        <td>{{ p.vehicle_id }}</td>
                        <td>{{ p.policy_type }}</td>
                        <td>{{ p.start_date }}</td>
                        <td>{{ p.end_date }}</td>
                        <td>{{ p.premium }}</td>
                        <td><span class=\"status-pill {{ p.status|lower }}\">{{ p.status }}</span></td>
                        <td><a href=\"{{ url_for('view_policy', policy_id=p.policy_id) }}\" class=\"btn btn-secondary\">View</a></td>
                    </tr>
                {% endfor %}
            {% else %}
                <tr><td colspan=\"9\">No policies found.</td></tr>
            {% endif %}
        </tbody>
    </table>
</div>
{% endblock %}
""",
    'templates/payments.html': """{% extends \"layout.html\" %}

{% block title %}Payments - Vehicle Insurance{% endblock %}
{% block breadcrumb %}Payments{% endblock %}
{% block page_heading %}Payment Management{% endblock %}

{% block content %}
<div class=\"stats-grid\">
    <article class=\"metric-card\"><div class=\"metric-title\"><p>Total Payments</p><span>💳</span></div><p class=\"metric-value\">{{ payments|length }}</p><div class=\"metric-meta\"><span class=\"metric-badge\">Transactions</span><span>Records</span></div></article>
    <article class=\"metric-card\"><div class=\"metric-title\"><p>Pending Payments</p><span>⏳</span></div><p class=\"metric-value\">{{ pending_count }}</p><div class=\"metric-meta\"><span class=\"metric-badge\">Due</span><span>Invoices</span></div></article>
    <article class=\"metric-card\"><div class=\"metric-title\"><p>Completed Payments</p><span>✅</span></div><p class=\"metric-value\">{{ completed_count }}</p><div class=\"metric-meta\"><span class=\"metric-badge\">Settled</span><span>Success</span></div></article>
    <article class=\"metric-card\"><div class=\"metric-title\"><p>Revenue</p><span>📈</span></div><p class=\"metric-value\">₹{{ '%.2f'|format(total_revenue) }}</p><div class=\"metric-meta\"><span class=\"metric-badge\">Total</span><span>Collected</span></div></article>
</div>

<div class=\"panel-card\">
    <div class=\"panel-card-header\"><div><p class=\"eyebrow\">Payments</p><h2>Payment History</h2></div></div>
    <form action=\"{{ url_for('payments') }}\" method=\"get\" class=\"search-form\">
        <input type=\"search\" name=\"q\" value=\"{{ query }}\" placeholder=\"Search by policy, customer, or status\" />
        <button type=\"submit\" class=\"btn btn-secondary\">Search</button>
    </form>
</div>

<div class=\"table-panel\">
    <table class=\"data-table\">
        <thead>
            <tr><th>Payment ID</th><th>Customer</th><th>Policy</th><th>Amount</th><th>Payment Date</th><th>Due Date</th><th>Method</th><th>Status</th></tr>
        </thead>
        <tbody>
            {% if payments %}
                {% for p in payments %}
                    <tr>
                        <td>{{ p.policy_id }}</td>
                        <td>{{ p.customer_id }}</td>
                        <td>{{ p.policy_id }}</td>
                        <td>{{ p.amount }}</td>
                        <td>{{ p.payment_date }}</td>
                        <td>{{ p.due_date }}</td>
                        <td>{{ p.method }}</td>
                        <td><span class=\"status-pill {% if p.status == 'Due' %}pending{% else %}active{% endif %}\">{{ p.status }}</span></td>
                    </tr>
                {% endfor %}
            {% else %}
                <tr><td colspan=\"8\">No payment records found.</td></tr>
            {% endif %}
        </tbody>
    </table>
</div>
{% endblock %}
""",
    'templates/view_claims.html': """{% extends \"layout.html\" %}

{% block title %}Claims - Vehicle Insurance{% endblock %}
{% block breadcrumb %}Claims{% endblock %}
{% block page_heading %}Claims Management{% endblock %}

{% block content %}
<div class=\"stats-grid\">
    <article class=\"metric-card\"><div class=\"metric-title\"><p>Total Claims</p><span>📋</span></div><p class=\"metric-value\">{{ claims|length }}</p><div class=\"metric-meta\"><span class=\"metric-badge\">Overview</span><span>Claim volume</span></div></article>
    <article class=\"metric-card\"><div class=\"metric-title\"><p>Pending</p><span>⏳</span></div><p class=\"metric-value\">{{ pending_count }}</p><div class=\"metric-meta\"><span class=\"metric-badge\">Review</span><span>In progress</span></div></article>
    <article class=\"metric-card\"><div class=\"metric-title\"><p>Approved</p><span>✅</span></div><p class=\"metric-value\">{{ approved_count }}</p><div class=\"metric-meta\"><span class=\"metric-badge\">Resolved</span><span>Closed</span></div></article>
    <article class=\"metric-card\"><div class=\"metric-title\"><p>Rejected</p><span>❌</span></div><p class=\"metric-value\">{{ rejected_count }}</p><div class=\"metric-meta\"><span class=\"metric-badge\">Declined</span><span>Closed</span></div></article>
</div>

<div class=\"table-panel\">
    <table class=\"data-table\">
        <thead><tr><th>Claim ID</th><th>Policy</th><th>Date</th><th>Amount</th><th>Reason</th><th>Status</th></tr></thead>
        <tbody>
            {% if claims %}
                {% for claim in claims %}
                    <tr>
                        <td>{{ claim.claim_id }}</td>
                        <td>{{ claim.policy_id }}</td>
                        <td>{{ claim.claim_date }}</td>
                        <td>{{ claim.claim_amount }}</td>
                        <td>{{ claim.reason }}</td>
                        <td><span class=\"status-pill {{ claim.status|lower }}\">{{ claim.status }}</span></td>
                    </tr>
                {% endfor %}
            {% else %}
                <tr><td colspan=\"6\">No claims found yet.</td></tr>
            {% endif %}
        </tbody>
    </table>
</div>
{% endblock %}
""",
    'templates/view_customer.html': """{% extends \"layout.html\" %}

{% block title %}Customer Details - Vehicle Insurance{% endblock %}
{% block breadcrumb %}Customers / Details{% endblock %}
{% block page_heading %}Customer Details{% endblock %}

{% block content %}
<div class=\"panel-card\">
    <div class=\"panel-card-header\"><div><p class=\"eyebrow\">Customer</p><h2>{{ customer.name }}</h2></div><a href=\"{{ url_for('customers') }}\" class=\"btn btn-secondary\">Back</a></div>
    <div class=\"form-grid\">
        <div class=\"form-group\"><label>Name</label><div class=\"form-control\">{{ customer.name }}</div></div>
        <div class=\"form-group\"><label>Customer ID</label><div class=\"form-control\">{{ customer.customer_id }}</div></div>
        <div class=\"form-group\"><label>Email</label><div class=\"form-control\">{{ customer.email }}</div></div>
        <div class=\"form-group\"><label>Phone</label><div class=\"form-control\">{{ customer.phone }}</div></div>
        <div class=\"form-group full-width\"><label>Address</label><div class=\"form-control\">{{ customer.address }}</div></div>
        <div class=\"form-group\"><label>DOB</label><div class=\"form-control\">{{ customer.dob }}</div></div>
        <div class=\"form-group\"><label>License</label><div class=\"form-control\">{{ customer.license_no }}</div></div>
    </div>
</div>

<div class=\"table-panel\">
    <h3>Related Policies</h3>
    <table class=\"data-table\">
        <thead><tr><th>Policy ID</th><th>Vehicle ID</th><th>Type</th><th>Premium</th><th>Start</th><th>End</th><th>Status</th></tr></thead>
        <tbody>
            {% if policies %}
                {% for p in policies %}
                    <tr><td>{{ p.policy_id }}</td><td>{{ p.vehicle_id }}</td><td>{{ p.policy_type }}</td><td>{{ p.premium }}</td><td>{{ p.start_date }}</td><td>{{ p.end_date }}</td><td><span class=\"status-pill {{ p.status|lower }}\">{{ p.status }}</span></td></tr>
                {% endfor %}
            {% else %}
                <tr><td colspan=\"7\">No policies found for this customer.</td></tr>
            {% endif %}
        </tbody>
    </table>
</div>
{% endblock %}
""",
    'templates/view_policy.html': """{% extends \"layout.html\" %}

{% block title %}Policy Details - Vehicle Insurance{% endblock %}
{% block breadcrumb %}Policies / Details{% endblock %}
{% block page_heading %}Policy Details{% endblock %}

{% block content %}
<div class=\"panel-card\">
    <div class=\"panel-card-header\"><div><p class=\"eyebrow\">Policy</p><h2>{{ policy.policy_id }}</h2></div><a href=\"{{ url_for('policies') }}\" class=\"btn btn-secondary\">Back</a></div>
    <div class=\"form-grid\">
        <div class=\"form-group\"><label>Type</label><div class=\"form-control\">{{ policy.policy_type }}</div></div>
        <div class=\"form-group\"><label>Premium</label><div class=\"form-control\">{{ policy.premium }}</div></div>
        <div class=\"form-group\"><label>Coverage</label><div class=\"form-control\">{{ policy.coverage }}</div></div>
        <div class=\"form-group\"><label>Status</label><div class=\"form-control\">{{ policy.status }}</div></div>
        <div class=\"form-group\"><label>Start Date</label><div class=\"form-control\">{{ policy.start_date }}</div></div>
        <div class=\"form-group\"><label>End Date</label><div class=\"form-control\">{{ policy.end_date }}</div></div>
    </div>
</div>

<div class=\"panel-card\">
    <div class=\"panel-card-header\"><div><h3>Linked Records</h3></div></div>
    <div class=\"table-panel\">
        <table class=\"data-table\">
            <thead><tr><th>Customer</th><th>Vehicle</th><th>Claim Count</th></tr></thead>
            <tbody><tr><td>{{ customer.name if customer else 'N/A' }}</td><td>{{ vehicle.vehicle_number if vehicle else 'N/A' }}</td><td>{{ claims|length }}</td></tr></tbody>
        </table>
    </div>
</div>

<div class=\"table-panel\">
    <h3>Related Claims</h3>
    <table class=\"data-table\">
        <thead><tr><th>Claim ID</th><th>Date</th><th>Reason</th><th>Amount</th><th>Status</th></tr></thead>
        <tbody>
            {% if claims %}
                {% for c in claims %}
                    <tr><td>{{ c.claim_id }}</td><td>{{ c.claim_date }}</td><td>{{ c.reason }}</td><td>{{ c.claim_amount }}</td><td><span class=\"status-pill {{ c.status|lower }}\">{{ c.status }}</span></td></tr>
                {% endfor %}
            {% else %}
                <tr><td colspan=\"5\">No claims found for this policy.</td></tr>
            {% endif %}
        </tbody>
    </table>
</div>
{% endblock %}
""",
    'templates/view_vehicle.html': """{% extends \"layout.html\" %}

{% block title %}Vehicle Details - Vehicle Insurance{% endblock %}
{% block breadcrumb %}Vehicles / Details{% endblock %}
{% block page_heading %}Vehicle Details{% endblock %}

{% block content %}
<div class=\"panel-card\">
    <div class=\"panel-card-header\"><div><p class=\"eyebrow\">Vehicle</p><h2>{{ vehicle.vehicle_number }}</h2></div><a href=\"{{ url_for('vehicles') }}\" class=\"btn btn-secondary\">Back</a></div>
    <div class=\"form-grid\">
        <div class=\"form-group\"><label>Vehicle ID</label><div class=\"form-control\">{{ vehicle.vehicle_id }}</div></div>
        <div class=\"form-group\"><label>Brand</label><div class=\"form-control\">{{ vehicle.brand }}</div></div>
        <div class=\"form-group\"><label>Model</label><div class=\"form-control\">{{ vehicle.model }}</div></div>
        <div class=\"form-group\"><label>Year</label><div class=\"form-control\">{{ vehicle.year }}</div></div>
        <div class=\"form-group\"><label>Engine No</label><div class=\"form-control\">{{ vehicle.engine_no }}</div></div>
        <div class=\"form-group\"><label>Chassis No</label><div class=\"form-control\">{{ vehicle.chassis_no }}</div></div>
    </div>
</div>

<div class=\"panel-card\">
    <div class=\"panel-card-header\"><div><h3>Owner Details</h3></div></div>
    <div class=\"form-grid\">
        <div class=\"form-group\"><label>Customer ID</label><div class=\"form-control\">{{ vehicle.customer_id or 'N/A' }}</div></div>
        <div class=\"form-group\"><label>Name</label><div class=\"form-control\">{{ customer.name if customer else 'Unknown' }}</div></div>
        <div class=\"form-group\"><label>Email</label><div class=\"form-control\">{{ customer.email if customer else '-' }}</div></div>
        <div class=\"form-group\"><label>Phone</label><div class=\"form-control\">{{ customer.phone if customer else '-' }}</div></div>
    </div>
</div>

<div class=\"table-panel\">
    <h3>Related Policies</h3>
    <table class=\"data-table\">
        <thead><tr><th>Policy ID</th><th>Type</th><th>Premium</th><th>Start</th><th>End</th><th>Status</th></tr></thead>
        <tbody>
            {% if policies %}
                {% for p in policies %}
                    <tr><td>{{ p.policy_id }}</td><td>{{ p.policy_type }}</td><td>{{ p.premium }}</td><td>{{ p.start_date }}</td><td>{{ p.end_date }}</td><td><span class=\"status-pill {{ p.status|lower }}\">{{ p.status }}</span></td></tr>
                {% endfor %}
            {% else %}
                <tr><td colspan=\"6\">No policies linked to this vehicle.</td></tr>
            {% endif %}
        </tbody>
    </table>
</div>
{% endblock %}
""",
    'static/js/dashboard.js': """document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');

    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', () => {
            sidebar.classList.toggle('sidebar-open');
        });
    }
});
""",
}

for relative_path, content in TEMPLATES.items():
    path = BASE / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')
    print(f'Updated {relative_path}')
