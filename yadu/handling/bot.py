from typing import NoReturn, Type

from yadu.handling.triggers import Trigger
from yadu.handling.request_handler import RequestHandler
from yadu.handling.post_processing import ResponsePostProcessing
from yadu.handling.state import State, UserStateConvertor
from yadu.server.server import Server
from yadu.server.aiohttp_server import AiohttpServer


class Bot:
    def __init__(self, using_server: Server = None):
        self.all_states: dict[str, Type[State]] = {}
        self.first_state = None
        self.post_processing_functions = []
        self.triggers = []
        self.server = using_server if using_server is not None else AiohttpServer()

    def set_first_state(self, state: State) -> None:
        self.first_state = state

    def state(self, state_name: str):
        def wrapper(state_class):
            if isinstance(state_class, State):
                raise ValueError("state class must be of type State")

            if state_name in self.all_states:
                raise ValueError("states names must be unique")

            self.all_states[state_name] = state_class

            return state_class

        return wrapper

    def add_post_processing_function(self, response_post_processing_function: ResponsePostProcessing) -> None:
        self.post_processing_functions.append(response_post_processing_function)

    def add_trigger(self, trigger: Trigger) -> None:
        self.triggers.append(trigger)

    def run(self, host: str = "0.0.0.0", port: int = 8080, url: str = "/api/v1/new_message") -> NoReturn:
        if self.first_state is None:
            raise ValueError("First state must be set")

        request_handler = RequestHandler(UserStateConvertor(self.all_states),
                                         self.first_state,
                                         post_processing_functions=self.post_processing_functions,
                                         triggers=self.triggers)
        self.server.run(request_handler, host, port, url)
