"""
Role-Based Access Control (RBAC) Module

Rules:
1. role == "customer":
   - allow /customer/*
   - deny /agent/*

2. role == "agent":
   - allow /agent/*

3. role == "admin" and username == "Akash":
   - allow /admin/*
   - allow /agent/*
"""

def is_allowed(role: str, username: str, path: str) -> bool:
    """
    Check if a user with given role and username is permitted to access path.
    """
    if not role or not path:
        return False

    role = role.strip().lower()
    username = (username or "").strip()
    path = path.rstrip("/") if path != "/" else "/"

    def matches_route(pattern: str) -> bool:
        prefix = pattern.rstrip("*")
        return path.startswith(prefix) or path == prefix.rstrip("/")

    if role == "customer":
        if matches_route("/agent/"):
            return False
        if matches_route("/customer/"):
            return True
        return False

    if role == "agent":
        if matches_route("/agent/"):
            return True
        return False

    if role == "admin" and username == "Akash":
        if matches_route("/admin/") or matches_route("/agent/"):
            return True
        return False

    return False
