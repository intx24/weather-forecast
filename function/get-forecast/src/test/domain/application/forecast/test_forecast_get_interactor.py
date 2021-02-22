from http import HTTPStatus
from unittest import TestCase
from unittest.mock import Mock

from lib.domain.application.forecast.forecast_get_interactor import ForecastGetInteractor
from lib.domain.domain.forecast.forecast import Forecast
from lib.infrastructure.forecast.forecast_repository import ForecastRepository
from lib.usecase.forecast.get.forecast_get_request import ForecastGetRequest
from lib.usecase.forecast.get.forecast_get_response import ForecastGetResponse


class TestForecastGetInteractor(TestCase):
    __repository_mock = Mock(spec=ForecastRepository)

    def test_handle__ok(self):
        # noinspection PyTypeChecker
        self.__repository_mock.get_by_city.return_value = Forecast(
            public_time='public_time1',
            public_time_format=None,
            link=None,
            title=None,
            location=None,
            forecasts=[],
            description=None,
        )
        interactor = ForecastGetInteractor(self.__repository_mock)

        request: ForecastGetRequest = ForecastGetRequest(
            city=1
        )
        actual = interactor.handle(request)

        # noinspection PyTypeChecker
        expected: ForecastGetResponse = ForecastGetResponse(
            statusCode=HTTPStatus.OK,
            errors=[],
            forecast=Forecast(
                public_time='public_time1',
                public_time_format=None,
                link=None,
                title=None,
                location=None,
                forecasts=[],
                description=None,
            )
        )
        self.assertEqual(expected, actual)

    def test_handle__raise(self):
        # noinspection PyTypeChecker
        self.__repository_mock.get_by_city.side_effect = Exception('error')
        interactor = ForecastGetInteractor(self.__repository_mock)

        request: ForecastGetRequest = ForecastGetRequest(
            city=1
        )

        actual: ForecastGetResponse = interactor.handle(request)
        expected: ForecastGetResponse = ForecastGetResponse(
            statusCode=HTTPStatus.INTERNAL_SERVER_ERROR,
            errors=['error'],
            forecast=None,
        )
        self.assertEqual(expected.statusCode, actual.statusCode)
        self.assertTrue('error' in actual.errors[0])
        self.assertEqual(expected.forecast, actual.forecast)
