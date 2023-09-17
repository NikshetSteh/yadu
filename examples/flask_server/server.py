import asyncio
import json
from typing import NoReturn

from yadu.handling.request_handler import RequestHandler
from yadu.server.server import Server
from yadu.types.request import InternetRequest
from yadu.types.response import InternetResponse

from flask import Flask, request, Request, Response


class FlaskServer(Server):
    def __init__(self, debug_mode: bool = False):
        self.application = None
        self.request_handler = None
        self.debug_mode = debug_mode

    def run(self, request_handler: RequestHandler, host: str = "0.0.0.0", port: int = 8080,
            url: str = "/api/v1/new_message") -> NoReturn:
        self.application = Flask(__name__)
        self.request_handler = request_handler

        @self.application.route(url, methods=["POST"])
        def hello():
            return self.process_request(request)

        if self.debug_mode:
            self.application.run(host=host, port=port, debug=True)

    def process_request(self, api_request: Request) -> Response:
        json_request_data = api_request.json

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        response = loop.run_until_complete(self.request_handler.process(InternetRequest(json_request_data)))

        loop.close()

        if response is None or not isinstance(response, InternetResponse):
            return Response({"message": "Response is not available"},
                            status=500,
                            headers={"Content-Type": "application/json"})

        return Response(json.dumps(response.data), status=400, headers={"Content-Type": "application/json"})

    def get_application(self):
        return self.application
