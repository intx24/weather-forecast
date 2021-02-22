import traceback
from http import HTTPStatus
from typing import List

from lib.domain.domain.channel.abstract_channel_repository import AbstractChannelRepository
from lib.domain.domain.channel.channel import Channel
from lib.usecase.channel.list.abstract_channel_list_usecase import AbstractChannelListUseCase
from lib.usecase.channel.list.channel_list_request import ChannelListRequest
from lib.usecase.channel.list.channel_list_response import ChannelListResponse


class ChannelListInteractor(AbstractChannelListUseCase):
    __repository = AbstractChannelRepository

    def __init__(self, repository: AbstractChannelRepository):
        self.__repository = repository

    def handle(self, request: ChannelListRequest) -> ChannelListResponse:
        try:
            channel_list: List[Channel] = self.__repository.list(request.token)
            response: ChannelListResponse = ChannelListResponse(
                statusCode=HTTPStatus.OK,
                errors=[],
                channel_list=channel_list
            )
            return response
        except Exception as e:
            e_message = ''.join(traceback.TracebackException.from_exception(e).format())

            response: ChannelListResponse = ChannelListResponse(
                statusCode=HTTPStatus.INTERNAL_SERVER_ERROR,
                errors=[e_message],
                channel_list=[],
            )

            return response
