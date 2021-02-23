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
    def test_send__ok(self, mock_getenv):
        self.__message_send_interactor_mock.handle.return_value = MessageSendResponse(
            statusCode=HTTPStatus.OK,
            errors=[],
        )
        mock_getenv.return_value = 'TOKEN'

        controller = MessageController(self.__message_send_interactor_mock)
        actual = controller.send(event={
            'token': 'token',
            'summary': 'summary',
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
