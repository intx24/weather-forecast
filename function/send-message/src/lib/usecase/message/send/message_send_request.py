from dataclasses import dataclass


@dataclass(frozen=True)
class MessageSendRequest:
    token: str
    summary: str
    telop: str
