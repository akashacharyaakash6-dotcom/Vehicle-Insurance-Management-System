from dataclasses import dataclass

@dataclass
class Payment:
    payment_id: str
    user_id: str
    policy_id: str
    amount: str
    payment_date: str
    transaction_id: str
    status: str
    id: int = None
