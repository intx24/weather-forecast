import json
from base64 import b64encode
from typing import Dict
from urllib.parse import urlencode

import requests

PORT: int = 8081
URL: str = f'http://localhost:{PORT}/2015-03-31/functions/function/invocations'


def call(url):
    body = json.dumps({
        'city': 410020
    }).encode('utf-8')
    res = requests.post(
        url,
        body,
        headers={'Content-Type': 'application/json'}
    )
    print(res.json())


if __name__ == '__main__':
    call(url=URL)
