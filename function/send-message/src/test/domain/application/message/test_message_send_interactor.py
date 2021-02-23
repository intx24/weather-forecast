from http import HTTPStatus
from unittest import TestCase
from unittest.mock import Mock

from lib.domain.application.message.message_send_interactor import MessageSendInteractor
from lib.domain.domain.channel.channel import Channel
from lib.infrastructure.channel.channel_repository import ChannelRepository
from lib.infrastructure.message.message_repository import MessageRepository
from lib.usecase.message.send.message_send_request import MessageSendRequest
from lib.usecase.message.send.message_send_response import MessageSendResponse


class TestMessageSendInteractor(TestCase):
    __message_repository_mock = Mock(spec=MessageRepository)
    __channel_repository_mock = Mock(spec=ChannelRepository)

    def test_handle__ok(self):
        channel_list = [Channel(
            id='id1',
            name='channel1',
            is_private=True
        )]
        self.__channel_repository_mock.list.return_value = channel_list
        self.__message_repository_mock.return_value = True
        interactor = MessageSendInteractor(self.__channel_repository_mock, self.__message_repository_mock)

        request = MessageSendRequest(
            token='token',
            summary='summary',
            telop='晴れ',
        )
        actual = interactor.handle(request)
        expected = MessageSendResponse(
            statusCode=HTTPStatus.OK,
            errors=[]
        )
        self.assertEqual(expected, actual)
