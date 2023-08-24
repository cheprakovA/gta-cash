from dataclasses import dataclass
import json
from typing import Literal


@dataclass
class UserData:
    platform: Literal['ps4', 'ps5', 'xboxsex', 'xboxone']
    username: str
    password: str
    recovery_codes: str
    
    @classmethod
    def from_dict(cls, data: dict) -> 'UserData':
        obj = cls(data['platform'], 
                  data['username'], 
                  data['password'], 
                  data['recovery_codes'])
        return obj

    def __repr__(self) -> str:
        return json.dumps(self.__dict__)


@dataclass
class MoneyAmount:
    currencyCode: str
    amount: str
    
    @classmethod
    def from_dict(cls, data) -> None:
        obj = cls(currencyCode = data.currencyCode,
                  amount = data.amount)
        return obj
    
    def __repr__(self) -> str:
        return json.dumps(self.__dict__)


@dataclass
class TempOrder:
    id: str
    number: str
    # amount: MoneyAmount
    created_dt: str
    expiration_dt: str
    pay_link: str
    direct_pay_link: str

    @classmethod
    def from_dict(cls, data: dict) -> 'TempOrder':
        obj = cls(data['id'], 
                  data['number'], 
                #   MoneyAmount.from_dict(data['amount']),
                  data['createdDateTime'], 
                  data['expirationDateTime'], 
                  data['payLink'], 
                  data['directPayLink'])
        return obj

    def __repr__(self) -> str:
        return json.dumps(self.__dict__)
