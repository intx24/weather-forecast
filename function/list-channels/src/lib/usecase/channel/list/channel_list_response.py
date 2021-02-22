from dataclasses import dataclass
from typing import List

from lib.domain.domain.channel.channel import Channel


@dataclass(frozen=True)
class ChannelListResponse:
    statusCode: int
    errors: List[str]
    channel_list: List[Channel]
