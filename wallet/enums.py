class CurrencyCode:
    TON  = 'TON'
    BTC  = 'BTC'
    USDT = 'USDT'
    EUR  = 'EUR'
    USD  = 'USD'
    RUB  = 'RUB'


class OperationResultStatus:
    SUCCESS = 'SUCCESS' 
    INVALID_REQUEST = 'INVALID_REQUEST' 
    INTERNAL_ERROR = 'INTERNAL_ERROR'


class OrderStatus:
    ACTIVE = 'ACTIVE' 
    EXPIRED = 'EXPIRED' 
    PAID = 'PAID' 
    CANCELLED ='CANCELLED'



class WebhookMessageType:
    ORDER_FAILED = 'ORDER_FAILED' 
    ORDER_PAID = 'ORDER_PAID'