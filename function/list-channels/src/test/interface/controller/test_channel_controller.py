import json
from http import HTTPStatus
from unittest import TestCase, mock
from unittest.mock import Mock

from lib.domain.application.channel.channel_list_interactor import ChannelListInteractor
from lib.interface.controller.channel_controller import ChannelController
from lib.usecase.channel.list.channel_list_response import ChannelListResponse


class TestChannelController(TestCase):
    __list_interactor_mock = Mock(spec=ChannelListInteractor)

    @mock.patch('os.getenv')
    def test_list__ok(self, mock_getenv):
        self.__list_interactor_mock.handle.return_value = ChannelListResponse(
            statusCode=HTTPStatus.OK,
            errors=[],
            channel_list=[]
        )
        mock_getenv.return_value = 'TOKEN'

        controller = ChannelController(self.__list_interactor_mock)
        actual = controller.list()

        expected = {
            'statusCode': HTTPStatus.OK,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'errors': [],
                'channel_list': []
            }, default=ChannelController.default_method)
        }
        self.assertEqual(expected, actual)

    @mock.patch('os.getenv')
    def test_list__raise(self, mock_getenv):
        self.__list_interactor_mock.handle.return_value = ChannelListResponse(
            statusCode=HTTPStatus.OK,
            errors=[],
            channel_list=[]
        )
        mock_getenv.side_effect = Exception('error')

        controller = ChannelController(self.__list_interactor_mock)
        actual = controller.list()

        self.assertEqual(HTTPStatus.INTERNAL_SERVER_ERROR, actual['statusCode'])
        self.assertTrue('error' in actual['body'])
