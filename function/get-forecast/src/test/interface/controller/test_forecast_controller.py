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
            telop=None,
            summary=None,
        )

        controller = ForecastController(get_interactor=self.__get_interactor_mock)
        actual = controller.get({'city': 1})

        expected = {
            'statusCode': HTTPStatus.OK,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': {
                'errors': [],
                'telop': None,
                'summary': None,
            }
        }
        self.assertEqual(expected, actual)
