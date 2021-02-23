import json

from lib.domain.application.forecast.forecast_get_interactor import ForecastGetInteractor
from lib.infrastructure.forecast.forecast_repository import ForecastRepository
from lib.interface.controller.forecast_controller import ForecastController


def handler(event, context):
    print('========start get-forecast========')
    print('event:' + json.dumps(event, ensure_ascii=False))

    forecast_controller = ForecastController(
        get_interactor=ForecastGetInteractor(ForecastRepository())
    )
    response = forecast_controller.get(event)

    print('response:' + json.dumps(response, ensure_ascii=False))
    print('========end get-forecast========')
    return response
