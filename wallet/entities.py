from base64 import b64encode
from dataclasses import InitVar, asdict, dataclass, field
import hashlib
import hmac
from typing import Generic, TypeVar
import uuid

from utils import BOT_TG_URL, WALLET_TG_URL
from .enums import CurrencyCode


@dataclass
class MoneyAmount:
    amount: float
    currencyCode: str = CurrencyCode.USD

    def __post_init__(self) -> None:
        self.amount = float(self.amount)
    
    def __str__(self):
        return f'{self.amount} {self.currencyCode}'


@dataclass
class PaymentRequest:
    amount: MoneyAmount
    customerTelegramUserId: int
    description: str
    externalId: str = field(default_factory=uuid.uuid4)
    timeoutSeconds: int = field(default=10800, repr=False)
    returnUrl: str = field(default=BOT_TG_URL, repr=False)
    failReturnUrl: str = field(default=WALLET_TG_URL, repr=False)
    customData: str | None = None

    def __post_init__(self) -> None:
        self.externalId = str(self.externalId)
        assert len(self.description) in range(5, 101), 'DDDD'


@dataclass
class OrderPreview:
    id: str
    status: str
    number: str
    amount: MoneyAmount
    createdDateTime: str
    expirationDateTime: str
    payLink: str
    directPayLink: str
    completedDateTime: str | None = None

    def __post_init__(self) -> None:
        self.amount = MoneyAmount(**self.amount)
    
    def convert_database_appropriate(self) -> tuple:
        t = self.id, self.status, self.number, str(self.amount), self.createdDateTime, \
            self.expirationDateTime, self.payLink, self.directPayLink, self.completedDateTime
        return t


@dataclass
class PaymentOption:
    amount: MoneyAmount
    amountFee: MoneyAmount
    amountNet: MoneyAmount
    exchangeRate: float

    def __post_init__(self) -> None:
        self.amount = MoneyAmount(**self.amount)
        self.amountFee = MoneyAmount(**self.amountFee)
        self.amountNet = MoneyAmount(**self.amountNet)
        self.exchangeRate = float(self.exchangeRate)
    


@dataclass
class OrderReconciliationItem:
    id: str
    status: str
    amount: MoneyAmount
    externalId: str
    createdDateTime: str
    expirationDateTime: str
    customerTelegramUserId: int | None = None
    paymentDateTime: str | None = None
    selectedPaymentOption: PaymentOption | None = None

    def __post_init__(self) -> None:
        self.amount = MoneyAmount(**self.amount)
        if self.selectedPaymentOption:
            self.selectedPaymentOption = PaymentOption(**self.selectedPaymentOption)
    

@dataclass
class OrderList:
    items: list[OrderReconciliationItem]

    def __post_init__(self) -> None:
        self.items = [OrderReconciliationItem(**item) for item in self.items]


@dataclass
class OrderAmount:
    totalAmount: int


TResponse = TypeVar('TResponse', OrderPreview, OrderList, OrderAmount)


@dataclass
class WalletResponse(Generic[TResponse]):
    status: str
    message: str | None = None
    data: TResponse | None = None
    member_class: InitVar[type[TResponse]] = OrderPreview

    def __post_init__(self, member_class: type[TResponse]) -> None:
        if self.data:
            self.data = member_class(**self.data)


@dataclass
class WebhookPayload:
    id: int
    number: str
    externalId: str
    orderAmount: MoneyAmount
    orderCompletedDateTime: str
    status: str | None = None
    customData: str | None = None
    selectedPaymentOption: PaymentOption | None = None

    def __post_init__(self) -> None:
        self.orderAmount = MoneyAmount(**self.orderAmount)
        if self.selectedPaymentOption:
            self.selectedPaymentOption = PaymentOption(**self.selectedPaymentOption)
    

@dataclass
class Update:
    eventDateTime: str 
    eventId: int
    type: str
    payload: WebhookPayload

    def __post_init__(self) -> None:
        self.payload = WebhookPayload(**self.payload)

    @staticmethod
    def compute_signature(api_key: str, method: str, uri: str,
                          timestamp: str, body: str) -> str:
        b64encoded = b64encode(body.encode()).decode()
        sign = f'{method}.{uri}.{timestamp}.{b64encoded}'
        _hmac = hmac.new(api_key.encode(), sign.encode(), digestmod=hashlib.sha256)
        return b64encode(_hmac.digest()).decode()