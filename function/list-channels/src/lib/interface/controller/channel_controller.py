import json
import os
import traceback
from http import HTTPStatus
from typing import Dict

from lib.usecase.channel.list.abstract_channel_list_usecase import AbstractChannelListUseCase
from lib.usecase.channel.list.channel_list_request import ChannelListRequest


class ChannelController:
    __list_interactor: AbstractChannelListUseCase

    @staticmethod
    def default_method(item):
        if isinstance(item, object) and hasattr(item, '__dict__'):
            return item.__dict__
        else:
            raise TypeError

    def __init__(self, list_interactor: AbstractChannelListUseCase):
        self.__list_interactor = list_interactor

    def list(self) -> Dict:
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
                    'channel_list': [],
                }, default=ChannelController.default_method,
                    ensure_ascii=False)
            }

        request = ChannelListRequest(token=token)
        response = self.__list_interactor.handle(request)
        print(response)

        return {
            'statusCode': response.statusCode,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'errors': response.errors,
                'channel_list': response.channel_list,
            },
                default=ChannelController.default_method,
                ensure_ascii=False)
        }
