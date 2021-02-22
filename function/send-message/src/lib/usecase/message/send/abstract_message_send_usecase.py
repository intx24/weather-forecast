from abc import ABCMeta, abstractmethod

from lib.usecase.message.send.message_send_request import MessageSendRequest
from lib.usecase.message.send.message_send_response import MessageSendResponse


class AbstractMessageSendUseCase(metaclass=ABCMeta):
    @abstractmethod
    def handle(self, request: MessageSendRequest) -> MessageSendResponse:
        pass
