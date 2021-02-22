import json
from http import HTTPStatus
from unittest import TestCase, mock
from unittest.mock import Mock

from lib.domain.application.message.message_send_interactor import MessageSendInteractor
from lib.interface.controller.message_controller import MessageController
from lib.usecase.message.send.message_send_response import MessageSendResponse


class TestMessageController(TestCase):
    __send_interactor_mock = Mock(spec=MessageSendInteractor)

    @mock.patch('os.getenv')
    def test_send(self, mock_getenv):
        self.__send_interactor_mock.handle.return_value = MessageSendResponse(
            statusCode=HTTPStatus.OK,
            errors=[],
        )
        mock_getenv.return_value = 'TOKEN'

        controller = MessageController(self.__send_interactor_mock)
        actual1 = controller.send(event={
            'token': 'token',
            'channel': 'channel',
            'text': 'text',
            'user_name': 'user_name',
            'icon_emoji': 'icon_emoji',
            'icon_url': 'icon_url',
        })

        expected1 = {
            'statusCode': HTTPStatus.OK,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'errors': [],
            }, default=MessageController.default_method)
        }
        self.assertEqual(expected1, actual1)

        actual2 = controller.send(event={
            'token': 'token',
            'channel': 'channel',
            'text': 'text',
        })

        expected2 = {
            'statusCode': HTTPStatus.OK,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'errors': [],
            }, default=MessageController.default_method)
        }
        self.assertEqual(expected2, actual2)

    @mock.patch('os.getenv')
    def test_list__raise(self, mock_getenv):
        self.__send_interactor_mock.handle.return_value = MessageSendResponse(
            statusCode=HTTPStatus.OK,
            errors=[],
        )
        mock_getenv.side_effect = Exception('error')

        controller = MessageController(self.__send_interactor_mock)
        actual = controller.send(event={
            'channel': 'channel',
            'text': 'text',
            'user_name': 'user_name',
            'icon_emoji': 'icon_emoji',
            'icon_url': 'icon_url',
        })

        self.assertEqual(HTTPStatus.INTERNAL_SERVER_ERROR, actual['statusCode'])
        self.assertTrue('error' in actual['body'])
