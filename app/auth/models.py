from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class User:
    uid: str
    email: str
    first_name: str
    last_name: str
    study_preferences: List[str]
    goals: Dict[str, str]
