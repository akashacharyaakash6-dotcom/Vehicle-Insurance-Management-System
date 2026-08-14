from dataclasses import dataclass


@dataclass
class Vehicle:
    vehicle_id: str
    customer_id: str
    vehicle_number: str
    brand: str
    model: str
    year: str
    engine_no: str
    chassis_no: str
    id: int = None
