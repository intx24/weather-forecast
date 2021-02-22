import traceback
from http import HTTPStatus

from lib.domain.domain.forecast.abstract_forecast_repository import AbstractForecastRepository
from lib.domain.domain.forecast.forecast import Forecast
from lib.usecase.forecast.get.abstract_forecast_get_usecase import AbstractForecastGetUseCase
from lib.usecase.forecast.get.forecast_get_request import ForecastGetRequest
from lib.usecase.forecast.get.forecast_get_response import ForecastGetResponse


class ForecastGetInteractor(AbstractForecastGetUseCase):
    __repository = AbstractForecastRepository

    def __init__(self, repository: AbstractForecastRepository):
        self.__repository = repository

    def handle(self, request: ForecastGetRequest) -> ForecastGetResponse:
        try:
            forecast: Forecast = self.__repository.get_by_city(request.city)
            response: ForecastGetResponse = ForecastGetResponse(
                statusCode=HTTPStatus.OK,
                errors=[],
                forecast=forecast,
            )
            return response
        except Exception as e:
            e_message = ''.join(traceback.TracebackException.from_exception(e).format())

            response: ForecastGetResponse = ForecastGetResponse(
                statusCode=HTTPStatus.INTERNAL_SERVER_ERROR,
                errors=[e_message],
                forecast=None,
            )

            return response
