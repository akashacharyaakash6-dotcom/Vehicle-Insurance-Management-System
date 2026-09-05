from dataclasses import dataclass

@dataclass
class User:
    username: str
    email: str
    password: str
    user_id: str = None
    mobile: str = None
    address: str = None
    role: str = "customer"
    secret_code: str = "AGENT789"
    id: int = None


