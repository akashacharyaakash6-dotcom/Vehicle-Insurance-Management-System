from dataclasses import dataclass

@dataclass
class User:
    username: str
    email: str
    password: str
    id: int = None
