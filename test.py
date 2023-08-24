import requests
import uuid
import json
str(uuid.uuid4())

d = {
    'amount': {
        'currencyCode': 'USD',
        'amount': '0.05'
    },
    'description': 'VPN for 1 month',
    'returnUrl': 'https://t.me/wallet',
    'failReturnUrl': 'https://t.me/wallet',
    'customData': 'client_ref=4E89',
    'externalId': str(uuid.uuid4()),
    'timeoutSeconds': 10800,
    'customerTelegramUserId': 0
}

headers = {
    'Wpay-Store-Api-Key': '0YzKF2xlOVXIxotj5EtF86APbFWMxhUtrbQw',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

r = requests.post('https://pay.wallet.tg/wpay/store-api/v1/order', headers=headers, data=json.dumps(d))