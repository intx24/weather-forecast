from http import HTTPStatus
from unittest import TestCase
from unittest.mock import Mock

from lib.domain.application.forecast.forecast_get_interactor import ForecastGetInteractor
from lib.domain.domain.forecast.forecast import Forecast, DayForecast, Temperature, CelsiusAndFahrenheit, ChanceOfRain, \
    Description, Location
from lib.infrastructure.forecast.forecast_repository import ForecastRepository
from lib.usecase.forecast.get.forecast_get_request import ForecastGetRequest
from lib.usecase.forecast.get.forecast_get_response import ForecastGetResponse


class TestForecastGetInteractor(TestCase):
    __repository_mock = Mock(spec=ForecastRepository)

    def test_handle__ok1(self):
        # noinspection PyTypeChecker
        self.__repository_mock.get_by_city.return_value = Forecast(
            public_time='public_time1',
            public_time_formatted=None,
            publishing_office=None,
            link=None,
            title='東京都 渋谷区 の天気',
            location=Location(
                area='area',
                prefecture='東京都',
                city='渋谷区',
                district='district'
            ),
            forecasts=[DayForecast(
                date='2020-11-11',
                date_label='今日',
                detail=None,
                telop='晴れ',
                temperature=Temperature(
                    min=CelsiusAndFahrenheit(
                        celsius=1,
                        fahrenheit=2
                    ),
                    max=CelsiusAndFahrenheit(
                        celsius=30,
                        fahrenheit=40
                    )
                ),
                chance_of_rain=ChanceOfRain(
                    t00_06='1%',
                    t06_12='2%',
                    t12_18='3%',
                    t18_24='4%',
                )
            )],
            description=Description(
                headline_text='詳細です。',
                body_text='詳細ボディです',
                text='full_text',
                public_time=None,
                public_time_formatted=None,
            ),
        )
        interactor = ForecastGetInteractor(self.__repository_mock)

        request: ForecastGetRequest = ForecastGetRequest(
            city=1,
            date_label='今日',
        )
        actual = interactor.handle(request)

        # noinspection PyTypeChecker
        expected: ForecastGetResponse = ForecastGetResponse(
            statusCode=HTTPStatus.OK,
            errors=[],
            telop='晴れ',
            summary='今日 (2020-11-11) の天気\n\n'
                    + '東京都 渋谷区 '
                    + ':sunny: 晴れ :sunny:\n\n'
                    + ':japanese_goblin: > 詳細です。\n\n'
                    + '最低気温: 1 ℃ :cold_face:, '
                    + '最高気温: 30 ℃ :hot_face:\n\n'
                    + '降水確率: 00~06 = 1%, 06~12 = 2%, '
                    + '12~18 = 3%, 18~24 = 4%'
        )
        self.assertEqual(expected, actual)

    def test_handle__ok2(self):
        # noinspection PyTypeChecker
        self.__repository_mock.get_by_city.return_value = Forecast(
            public_time='public_time1',
            publishing_office=None,
            public_time_formatted=None,
            link=None,
            title='東京都 渋谷区 の天気',
            location=Location(
                area='area',
                prefecture='東京都',
                city='渋谷区',
                district='district'
            ),
            forecasts=[DayForecast(
                date='2020-11-11',
                date_label='明日',
                detail=None,
                telop='雷',
                temperature=Temperature(
                    min=None,
                    max=None,
                ),
                chance_of_rain=ChanceOfRain(
                    t00_06='1%',
                    t06_12='2%',
                    t12_18='3%',
                    t18_24='4%',
                )
            )],
            description=Description(
                headline_text='詳細です。',
                body_text='詳細ボディです',
                text='full_text',
                public_time=None,
                public_time_formatted=None,
            ),
        )
        interactor = ForecastGetInteractor(self.__repository_mock)

        request: ForecastGetRequest = ForecastGetRequest(
            city=1,
            date_label='明日'
        )
        actual = interactor.handle(request)

        # noinspection PyTypeChecker
        expected: ForecastGetResponse = ForecastGetResponse(
            statusCode=HTTPStatus.OK,
            errors=[],
            telop='雷',
            summary='明日 (2020-11-11) の天気\n\n'
                    + '東京都 渋谷区 '
                    + ':thunder_cloud_and_rain: 雷 :thunder_cloud_and_rain:\n\n'
                    + ':japanese_goblin: > 詳細です。\n\n'
                    + '最低気温: 不明, '
                    + '最高気温: 不明\n\n'
                    + '降水確率: 00~06 = 1%, 06~12 = 2%, '
                    + '12~18 = 3%, 18~24 = 4%'
        )
        self.assertEqual(expected, actual)

    def test_handle__raise(self):
        # noinspection PyTypeChecker
        self.__repository_mock.get_by_city.side_effect = Exception('error')
        interactor = ForecastGetInteractor(self.__repository_mock)

        request: ForecastGetRequest = ForecastGetRequest(
            city=1,
            date_label='今日',
        )

        actual: ForecastGetResponse = interactor.handle(request)
        expected: ForecastGetResponse = ForecastGetResponse(
            statusCode=HTTPStatus.INTERNAL_SERVER_ERROR,
            errors=['error'],
            telop=None,
            summary=None,
        )
        self.assertEqual(expected.statusCode, actual.statusCode)
        self.assertTrue('error' in actual.errors[0])
        self.assertEqual(expected.telop, actual.telop)
        self.assertEqual(expected.summary, actual.summary)
