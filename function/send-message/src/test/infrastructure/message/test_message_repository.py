from unittest import TestCase, mock

from lib.domain.domain.message.abstract_message_repository import AbstractMessageRepository
from lib.domain.domain.message.message import Message
from lib.infrastructure.message.message_repository import MessageRepository


class MockResponse:
    def __init__(self, json_data):
        self.json_data = json_data

    def json(self):
        return self.json_data


class TestMessageRepository(TestCase):
    __repository: AbstractMessageRepository

    def setUp(self) -> None:
        self.__repository = MessageRepository()

    @mock.patch('requests.post')
    def test_send__ok(self, mock_post):
        response: MockResponse = MockResponse({
            'ok': True,
        })
        mock_post.return_value = response

        message = Message(
            icon_emoji=':sun:',
            username='username',
            text='text',
            link_names=True,
            channel='channel',
        )
        actual = self.__repository.send('token', message)
        self.assertTrue(actual)

    @mock.patch('requests.post')
    def test_send__not_ok(self, mock_post):
        response: MockResponse = MockResponse({
            'ok': False,
        })
        mock_post.return_value = response

        message = Message(
            icon_emoji='icon_emoji',
            username='username',
            text='text',
            link_names=True,
            channel='channel',
        )
        with self.assertRaises(Exception):
            self.__repository.send('token', message)
