from dataclasses import asdict
import aiohttp
import ujson
from utils import HEADERS, WALLET_API_URL
from .entities import OrderAmount, OrderList, PaymentRequest, WalletResponse


async def send_payment_request(payment_request: PaymentRequest) -> WalletResponse:
    async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
        async with session.post(f'{WALLET_API_URL}/order',
                                headers=HEADERS, 
                                json=asdict(payment_request)) as resp:
            return WalletResponse(**(await resp.json()))


async def retrieve_order_info(order_id: str) -> WalletResponse:
    url = f'{WALLET_API_URL}/order/preview?id={order_id}'
    async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
        async with session.get(url, headers=HEADERS) as resp:
            return WalletResponse(**(await resp.json()))


async def retrieve_orders_list(offset: int = 0, count: int = 100) -> WalletResponse:
    url = f'{WALLET_API_URL}/reconciliation/order-list?offset={offset}&count={count}'
    async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
        async with session.get(url, headers=HEADERS) as resp:
            return WalletResponse(**(await resp.json()), member_class=OrderList)


async def retrieve_orders_amount() -> WalletResponse:
    url = f'{WALLET_API_URL}/reconciliation/order-amount'
    async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
        async with session.get(url, headers=HEADERS) as resp:
            return WalletResponse(**(await resp.json()), member_class=OrderAmount)