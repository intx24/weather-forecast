from dataclasses import dataclass


@dataclass(frozen=True)
class ForecastGetRequest:
    city: int
    date_label: str
