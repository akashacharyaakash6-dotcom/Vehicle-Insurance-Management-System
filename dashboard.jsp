<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
    <%@ page import="java.util.*" %>
        <% String username=(String) session.getAttribute("username"); String email=(String)
            session.getAttribute("email"); Integer userId=(Integer) session.getAttribute("userId"); if (username==null
            || email==null || userId==null) { response.sendRedirect("index.jsp"); return; } String today=new
            java.text.SimpleDateFormat("EEEE, MMMM d, yyyy").format(new Date()); %>
            <!DOCTYPE html>
            <html lang="en">

            <head>
                <meta charset="UTF-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                <title>Dashboard - Vehicle Insurance Management</title>
                <link rel="stylesheet" href="css/dashboard.css" />
            </head>

            <body>
                <div class="dashboard-shell">
                    <aside class="nav-panel">
                        <div class="nav-brand">
                            <img src="images/logo.png" alt="Logo" />
                            <div>
                                <h2>Vehicle Insurance</h2>
                                <span>Management System</span>
                            </div>
                        </div>
                        <nav class="nav-links">
                            <a class="active" href="#">Dashboard</a>
                            <a href="#">Customers</a>
                            <a href="#">Vehicles</a>
                            <a href="#">Policies</a>
                            <a href="#">Claims</a>
                            <a href="#">Payments</a>
                            <a href="#">Reports</a>
                            <a href="logout.jsp" class="logout-link">Logout</a>
                        </nav>
                    </aside>

                    <main class="dashboard-main">
                        <header class="topbar">
                            <div>
                                <h1>Hello,<span class="highlight">
                                        <%= username %>
                                    </span> 👋</h1>
                                <p>Welcome back to your Vehicle Insurance dashboard.</p>
                            </div>
                            <div class="topbar-meta">
                                <span>Today</span>
                                <strong>
                                    <%= today %>
                                </strong>
                            </div>
                        </header>

                        <section class="stats-grid animate-slide-up">
                            <article class="stat-card">
                                <div class="stat-icon">👥</div>
                                <div>
                                    <h3>Total Customers</h3>
                                    <p>1245</p>
                                </div>
                            </article>
                            <article class="stat-card">
                                <div class="stat-icon">🚗</div>
                                <div>
                                    <h3>Total Vehicles</h3>
                                    <p>862</p>
                                </div>
                            </article>
                            <article class="stat-card">
                                <div class="stat-icon">🛡️</div>
                                <div>
                                    <h3>Active Policies</h3>
                                    <p>578</p>
                                </div>
                            </article>
                            <article class="stat-card">
                                <div class="stat-icon">⚠️</div>
                                <div>
                                    <h3>Claims</h3>
                                    <p>73</p>
                                </div>
                            </article>
                            <article class="stat-card">
                                <div class="stat-icon">💰</div>
                                <div>
                                    <h3>Premium Collection</h3>
                                    <p>$184,320</p>
                                </div>
                            </article>
                        </section>

                        <section class="dashboard-content animate-fade-in">
                            <div class="welcome-banner">
                                <div>
                                    <h2>Hello, <%= username %>!</h2>
                                    <p>Manage policy renewals, customer records, vehicle insurance, and claims in one
                                        place.</p>
                                </div>
                                <div class="banner-cta">
                                    <button class="btn-secondary">Explore Reports</button>
                                </div>
                            </div>

                            <div class="quick-actions">
                                <button>Add Customer</button>
                                <button>Add Vehicle</button>
                                <button>New Policy</button>
                                <button>View Claims</button>
                            </div>

                            <div class="recent-activity">
                                <div class="activity-header">
                                    <h2>Recent Activity</h2>
                                    <span>Updated moments ago</span>
                                </div>
                                <div class="activity-list">
                                    <div class="activity-item">
                                        <span>✔</span>
                                        <div>
                                            <strong>Policy renewed</strong>
                                            <p>Customer Aria K. renewed a comprehensive plan.</p>
                                        </div>
                                    </div>
                                    <div class="activity-item">
                                        <span>📄</span>
                                        <div>
                                            <strong>New claim filed</strong>
                                            <p>Claim submitted for vehicle ID #V-9812.</p>
                                        </div>
                                    </div>
                                    <div class="activity-item">
                                        <span>💳</span>
                                        <div>
                                            <strong>Premium collected</strong>
                                            <p>$1,200 received from John D.</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </section>
                    </main>
                </div>

                <script src="js/dashboard.js"></script>
            </body>

            </html>