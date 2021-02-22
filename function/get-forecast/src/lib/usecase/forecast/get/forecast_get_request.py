from dataclasses import dataclass


@dataclass(frozen=True)
class ForecastGetRequest:
    city: int
