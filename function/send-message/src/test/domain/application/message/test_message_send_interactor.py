from http import HTTPStatus
from unittest import TestCase
from unittest.mock import Mock

from lib.domain.application.message.message_send_interactor import MessageSendInteractor
from lib.infrastructure.message.message_repository import MessageRepository
from lib.usecase.message.send.message_send_request import MessageSendRequest
from lib.usecase.message.send.message_send_response import MessageSendResponse


class TestMessageSendInteractor(TestCase):
    __repository_mock = Mock(spec=MessageRepository)

    def test_handle__ok(self):
        self.__repository_mock.return_value = True
        interactor = MessageSendInteractor(self.__repository_mock)

        request = MessageSendRequest(
            token='token',
            text='text',
            channel='channel',
            user_name='user_name',
            link_names=True,
            icon_url='icon_url',
            icon_emoji='icon_emoji',
        )
        actual = interactor.handle(request)
        expected = MessageSendResponse(
            statusCode=HTTPStatus.OK,
            errors=[]
        )
        self.assertEqual(expected, actual)

    def test_handle__raise(self):
        self.__repository_mock.send.side_effect = Exception('error')
        interactor = MessageSendInteractor(self.__repository_mock)

        request = MessageSendRequest(
            token='token',
            text='text',
            channel='channel',
            user_name='user_name',
            link_names=True,
            icon_url='icon_url',
            icon_emoji='icon_emoji',
        )

        actual = interactor.handle(request)
        expected = MessageSendResponse(
            statusCode=HTTPStatus.INTERNAL_SERVER_ERROR,
            errors=['error'],
        )
        self.assertEqual(expected.statusCode, actual.statusCode)
        self.assertTrue('error' in actual.errors[0])
