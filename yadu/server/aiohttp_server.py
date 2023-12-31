import json
from typing import NoReturn

from aiohttp import web

from yadu.handling.request_handler import RequestHandler
from yadu.logger import yadu_logger
from yadu.server.server import Server
from yadu.types.request import InternetRequest
from yadu.types.response import InternetResponse


class AiohttpServer(Server):
    def __init__(self):
        super().__init__()
        self.request_handler = None

    def run(self, request_handler: RequestHandler, host: str = "0.0.0.0", port: int = 8080,
            url: str = "/api/v1/new_message") -> NoReturn:
        self.request_handler = request_handler
        app = web.Application()
        app.router.add_post(url, self.process_request)
        web.run_app(app, host=host, port=port)

    async def process_request(self, request: web.Request) -> web.Response:
        try:
            json_request_data = await request.json()
        except Exception:
            yadu_logger.error("Response is not in JSON format")
            return web.Response(text="Response is not in JSON format", status=400)

        response = await self.request_handler.process(InternetRequest(json_request_data))
        if response is None or not isinstance(response, InternetResponse):
            yadu_logger.error("Response is not available")
            return web.Response(text="Response is not available", status=500)

        return web.json_response(text=json.dumps(response.data))
