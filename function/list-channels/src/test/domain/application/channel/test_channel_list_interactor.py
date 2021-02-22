from http import HTTPStatus
from unittest import TestCase
from unittest.mock import Mock

from lib.domain.application.channel.channel_list_interactor import ChannelListInteractor
from lib.domain.domain.channel.channel import Channel
from lib.infrastructure.channel.channel_repository import ChannelRepository
from lib.usecase.channel.list.channel_list_request import ChannelListRequest
from lib.usecase.channel.list.channel_list_response import ChannelListResponse


class TestChannelListInteractor(TestCase):
    __repository_mock = Mock(spec=ChannelRepository)

    def test_handle__ok(self):
        channel_list = [Channel(
            id='id1',
            name='name1',
            is_private=True
        )]
        self.__repository_mock.list.return_value = channel_list
        interactor = ChannelListInteractor(self.__repository_mock)

        request = ChannelListRequest(token='token')
        actual = interactor.handle(request)
        expected = ChannelListResponse(
            statusCode=HTTPStatus.OK,
            errors=[],
            channel_list=channel_list
        )
        self.assertEqual(expected, actual)

    def test_handle__raise(self):
        self.__repository_mock.list.side_effect = Exception('error')
        interactor = ChannelListInteractor(self.__repository_mock)

        request = ChannelListRequest(token='token')

        actual = interactor.handle(request)
        expected = ChannelListResponse(
            statusCode=HTTPStatus.INTERNAL_SERVER_ERROR,
            errors=['error'],
            channel_list=[]
        )
        self.assertEqual(expected.statusCode, actual.statusCode)
        self.assertTrue('error' in actual.errors[0])
        self.assertEqual(expected.channel_list, actual.channel_list)
