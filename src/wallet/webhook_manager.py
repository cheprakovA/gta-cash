from fastapi import FastAPI, Request, HTTPException
from .entities import Event
from .enums import UpdateType
import logging
import hmac
import base64


logging.basicConfig(level=logging.INFO)


class WebhookManager:
    ALLOWED_IPS = {'172.255.248.29', '172.255.248.12', '127.0.0.1'}

    def __init__(self, api_key: str, host: str = '0.0.0.0', port: int = 9123,
                 webhook_endpoint: str = '/wp_webhoo'):
        self.successful_callbacks = []
        self.failed_callbacks = []
        self.host = host
        self.port = port
        self.api_key = api_key
        self.webhook_endpoint = '/' if webhook_endpoint[0] != '/' else '' + webhook_endpoint

        self.app = FastAPI()

    async def start(self):
        if self.app:
            import uvicorn

            self.register_webhook_endpoint()
            logging.info((f'Webhook is listening at https://{self.host}:'
                          f'{self.port}{self.webhook_endpoint}'))

            runner = uvicorn.Server(config=uvicorn.Config(self.app, 
                                                          host=self.host, 
                                                          port=self.port, 
                                                          access_log=False, 
                                                          log_level='info'))
            
            await runner.serve()

    def successful_handler(self, func):
        self.successful_callbacks.append(func)

    def failed_handler(self, func):
        self.failed_callbacks.append(func)

    async def _handle_webhook(self, request: Request):
        x_forwarded_for = request.headers.get('X-Forwarded-For')
        client_ip = x_forwarded_for or request.client.host

        logging.info(f'Incoming webhook from {client_ip}')

        if client_ip not in self.ALLOWED_IPS:
            logging.info(f'IP {client_ip} not allowed')
            raise HTTPException(status_code=403, detail='IP not allowed')

        data = await request.json()
        raw_body = await request.body()
        headers = request.headers

        signature = headers.get('Walletpay-Signature')
        timestamp = headers.get('WalletPay-Timestamp')
        method = request.method
        path = request.url.path
        message = f'{method}.{path}.{timestamp}.{base64.b64encode(raw_body).decode()}'

        expected_signature = hmac.new(
            bytes(self.api_key, 'utf-8'),
            msg=bytes(message, 'utf-8'),
            digestmod=hmac._hashlib.sha256
        ).digest()

        expected_signature_b64 = base64.b64encode(expected_signature).decode()
        if not hmac.compare_digest(expected_signature_b64, signature):
            logging.info((f'Invalid signature. Expected: {expected_signature_b64} '
                          f'Get from header: {signature}'))
            raise HTTPException(status_code=400, detail='Invalid signature')

        event = Event(**data[0])

        if event.type == UpdateType.ORDER_PAID:
            for callback in self.successful_callbacks:
                await callback(event)
            return {'message': 'Successful event processed!'}
        elif event.type == UpdateType.ORDER_FAILED:
            for callback in self.failed_callbacks:
                await callback(event)
            return {'message': 'Failed event processed!'}
        else:
            return {'message': 'Webhook received with unknown status!'}

    def register_webhook_endpoint(self, endpoint: str = '/wp_webhook'):
        self.app.post(endpoint)(self._handle_webhook)