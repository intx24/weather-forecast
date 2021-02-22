import json

import requests

PORT: int = 8083
URL: str = f'http://localhost:{PORT}/2015-03-31/functions/function/invocations'


def call(url):
    res = requests.post(
        url,
        json.dumps({
            'channel': 'C01NUVC2N2E',
            'text': 'text',
            'user_name': 'user_name',
            'icon_emoji': ':one-sec-cooking:',
        }).encode('utf-8'),
        headers={'Content-Type': 'application/json'})
    print(res.json())


if __name__ == '__main__':
    call(url=URL)
