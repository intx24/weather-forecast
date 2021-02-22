from typing import List

import requests

from lib.domain.domain.forecast.abstract_forecast_repository import AbstractForecastRepository
from lib.domain.domain.forecast.forecast import Forecast, Description, Temperature, CelsiusAndFahrenheit, ChanceOfRain, \
    DayForecast, Location


class ForecastRepository(AbstractForecastRepository):

    def get_by_city(self, city: int) -> Forecast:
        response = requests.get(
            'https://weather.tsukumijima.net/api/forecast',
            params={'city': city})

        response_dict = response.json()

        description: Description = Description(
            text=response_dict['description']['text'],
            public_time=response_dict['description']['publicTime'],
            public_time_format=response_dict['description']['publicTime_format'],
        )

        day_forecast_list: List[DayForecast] = []
        for f in response_dict['forecasts']:
            temperature_dict = f['temperature']
            min_dict = temperature_dict['min']
            max_dict = temperature_dict['max']
            temperature = Temperature(
                min=CelsiusAndFahrenheit(
                    celsius=float(min_dict['celsius']),
                    fahrenheit=float(min_dict['fahrenheit'])
                ) if min_dict else None,
                max=CelsiusAndFahrenheit(
                    celsius=float(max_dict['celsius']) if bool(max_dict['celsius']) else None,
                    fahrenheit=float(max_dict['fahrenheit']) if bool(max_dict['fahrenheit']) else None,
                ) if max_dict else None,
            )
            cor_dict = f['chanceOfRain']
            cor = ChanceOfRain(
                t00_06=cor_dict['00-06'],
                t06_12=cor_dict['06-12'],
                t12_18=cor_dict['12-18'],
                t18_24=cor_dict['18-24'],
            )

            day_forecast = DayForecast(
                date=f['date'],
                date_label=f['dateLabel'],
                telop=f['telop'],
                temperature=temperature,
                chance_of_rain=cor,
            )

            day_forecast_list.append(day_forecast)

        location: Location = Location(
            area=response_dict['location']['area'],
            prefecture=response_dict['location']['prefecture'],
            city=response_dict['location']['city']
        )

        forecast: Forecast = Forecast(
            public_time=response_dict['publicTime'],
            public_time_format=response_dict['publicTime_format'],
            title=response_dict['title'],
            link=response_dict['link'],
            description=description,
            forecasts=day_forecast_list,
            location=location
        )

        return forecast
