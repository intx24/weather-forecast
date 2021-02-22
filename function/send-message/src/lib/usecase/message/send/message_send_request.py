from dataclasses import dataclass


@dataclass(frozen=True)
class MessageSendRequest:
    token: str
    channel: str
    link_names: bool
    text: str
    user_name: str
    icon_emoji: str = None
    icon_url: str = None
