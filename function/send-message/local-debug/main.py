import json

import requests

PORT: int = 8082
URL: str = f'http://localhost:{PORT}/2015-03-31/functions/function/invocations'


def call(url):
    res = requests.post(
        url,
        json.dumps({
            'body': {
                'username': '天気予報Bot(テスト)',
                'telop': '晴れ',
                'summary': '今日(2021-02-23)の 佐賀県 伊万里 の天気\\n晴のち曇\\n最低気温: 不明\\n最高気温: 15.0 度\\n降水確率: 00-06=--%, 06-12=--%, '
                           '12-18=0%, 18-24=0%',
            }
        }).encode('utf-8'),
        headers={'Content-Type': 'application/json'})
    print(res.json())


if __name__ == '__main__':
    call(url=URL)
