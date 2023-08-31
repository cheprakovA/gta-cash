from dataclasses import dataclass, asdict, fields, is_dataclass
import json
import uuid

from wallet.entities import MoneyAmount
from wallet.enums import OperationStatus
from .enums import Platform


class UnpackDCMixin:
    def __iter__(self):
        if not is_dataclass(self):
            raise TypeError(f'this mixin is dataclass-only, not {type(self)}')
        return (getattr(self, field.name) for field in fields(self))


@dataclass
class UserData:
    platform: Platform
    username: str
    password: str
    recovery_codes: str

    def __str__(self) -> str:
        return json.dumps(asdict(self))


@dataclass
class OrderData(UnpackDCMixin):
    id: str
    user_id: int
    item_id: int
    externalId: uuid.UUID | str
    user_data: UserData | dict
    status: OperationStatus
    number: str
    amount: MoneyAmount | dict | float
    createdDateTime: str
    expirationDateTime: str
    payLink: str
    directPayLink: str
    completedDateTime: str | None = None

    def __post_init__(self) -> None:
        self.externalId = str(self.externalId)
        if not isinstance(self.user_data, UserData):
            self.user_data = UserData(**self.user_data)
        if not isinstance(self.amount, MoneyAmount):
            if isinstance(self.amount, float):
                self.amount = MoneyAmount(amount=self.amount)
            else:
                self.amount = MoneyAmount(**self.amount)

    # def convert_database_appropriate(self) -> tuple:
    #     res = self.id, self.user_id, self.item_id, self.externalId, self.user_data, \
    #           self.status, self.number, self.amount, self.createdDateTime, \
    #           self.expirationDateTime, self.payLink, self.directPayLink, self.completedDateTime
    #     return res


              