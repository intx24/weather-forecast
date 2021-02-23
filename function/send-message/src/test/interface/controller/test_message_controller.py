import json
from http import HTTPStatus
from unittest import TestCase, mock
from unittest.mock import Mock

from lib.domain.application.message.message_send_interactor import MessageSendInteractor
from lib.interface.controller.message_controller import MessageController
from lib.usecase.message.send.message_send_response import MessageSendResponse


class TestMessageController(TestCase):
    __message_send_interactor_mock = Mock(spec=MessageSendInteractor)

    @mock.patch('os.getenv')
    def test_send(self, mock_getenv):
        self.__message_send_interactor_mock.handle.return_value = MessageSendResponse(
            statusCode=HTTPStatus.OK,
            errors=[],
        )
        mock_getenv.return_value = 'TOKEN'

        controller = MessageController(self.__message_send_interactor_mock)
        actual = controller.send(event={
            'token': 'token',
            'text': 'text',
            'telop': '晴れ',
        })

        expected = {
            'statusCode': HTTPStatus.OK,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'errors': [],
            }, default=MessageController.default_method)
        }
        self.assertEqual(expected, actual)

    @mock.patch('os.getenv')
    def test_list__raise(self, mock_getenv):
        self.__message_send_interactor_mock.handle.return_value = MessageSendResponse(
            statusCode=HTTPStatus.OK,
            errors=[],
        )
        mock_getenv.side_effect = Exception('error')

        controller = MessageController(self.__message_send_interactor_mock)
        actual = controller.send(event={
            'text': 'text',
            'telop': '雨',
        })

        self.assertEqual(HTTPStatus.INTERNAL_SERVER_ERROR, actual['statusCode'])
        self.assertTrue('error' in actual['body'])
