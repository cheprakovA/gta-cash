from enum import Enum


class CurrencyCode(str, Enum):
    TON  = 'TON'
    BTC  = 'BTC'
    USDT = 'USDT'
    EUR  = 'EUR'
    USD  = 'USD'
    RUB  = 'RUB'


class OperationStatus(str, Enum):
    SUCCESS = 'SUCCESS' 
    INVALID_REQUEST = 'INVALID_REQUEST' 
    INTERNAL_ERROR = 'INTERNAL_ERROR'


class OrderStatus(str, Enum):
    ACTIVE = 'ACTIVE' 
    EXPIRED = 'EXPIRED' 
    PAID = 'PAID' 
    CANCELLED ='CANCELLED'


class UpdateType(str, Enum):
    ORDER_FAILED = 'ORDER_FAILED' 
    ORDER_PAID = 'ORDER_PAID'
