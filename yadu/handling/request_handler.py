import yadu.types.response
from yadu.handling import post_processing
from yadu.handling.state import State, UserStateConvertor
from yadu.handling.triggers import Trigger
from yadu.logger import yadu_logger
from yadu.types.request import *
from yadu.types.response import InternetResponse
from yadu.types.yadl_exception import YadlException


class RequestHandler:
    def __init__(self,
                 state_serializer: UserStateConvertor,
                 first_state: State,
                 protocol_version: str = "1.0",
                 post_processing_functions: list[post_processing.ResponsePostProcessing] = None,
                 triggers: list[Trigger] = None):
        self.protocol_version = protocol_version
        self.first_state = first_state
        self.post_processing_functions = post_processing_functions if post_processing_functions is not None else []
        self.state_serializer = state_serializer
        self.triggers = triggers if triggers is not None else []

    async def process(self, request: InternetRequest) -> InternetResponse:
        try:
            api_request = ApiRequest(request.request_data)
        except Exception:
            yadu_logger.error(f"Error processing request. Can`t parse API request.")
            return InternetResponse({"message": "Response is not in API format"}, 400)

        if api_request.version != self.protocol_version:
            yadu_logger.error(
                f"Version mismatch. Request version: {api_request.version}, Server version: {self.protocol_version}")
            return InternetResponse({"message": "Version mismatch"}, 400)

        try:
            now_user_state = self.get_user_state_from_request(api_request)
        except YadlException as e:
            yadu_logger.error(f"Error processing request. {e}")
            return InternetResponse({"message": e.message}, 400)

        trigger_response = None
        for i in self.triggers:
            trigger_response = await i.on_new_message(api_request)
            if trigger_response is not None:
                break

        if trigger_response is not None:
            response = self.apply_post_processing(trigger_response, None)
            self.state_serializer.serialize(now_user_state, response.skill_state)
            response_data = response.serialize()
            return InternetResponse(response_data)

        return await self.process_user_state(now_user_state, api_request)

    async def process_user_state(self, now_state: State, api_request: ApiRequest) -> InternetResponse:
        response, new_user_state = await now_state.on_get_message(api_request)

        if response is None or not isinstance(response, yadu.types.response.Response) or not response.validate():
            yadu_logger.error("State response is invalid. Response is not in Response format")
            return InternetResponse({"message": "State response is invalid"}, 400)

        response = self.apply_post_processing(response, now_state)

        self.state_serializer.serialize(new_user_state, response.skill_state)
        response_data = response.serialize()

        return InternetResponse(response_data)

    def apply_post_processing(self, response: yadu.types.response.Response, now_state: Optional[State]) -> yadu.types.response.Response:
        for i in self.post_processing_functions:
            response = i.process(response, response.skill_state, now_state)

        return response

    def get_user_state_from_request(self, api_request: ApiRequest) -> State:
        if api_request.session.is_new:
            now_state = self.first_state
        else:
            now_state = self.state_serializer.deserialize(api_request.skill_state)

        return now_state
