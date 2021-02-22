import traceback
from http import HTTPStatus

from lib.domain.domain.message.abstract_message_repository import AbstractMessageRepository
from lib.domain.domain.message.message import Message
from lib.usecase.message.send.abstract_message_send_usecase import AbstractMessageSendUseCase
from lib.usecase.message.send.message_send_request import MessageSendRequest
from lib.usecase.message.send.message_send_response import MessageSendResponse


class MessageSendInteractor(AbstractMessageSendUseCase):
    __repository: AbstractMessageRepository

    def __init__(self, repository: AbstractMessageRepository):
        self.__repository = repository

    def handle(self, request: MessageSendRequest) -> MessageSendResponse:
        try:
            message = Message(
                text=request.text,
                channel=request.channel,
                user_name=request.user_name,
                link_names=request.link_names,
                icon_url=request.icon_url,
                icon_emoji=request.icon_emoji,
            )
            self.__repository.send(request.token, message)
            response = MessageSendResponse(
                statusCode=HTTPStatus.OK,
                errors=[],
            )
            return response
        except Exception as e:
            e_message = ''.join(traceback.TracebackException.from_exception(e).format())

            response = MessageSendResponse(
                statusCode=HTTPStatus.INTERNAL_SERVER_ERROR,
                errors=[e_message],
            )

            return response
