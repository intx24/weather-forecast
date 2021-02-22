from dataclasses import dataclass
from typing import List, Optional

from lib.domain.domain.forecast.forecast import Forecast


@dataclass(frozen=True)
class ForecastGetResponse:
    statusCode: int
    errors: List[str]
    forecast: Optional[Forecast]
