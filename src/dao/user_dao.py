import sqlite3
from database import get_db_connection
from model.user import User

class UserDAO:
    def find_by_email(self, email: str):
        conn = get_db_connection()
        user = None
        try:
            cursor = conn.execute(
                "SELECT id, username, email, password FROM users WHERE email = ?",
                (email,),
            )
            row = cursor.fetchone()
            if row:
                user = User(
                    id=row["id"],
                    username=row["username"],
                    email=row["email"],
                    password=row["password"],
                )
        finally:
            conn.close()
        return user

    def create_user(self, user: User):
        conn = get_db_connection()
        try:
            cursor = conn.execute(
                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                (user.username, user.email, user.password),
            )
            conn.commit()
            user.id = cursor.lastrowid
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
