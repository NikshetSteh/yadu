from abc import abstractmethod
from typing import Optional

from yadu.types.request import ApiRequest
from yadu.types.response import Response


class Trigger:
    @abstractmethod
    async def on_new_message(self, message: ApiRequest) -> Optional[Response]:
        return None
