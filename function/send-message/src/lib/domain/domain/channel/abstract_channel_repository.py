from abc import ABCMeta, abstractmethod
from typing import List

from lib.domain.domain.channel.channel import Channel


class AbstractChannelRepository(metaclass=ABCMeta):
    @abstractmethod
    def list(self, token: str) -> List[Channel]:
        pass
