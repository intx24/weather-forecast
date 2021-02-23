from typing import List, Dict

import requests as requests

from lib.domain.domain.channel.abstract_channel_repository import AbstractChannelRepository
from lib.domain.domain.channel.channel import Channel


class ChannelRepository(AbstractChannelRepository):

    def __init__(self):
        pass

    def list(self, token: str) -> List[Channel]:
        response = requests.get(
            'https://slack.com/api/users.conversations',
            params={
                'token': token,
                'exclude_archived': True,
                'types': 'public_channel, private_channel',
            })

        response_dict: Dict = response.json()

        ok: bool = response_dict['ok']
        if not ok:
            error = response_dict['error']
            raise Exception(f'calling api was failed. error: {error}')

        channel_list: List[Channel] = []
        for c in response_dict['channels']:
            channel: Channel = Channel(
                id=c['id'],
                name=c['name'],
                is_private=c['is_private'],
            )
            channel_list.append(channel)

        return channel_list
