from abc import abstractmethod
from typing import NoReturn

from yadu.handling.request_handler import RequestHandler


class Server:
    @abstractmethod
    def run(self, request_handler: RequestHandler, host: str = "0.0.0.0", port: int = 8080,
            url: str = "/api/v1/new_message") -> NoReturn:
        pass
