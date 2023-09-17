# Server 
This library can support almost all servers. To get out of support, you need to implement a wrapper.

Server wrapper is class inherited from the `Server` class and redefine the abstract method 
`run(request_handler: RequestHandler, host: str = "0.0.0.0", port: int = 8080, url: str = "/api/v1/new_message")`.

Method `run` can be a loop or no. If it is not loop, `bot.run()` don\`t will be a loop. For set bot server, when create 
bot instance, set as argument `using_server` instance of your server

## Example
This is example of Flask server wrapper

```python
from yadu import *

import asyncio
import json
from typing import NoReturn

from yadu.handling.request_handler import RequestHandler
from yadu.server.server import Server
from yadu.types.request import InternetRequest
from yadu.types.response import InternetResponse

from flask import Flask, request, Request, Response


# Create wrapper
class FlaskServer(Server):
    def __init__(self, debug_mode: bool = False):
        self.application = None
        self.request_handler = None
        self.debug_mode = debug_mode

    def run(self, request_handler: RequestHandler, host: str = "0.0.0.0", port: int = 8080,
            url: str = "/api/v1/new_message") -> NoReturn:
        # Save Flask application instance
        self.application = Flask(__name__)
        self.request_handler = request_handler

        # Create api endpoint
        @self.application.route(url, methods=["POST"])
        def hello():
            return self.process_request(request)

        # If debug mode is enable, run local server
        if self.debug_mode:
            self.application.run(host=host, port=port, debug=True)

    def process_request(self, api_request: Request) -> Response:
        # Prepare request 
        json_request_data = api_request.json

        # Handlers are async, and Flask is not support it. For fix this, create new event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Get response of request handler
        response = loop.run_until_complete(self.request_handler.process(InternetRequest(json_request_data)))

        loop.close()

        # If request type is not InternetResponse, return error
        if response is None or not isinstance(response, InternetResponse):
            return Response({"message": "Response is not available"},
                            status=500,
                            headers={"Content-Type": "application/json"})

        # Converting the internal abstract class into server responses and returning it
        return Response(json.dumps(response.data), status=400, headers={"Content-Type": "application/json"})

    def get_application(self):
        return self.application



# Create server instance and set it to bot
server = FlaskServer(debug_mode=False)
bot = Bot(using_server=server)


@bot.state("Hello State")
class HelloState(State):
    def serialize(self) -> dict:
        pass

    @staticmethod
    def deserialize(state_data: dict) -> State:
        pass

    async def on_get_message(self, message: ApiRequest) -> tuple[Response, State]:
        return Response(text=f"Hello, world!", skill_state=message.skill_state), self


bot.set_first_state(HelloState())

bot.run()

# Get application for wsgi
application = server.get_application()
```

WSGI file:

```python
import sys

path = 'path/to/project/folder'
if path not in sys.path:
    sys.path.append(path)

# noinspection PyUnresolvedReferences
from main import application
```


You can see full example in `examples/flask_server`