import sqlite3
from database import get_db_connection
from model.user import User

class UserDAO:
    def find_by_email(self, email: str):
        conn = get_db_connection()
        user = None
        try:
            cursor = conn.execute(
                "SELECT id, user_id, username, email, mobile, address, password, role, secret_code FROM users WHERE email = ?",
                (email,),
            )
            row = cursor.fetchone()
            if row:
                user = User(
                    id=row["id"],
                    user_id=row["user_id"],
                    username=row["username"],
                    email=row["email"],
                    mobile=row["mobile"],
                    address=row["address"],
                    password=row["password"],
                    role=row["role"] if "role" in row.keys() and row["role"] else "customer",
                    secret_code=row["secret_code"] if "secret_code" in row.keys() and row["secret_code"] is not None else "AGENT789",
                )
        finally:
            conn.close()
        return user

    def find_by_user_id(self, user_id: str):
        conn = get_db_connection()
        user = None
        try:
            cursor = conn.execute(
                "SELECT id, user_id, username, email, mobile, address, password, role, secret_code FROM users WHERE user_id = ?",
                (user_id,),
            )
            row = cursor.fetchone()
            if row:
                user = User(
                    id=row["id"],
                    user_id=row["user_id"],
                    username=row["username"],
                    email=row["email"],
                    mobile=row["mobile"],
                    address=row["address"],
                    password=row["password"],
                    role=row["role"] if "role" in row.keys() and row["role"] else "customer",
                    secret_code=row["secret_code"] if "secret_code" in row.keys() and row["secret_code"] is not None else "AGENT789",
                )
        finally:
            conn.close()
        return user

    def create_user(self, user: User):
        conn = get_db_connection()
        try:
            cursor = conn.execute(
                "INSERT INTO users (user_id, username, email, mobile, address, password, role, secret_code) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (user.user_id, user.username, user.email, user.mobile, user.address, user.password, user.role or "customer", user.secret_code or "AGENT789"),
            )
            conn.commit()
            user.id = cursor.lastrowid
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def update_secret_code(self, user_id: str, new_secret_code: str):
        conn = get_db_connection()
        try:
            conn.execute(
                "UPDATE users SET secret_code = ? WHERE user_id = ?",
                (new_secret_code, user_id),
            )
            conn.commit()
            return True
        except sqlite3.Error:
            return False
        finally:
            conn.close()
