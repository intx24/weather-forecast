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
        try:
            city = int(event['city'])
        except Exception as e:
            e_message = ''.join(traceback.TracebackException.from_exception(e).format())

            return {
                'statusCode': HTTPStatus.BAD_REQUEST,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'errors': [e_message],
                    'forecast': None,
                }, default=ForecastController.default_method,
                    ensure_ascii=False)
            }

        request: ForecastGetRequest = ForecastGetRequest(city=city)
        response = self.__get_interactor.handle(request)

        x = json.dumps({
            'errors': response.errors,
            'forecast': response.forecast,
        }, default=ForecastController.default_method,
            ensure_ascii=False)

        return {
            'statusCode': response.statusCode,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'errors': response.errors,
                'forecast': response.forecast,
            },
                default=ForecastController.default_method,
                ensure_ascii=False)
        }
