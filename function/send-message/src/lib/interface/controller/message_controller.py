import json
import os
from typing import Dict

from lib.usecase.message.send.abstract_message_send_usecase import AbstractMessageSendUseCase
from lib.usecase.message.send.message_send_request import MessageSendRequest


class MessageController:
    __message_send_interactor: AbstractMessageSendUseCase

    @staticmethod
    def default_method(item):
        if isinstance(item, object) and hasattr(item, '__dict__'):
            return item.__dict__
        else:
            raise TypeError

    def __init__(self, message_send_interactor: AbstractMessageSendUseCase):
        self.__message_send_interactor = message_send_interactor

    def send(self, event: Dict) -> Dict:
        token = os.getenv('BOT_USER_TOKEN', None)

        telop: str = event['telop'] if 'telop' in event else ''
        summary: str = event['summary'] if 'summary' in event else ''
        r_summary: str = summary.replace('\\n', '\n')
        request = MessageSendRequest(
            token=token,
            summary=r_summary,
            telop=telop,
        )
        response = self.__message_send_interactor.handle(request)

        return {
            'statusCode': response.statusCode,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'errors': response.errors,
            },
                default=MessageController.default_method,
                ensure_ascii=False)
        }
