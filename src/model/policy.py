from dataclasses import dataclass


@dataclass
class Policy:
    policy_id: str
    customer_id: str
    vehicle_id: str
    policy_type: str
    premium: str
    start_date: str
    end_date: str
    coverage: str
    status: str
    policy_number: str = ""
    expiry_date: str = ""
    id: int = None
