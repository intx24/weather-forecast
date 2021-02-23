from http import HTTPStatus
from typing import List

from lib.domain.domain.channel.abstract_channel_repository import AbstractChannelRepository
from lib.domain.domain.channel.channel import Channel
from lib.domain.domain.message.abstract_message_repository import AbstractMessageRepository
from lib.domain.domain.message.message import Message
from lib.usecase.message.send.abstract_message_send_usecase import AbstractMessageSendUseCase
from lib.usecase.message.send.message_send_request import MessageSendRequest
from lib.usecase.message.send.message_send_response import MessageSendResponse


class MessageSendInteractor(AbstractMessageSendUseCase):
    __channel_repository: AbstractChannelRepository
    __message_repository: AbstractMessageRepository

    def __init__(self, channel_repository: AbstractChannelRepository, message_repository: AbstractMessageRepository):
        self.__channel_repository = channel_repository
        self.__message_repository = message_repository

    @staticmethod
    def get_icon_emoji(telop: str):
        if '晴' in telop:
            return ':sunny:'
        elif '風' in telop:
            return ':tornado_cloud:'
        elif '雷' in telop:
            return ':thunder_cloud_and_rain:'
        elif '雨' in telop:
            return ':rain_cloud:'
        elif '曇' in telop:
            return ':cloud:'
        else:
            return ':sunny:'

    def handle(self, request: MessageSendRequest) -> MessageSendResponse:
        channel_list: List[Channel] = self.__channel_repository.list(request.token)
        channel_name_list: List[str] = [c.name for c in channel_list]

        for n in channel_name_list:
            message = Message(
                text=request.summary,
                channel=n,
                username='天気予報Bot',
                link_names=True,
                icon_emoji=MessageSendInteractor.get_icon_emoji(request.telop),
            )
            print(message)
            # TODO: 非同期で並列に走らせる
            self.__message_repository.send(request.token, message)

        response = MessageSendResponse(
            statusCode=HTTPStatus.OK,
            errors=[],
        )
        return response
