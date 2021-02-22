import json
from http import HTTPStatus
from unittest import TestCase
from unittest.mock import Mock

from lib.domain.application.forecast.forecast_get_interactor import ForecastGetInteractor
from lib.interface.controller.forecast_controller import ForecastController
from lib.usecase.forecast.get.forecast_get_response import ForecastGetResponse


class TestForecastController(TestCase):
    __get_interactor_mock = Mock(spec=ForecastGetInteractor)

    def test_get__ok(self):
        self.__get_interactor_mock.handle.return_value = ForecastGetResponse(
            statusCode=HTTPStatus.OK,
            errors=[],
            forecast=None,
        )

        controller = ForecastController(get_interactor=self.__get_interactor_mock)
        actual = controller.get({'city': 1})

        expected = {
            'statusCode': HTTPStatus.OK,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'errors': [],
                'forecast': None
            }, default=ForecastController.default_method)
        }
        self.assertEqual(expected, actual)

    def test_get__raise_validation_exception(self):
        self.__get_interactor_mock.handle.return_value = ForecastGetResponse(
            statusCode=HTTPStatus.OK,
            errors=[],
            forecast=None,
        )

        controller = ForecastController(get_interactor=self.__get_interactor_mock)

        actual1 = controller.get({})
        self.assertEqual(HTTPStatus.BAD_REQUEST, actual1['statusCode'])
        self.assertEqual({'Content-Type': 'application/json'}, actual1['headers'])
        self.assertTrue('error' in actual1['body'])

        actual2 = controller.get({'city': ''})
        self.assertEqual(HTTPStatus.BAD_REQUEST, actual2['statusCode'])
        self.assertEqual({'Content-Type': 'application/json'}, actual2['headers'])
        self.assertTrue('error' in actual2['body'])

        actual3 = controller.get({'city': 'str'})
        self.assertEqual(HTTPStatus.BAD_REQUEST, actual3['statusCode'])
        self.assertEqual({'Content-Type': 'application/json'}, actual3['headers'])
        self.assertTrue('error' in actual3['body'])

        actual3 = controller.get({'city': None})
        self.assertEqual(HTTPStatus.BAD_REQUEST, actual3['statusCode'])
        self.assertEqual({'Content-Type': 'application/json'}, actual3['headers'])
        self.assertTrue('error' in actual3['body'])
