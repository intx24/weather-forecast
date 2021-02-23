from dataclasses import dataclass


@dataclass(frozen=True)
class Message:
    channel: str
    link_names: bool
    text: str
    username: str
    icon_emoji: str = None
