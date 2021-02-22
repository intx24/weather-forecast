from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class MessageSendResponse:
    statusCode: int
    errors: List[str]
