from abc import ABCMeta, abstractmethod

from lib.domain.domain.message.message import Message


class AbstractMessageRepository(metaclass=ABCMeta):
    @abstractmethod
    def send(self, token: str, message: Message) -> bool:
        pass
