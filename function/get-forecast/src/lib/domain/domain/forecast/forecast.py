from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class Detail:
    weather: str
    wind: str
    wave: str

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
    public_time: str
    formatted_public_time: str
    headline_text: str
    body_text: str
    text: str


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
    detail: Detail
    telop: str
    temperature: Temperature
    chance_of_rain: ChanceOfRain


@dataclass(frozen=True)
class Location:
    city: str
    area: str
    district: str
    prefecture: str


@dataclass(frozen=True)
class Forecast:
    public_time: str
    formatted_public_time: str
    publishing_office: str
    title: str
    link: str
    description: Description
    forecasts: List[DayForecast]
    location: Location
