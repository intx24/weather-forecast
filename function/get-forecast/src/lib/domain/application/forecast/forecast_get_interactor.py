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
    def to_summary(forecast: Forecast, day_forecast: DayForecast):
        min_temp = f'{day_forecast.temperature.min.celsius} 度' if day_forecast.temperature.min is not None else '不明'
        max_temp = f'{day_forecast.temperature.max.celsius} 度' if day_forecast.temperature.max is not None else '不明'
        return f'{day_forecast.date_label}({day_forecast.date})の {forecast.title}\n' \
            + f'{day_forecast.telop}\n' \
            + f'最低気温: {min_temp}\n' \
            + f'最高気温: {max_temp}\n' \
            + f'降水確率: 00-06={day_forecast.chance_of_rain.t00_06}, ' \
            + f'06-12={day_forecast.chance_of_rain.t06_12}, ' \
            + f'12-18={day_forecast.chance_of_rain.t12_18}, ' \
            + f'18-24={day_forecast.chance_of_rain.t18_24}'

    def handle(self, request: ForecastGetRequest) -> ForecastGetResponse:
        try:
            forecast: Forecast = self.__repository.get_by_city(request.city)
            today_forecast = next(filter(lambda f: f.date_label == '今日', forecast.forecasts), None)

            if today_forecast is None:
                raise Exception('today forecast is not inlucded.')

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
