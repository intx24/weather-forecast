import json
import traceback
from http import HTTPStatus
from typing import Dict

from lib.usecase.forecast.get.abstract_forecast_get_usecase import AbstractForecastGetUseCase
from lib.usecase.forecast.get.forecast_get_request import ForecastGetRequest


class ForecastController:
    __get_interactor: AbstractForecastGetUseCase

    @staticmethod
    def default_method(item):
        if isinstance(item, object) and hasattr(item, '__dict__'):
            return item.__dict__
        else:
            raise TypeError

    def __init__(self, get_interactor: AbstractForecastGetUseCase):
        self.__get_interactor = get_interactor

    def get(self, event: Dict) -> Dict:
        city = int(event['city'])

        request: ForecastGetRequest = ForecastGetRequest(city=city)
        response = self.__get_interactor.handle(request)

        return {
            'statusCode': response.statusCode,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': {
                'errors': response.errors,
                'telop': response.telop,
                'summary': response.summary,
            }
        }
