from dataclasses import dataclass


@dataclass(frozen=True)
class Channel:
    id: str
    name: str
    is_private: bool
