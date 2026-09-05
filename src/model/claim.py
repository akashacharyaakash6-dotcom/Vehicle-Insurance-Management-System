from dataclasses import dataclass


@dataclass
class Claim:
    claim_id: str
    policy_id: str
    customer_name: str
    vehicle_number: str
    insurance_company: str
    accident_date: str
    claim_date: str
    claim_amount: str
    reason: str
    description: str
    status: str
    documents: str
    user_id: str = ""
    vehicle_id: str = ""
    incident_location: str = ""
    id: int = None
