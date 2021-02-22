from abc import ABCMeta, abstractmethod

from lib.usecase.channel.list.channel_list_request import ChannelListRequest
from lib.usecase.channel.list.channel_list_response import ChannelListResponse


class AbstractChannelListUseCase(metaclass=ABCMeta):
    @abstractmethod
    def handle(self, request: ChannelListRequest) -> ChannelListResponse:
        pass
