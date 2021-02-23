from dataclasses import dataclass


@dataclass(frozen=True)
class MessageSendRequest:
    token: str
    text: str
    telop: str
