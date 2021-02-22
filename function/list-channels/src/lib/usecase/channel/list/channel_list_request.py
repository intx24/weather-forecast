from dataclasses import dataclass


@dataclass(frozen=True)
class ChannelListRequest:
    token: str
