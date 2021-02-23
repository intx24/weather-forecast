import json
from typing import Dict

import requests

from lib.domain.domain.message.abstract_message_repository import AbstractMessageRepository
from lib.domain.domain.message.message import Message


class MessageRepository(AbstractMessageRepository):

    def __init__(self):
        pass

    def send(self, token: str, message: Message) -> bool:
        response = requests.post(
            'https://slack.com/api/chat.postMessage',
            json.dumps({
                'channel': message.channel,
                'icon_emoji': message.icon_emoji,
                'link_names': message.link_names,
                'text': message.text,
                'username': message.username,
            }, ensure_ascii=False).encode('utf-8'),
            headers={
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
        )

        response_dict: Dict = response.json()

        ok: bool = response_dict['ok']
        if not ok:
            error = response_dict['error']
            raise Exception(f'calling api was failed. error: {error}')

        return ok
