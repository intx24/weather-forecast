from unittest import TestCase, mock

from lib.domain.domain.forecast.abstract_forecast_repository import AbstractForecastRepository
from lib.domain.domain.forecast.forecast import Forecast, Description, DayForecast, Temperature, CelsiusAndFahrenheit, \
    ChanceOfRain, Location, Detail
from lib.infrastructure.forecast.forecast_repository import ForecastRepository


class MockResponse:
    def __init__(self, json_data):
        self.json_data = json_data

    def json(self):
        return self.json_data


class TestForecastRepository(TestCase):
    __repository: AbstractForecastRepository

    def setUp(self) -> None:
        self.__repository = ForecastRepository()

    @mock.patch('requests.get')
    def test_get_by_city(self, mock_get):
        response: MockResponse = MockResponse({
            'publicTime': 'publicTime1',
            'publicTimeFormatted': 'publicTime_format1',
            'publishingOffice': 'po1',
            'title': 'title1',
            'link': 'https://www.jma.go.jp/jp/yoho/346.html',
            'description': {
                'text': 'text1',
                'publicTime': 'publicTime1',
                'publicTimeFormatted': 'publicTime_format1',
                'headlineText': 'ht1',
                'bodyText': 'bt1',
            },
            'forecasts': [{
                'date': 'date1',
                'dateLabel': '今日',
                'detail': {
                    'weather': '晴れ',
                    'wind': '北の風',
                    'wave': '０．５メートル'
                },
                'telop': '晴のち曇',
                'temperature': {'min': {
                    'celsius': '7',
                    'fahrenheit': '44.6'
                },
                    'max': {
                        'celsius': '16',
                        'fahrenheit': '60.8'
                    }
                },
                'chanceOfRain': {
                    'T00_06': '10%',
                    'T06_12': '20%',
                    'T12_18': '30%',
                    'T18_24': '40%'
                },
            }],
            'location': {
                'city': '久留米',
                'area': '九州',
                'prefecture': '福岡県',
                'district': '筑後地方',
            }
        })
        mock_get.return_value = response

        expected = Forecast(
            public_time='publicTime1',
            public_time_formatted='publicTime_format1',
            publishing_office='po1',
            title='title1',
            link='https://www.jma.go.jp/jp/yoho/346.html',
            description=Description(
                text='text1',
                public_time='publicTime1',
                public_time_formatted='publicTime_format1',
                headline_text='ht1',
                body_text='bt1',
            ),
            forecasts=[DayForecast(
                date='date1',
                date_label='今日',
                detail=Detail(
                    weather='晴れ',
                    wind='北の風',
                    wave='０．５メートル',
                ),
                telop='晴のち曇',
                temperature=Temperature(
                    min=CelsiusAndFahrenheit(
                        celsius=7,
                        fahrenheit=44.6,
                    ),
                    max=CelsiusAndFahrenheit(
                        celsius=16,
                        fahrenheit=60.8,
                    ),
                ),
                chance_of_rain=ChanceOfRain(
                    t00_06='10%',
                    t06_12='20%',
                    t12_18='30%',
                    t18_24='40%',
                ),
            )],
            location=Location(
                city='久留米',
                area='九州',
                prefecture='福岡県',
                district='筑後地方',
            )
        )

        actual = self.__repository.get_by_city(1)
        self.assertEqual(expected, actual)
