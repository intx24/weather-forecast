import json

from lib.domain.application.message.message_send_interactor import MessageSendInteractor
from lib.infrastructure.channel.channel_repository import ChannelRepository
from lib.infrastructure.message.message_repository import MessageRepository
from lib.interface.controller.message_controller import MessageController


def handler(event, context):
    print('========start send-message========')
    print('event:' + json.dumps(event, ensure_ascii=False))

    message_controller = MessageController(
        message_send_interactor=MessageSendInteractor(
            ChannelRepository(),
            MessageRepository(),
        )
    )
    response = message_controller.send(event)

    print('response:' + json.dumps(response, ensure_ascii=False))
    print('========end send-message========')
    return response
