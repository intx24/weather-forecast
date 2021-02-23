from typing import List
from unittest import TestCase, mock

from lib.domain.domain.channel.abstract_channel_repository import AbstractChannelRepository
from lib.domain.domain.channel.channel import Channel
from lib.infrastructure.channel.channel_repository import ChannelRepository


class MockResponse:
    def __init__(self, json_data):
        self.json_data = json_data

    def json(self):
        return self.json_data


class TestChannelRepository(TestCase):
    __repository: AbstractChannelRepository

    def setUp(self) -> None:
        self.__repository = ChannelRepository()

    @mock.patch('requests.get')
    def test_list__ok(self, mock_get):
        response: MockResponse = MockResponse({
            'ok': True,
            'channels': [{
                'id': 'id1',
                'name': 'name1',
                'is_private': True,
            }]
        })
        mock_get.return_value = response

        expected: List[Channel] = [Channel(
            id='id1',
            name='name1',
            is_private=True
        )]
        actual = self.__repository.list('token')
        self.assertEqual(expected, actual)

    @mock.patch('requests.get')
    def test_list__not_ok(self, mock_get):
        response: MockResponse = MockResponse({
            'ok': False,
            'error': 'message',
        })
        mock_get.return_value = response

        with self.assertRaises(Exception):
            self.__repository.list('token')
