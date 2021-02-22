import json

from lib.domain.application.channel.channel_list_interactor import ChannelListInteractor
from lib.infrastructure.channel.channel_repository import ChannelRepository
from lib.interface.controller.channel_controller import ChannelController


def handler(event, context):
    print('========start list-channels========')
    print('event:' + json.dumps(event, ensure_ascii=False))

    channel_controller = ChannelController(
        list_interactor=ChannelListInteractor(ChannelRepository())
    )
    response = channel_controller.list()

    print('response:' + json.dumps(response, ensure_ascii=False))
    print('========end list-channels========')
    return response
