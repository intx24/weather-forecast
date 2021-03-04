import traceback
from http import HTTPStatus

from lib.domain.domain.forecast.abstract_forecast_repository import AbstractForecastRepository
from lib.domain.domain.forecast.forecast import Forecast, DayForecast
from lib.usecase.forecast.get.abstract_forecast_get_usecase import AbstractForecastGetUseCase
from lib.usecase.forecast.get.forecast_get_request import ForecastGetRequest
from lib.usecase.forecast.get.forecast_get_response import ForecastGetResponse


class ForecastGetInteractor(AbstractForecastGetUseCase):
    __repository = AbstractForecastRepository

    def __init__(self, repository: AbstractForecastRepository):
        self.__repository = repository

    @staticmethod
    def get_icon_emoji(telop: str):
        if '晴' in telop:
            return ':sunny:'
        elif '風' in telop:
            return ':tornado_cloud:'
        elif '雷' in telop:
            return ':thunder_cloud_and_rain:'
        elif '雨' in telop:
            return ':rain_cloud:'
        elif '曇' in telop:
            return ':cloud:'
        else:
            return ':sunny:'

    @staticmethod
    def get_face_icon_by_temperature(temperature: float):
        if temperature is None:
            return ''

        if temperature <= 10:
            return ':cold_face:'
        elif temperature >= 30:
            return ':hot_face:'
        else:
            return ''

    @staticmethod
    def to_summary(forecast: Forecast, day_forecast: DayForecast):
        min_temp = '不明'
        if day_forecast.temperature.min:
            min_celsius = day_forecast.temperature.min.celsius
            min_celsius_icon = ForecastGetInteractor.get_face_icon_by_temperature(min_celsius)
            min_temp = f'{min_celsius} ℃ {min_celsius_icon}' if min_celsius is not None else '不明'

        max_temp = '不明'
        if day_forecast.temperature.max:
            max_celsius = day_forecast.temperature.max.celsius
            max_celsius_icon = ForecastGetInteractor.get_face_icon_by_temperature(max_celsius)
            max_temp = f'{max_celsius} ℃ {max_celsius_icon}' if max_celsius is not None else '不明'

        telop_icon = ForecastGetInteractor.get_icon_emoji(telop=day_forecast.telop)
        return f'{day_forecast.date} {forecast.location.prefecture} {forecast.location.city} ' \
            + f'{telop_icon} {day_forecast.telop} {telop_icon}\n\n' \
            + f':japanese_goblin: > {forecast.description.headline_text}\n\n' \
            + f'最低気温: {min_temp}, ' \
            + f'最高気温: {max_temp}\n\n' \
            + f'降水確率: 00~06 = {day_forecast.chance_of_rain.t00_06}, ' \
            + f'06~12 = {day_forecast.chance_of_rain.t06_12}, ' \
            + f'12~18 = {day_forecast.chance_of_rain.t12_18}, ' \
            + f'18~24 = {day_forecast.chance_of_rain.t18_24}'

    def handle(self, request: ForecastGetRequest) -> ForecastGetResponse:
        try:
            forecast: Forecast = self.__repository.get_by_city(request.city)
            today_forecast = next(filter(lambda f: f.date_label == '今日', forecast.forecasts), None)

            if today_forecast is None:
                raise Exception('today forecast is not inclucded.')

            response: ForecastGetResponse = ForecastGetResponse(
                statusCode=HTTPStatus.OK,
                errors=[],
                telop=today_forecast.telop,
                summary=ForecastGetInteractor.to_summary(forecast, today_forecast)
            )
            return response
        except Exception as e:
            e_message = ''.join(traceback.TracebackException.from_exception(e).format())

            response: ForecastGetResponse = ForecastGetResponse(
                statusCode=HTTPStatus.INTERNAL_SERVER_ERROR,
                errors=[e_message],
                telop=None,
                summary=None,
            )

            return response
