from typing import Dict

from lib.config.config import config


class StackUtil:
    __default_config: Dict

    def __init__(self):
        self.__default_config = config['default']

    def get_stack_name(self, stack_part: str) -> str:
        return f"{self.__default_config['system_name']}-{stack_part}".upper()

    def get_name(self, resource_part: str) -> str:
        return f"{self.__default_config['system_name']}-{resource_part}"

    def get_upper_name(self, resource_part: str) -> str:
        return f"{self.__default_config['system_name']}-{resource_part}".upper()
