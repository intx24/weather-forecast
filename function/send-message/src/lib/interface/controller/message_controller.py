import json
import os
import traceback
from http import HTTPStatus
from typing import Dict

from lib.usecase.message.send.abstract_message_send_usecase import AbstractMessageSendUseCase
from lib.usecase.message.send.message_send_request import MessageSendRequest


class MessageController:
    __send_interactor: AbstractMessageSendUseCase

    @staticmethod
    def default_method(item):
        if isinstance(item, object) and hasattr(item, '__dict__'):
            return item.__dict__
        else:
            raise TypeError

    def __init__(self, send_interactor: AbstractMessageSendUseCase):
        self.__send_interactor = send_interactor

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

        request = MessageSendRequest(
            token=token,
            channel=event['channel'],
            link_names=True,
            text=event['text'],
            user_name=event['user_name'] if 'user_name' in event else 'weather_bot',
            icon_emoji=event['icon_emoji'] if 'icon_emoji' in event else None,
            icon_url=event['icon_url'] if 'icon_url' in event else None,
        )
        response = self.__send_interactor.handle(request)
        print(response)

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
