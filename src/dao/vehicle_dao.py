import sqlite3
from database import get_db_connection
from model.vehicle import Vehicle


class VehicleDAO:
    def _map_row(self, row):
        return Vehicle(
            id=row["id"],
            vehicle_id=row["vehicle_id"],
            customer_id=row["customer_id"],
            vehicle_number=row["vehicle_number"],
            brand=row["brand"],
            model=row["model"],
            year=row["year"],
            engine_no=row["engine_no"],
            chassis_no=row["chassis_no"],
            vehicle_type=row["vehicle_type"] if "vehicle_type" in row.keys() and row["vehicle_type"] else "Car",
            registration_date=row["registration_date"] if "registration_date" in row.keys() and row["registration_date"] else "",
        )

    def create_vehicle(self, vehicle: Vehicle):
        conn = get_db_connection()
        try:
            cursor = conn.execute(
                """
                INSERT INTO vehicles (
                    vehicle_id, customer_id, vehicle_number, brand, model, year, engine_no, chassis_no, vehicle_type, registration_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    vehicle.vehicle_id,
                    vehicle.customer_id,
                    vehicle.vehicle_number,
                    vehicle.brand,
                    vehicle.model,
                    vehicle.year,
                    vehicle.engine_no,
                    vehicle.chassis_no,
                    vehicle.vehicle_type,
                    vehicle.registration_date,
                ),
            )
            conn.commit()
            vehicle.id = cursor.lastrowid
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def get_all_vehicles(self):
        conn = get_db_connection()
        try:
            rows = conn.execute(
                """
                SELECT id, vehicle_id, customer_id, vehicle_number, brand, model, year, engine_no, chassis_no, vehicle_type, registration_date
                FROM vehicles
                ORDER BY id DESC
                """
            ).fetchall()
            return [self._map_row(row) for row in rows]
        finally:
            conn.close()

    def get_vehicles_by_user_id(self, user_id: str):
        conn = get_db_connection()
        try:
            rows = conn.execute(
                """
                SELECT id, vehicle_id, customer_id, vehicle_number, brand, model, year, engine_no, chassis_no, vehicle_type, registration_date
                FROM vehicles
                WHERE customer_id = ?
                ORDER BY id DESC
                """,
                (user_id,)
            ).fetchall()
            return [self._map_row(row) for row in rows]
        finally:
            conn.close()

    def find_by_vehicle_id(self, vehicle_id: str):
        conn = get_db_connection()
        try:
            row = conn.execute(
                """
                SELECT id, vehicle_id, customer_id, vehicle_number, brand, model, year, engine_no, chassis_no, vehicle_type, registration_date
                FROM vehicles
                WHERE vehicle_id = ?
                LIMIT 1
                """,
                (vehicle_id,)
            ).fetchone()
            if not row:
                return None
            return self._map_row(row)
        finally:
            conn.close()

