from dataclasses import asdict, dataclass, field
import json
from typing import Literal
from .enums import Platform


@dataclass
class UserData:
    platform: str
    username: str
    password: str
    recovery_codes: str

    def __repr__(self) -> str:
        return json.dumps(asdict(self))