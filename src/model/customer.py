from dataclasses import dataclass


@dataclass
class Customer:
    customer_id: str
    name: str
    email: str
    phone: str
    address: str
    dob: str
    license_no: str
    id: int = None
