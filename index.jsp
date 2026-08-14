<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Vehicle Insurance Management System - Login</title>
    <link rel="stylesheet" href="css/style.css" />
</head>
<body>
    <div class="page-background"></div>
    <div class="login-wrapper">
        <div class="glass-card animate-fade-in">
            <div class="brand-header">
                <img src="images/logo.png" alt="Company Logo" class="brand-logo" />
                <div>
                    <h1>Vehicle Insurance Management</h1>
                    <p>Sign in to manage customers, vehicles, policies and claims</p>
                </div>
            </div>

            <form id="loginForm" action="login" method="post" novalidate>
                <% String error = request.getParameter("error"); if (error != null && !error.isEmpty()) { %>
                    <div class="server-error"><%= error %></div>
                <% } %>
                <div class="form-group">
                    <label for="username">Username</label>
                    <input type="text" id="username" name="username" placeholder="Enter your username" required />
                    <span class="error-message" id="usernameError"></span>
                </div>

                <div class="form-group">
                    <label for="email">Gmail Address</label>
                    <input type="email" id="email" name="email" placeholder="abc@gmail.com" required />
                    <span class="error-message" id="emailError"></span>
                </div>

                <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" id="password" name="password" placeholder="Enter your password" required />
                    <span class="error-message" id="passwordError"></span>
                </div>

                <div class="form-details">
                    <label class="checkbox-label">
                        <input type="checkbox" id="rememberMe" name="rememberMe" /> Remember Me
                    </label>
                    <a href="#" class="forgot-link">Forgot Password?</a>
                </div>

                <button type="submit" class="btn-primary">Login</button>
                <p class="footer-text">New user? Your account will be created automatically if Gmail is not found.</p>
            </form>
        </div>
    </div>

    <script src="js/login.js"></script>
</body>
</html>
