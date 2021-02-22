from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class CelsiusAndFahrenheit:
    celsius: float
    fahrenheit: float


@dataclass(frozen=True)
class Temperature:
    min: CelsiusAndFahrenheit
    max: CelsiusAndFahrenheit


@dataclass(frozen=True)
class Description:
    text: str
    public_time: str
    public_time_format: str


@dataclass(frozen=True)
class ChanceOfRain:
    t00_06: str
    t06_12: str
    t12_18: str
    t18_24: str


@dataclass(frozen=True)
class DayForecast:
    date: str
    date_label: str
    telop: str
    temperature: Temperature
    chance_of_rain: ChanceOfRain


@dataclass(frozen=True)
class Location:
    city: str
    area: str
    prefecture: str


@dataclass(frozen=True)
class Forecast:
    public_time: str
    public_time_format: str
    title: str
    link: str
    description: Description
    forecasts: List[DayForecast]
    location: Location
