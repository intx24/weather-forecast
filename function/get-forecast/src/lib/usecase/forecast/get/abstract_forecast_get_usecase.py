from abc import ABCMeta, abstractmethod

from lib.usecase.forecast.get.forecast_get_request import ForecastGetRequest
from lib.usecase.forecast.get.forecast_get_response import ForecastGetResponse


class AbstractForecastGetUseCase(metaclass=ABCMeta):
    @abstractmethod
    def handle(self, request: ForecastGetRequest) -> ForecastGetResponse:
        pass
