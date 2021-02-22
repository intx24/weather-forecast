from abc import ABCMeta, abstractmethod

from lib.domain.domain.forecast.forecast import Forecast


class AbstractForecastRepository(metaclass=ABCMeta):
    @abstractmethod
    def get_by_city(self, city: int) -> Forecast:
        pass
