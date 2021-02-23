import json
import os
import traceback
from http import HTTPStatus
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
        try:
            token = os.getenv('BOT_USER_TOKEN', None)
        except Exception as e:
            e_message = ''.join(traceback.TracebackException.from_exception(e).format())

            return {
                'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'errors': [e_message],
                }, default=MessageController.default_method,
                    ensure_ascii=False)
            }

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
