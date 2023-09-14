import random
from typing import Optional

from yadu import *
from server import FlaskServer

server = FlaskServer(debug_mode=True)
bot = Bot(using_server=server)


@bot.state("Hello State")
class HelloState(State):
    def serialize(self) -> dict:
        pass

    @staticmethod
    def deserialize(state_data: dict) -> State:
        pass

    async def on_get_message(self, message: ApiRequest) -> tuple[Response, State]:
        random_number = random.randint(0, 100)
        return Response(text=f"Hello, world! Random number: {random_number}",
                        skill_state=message.skill_state), MainState(random_number)


@bot.state("MainState")
class MainState(State):
    def __init__(self, random_number: int, last_message: str = ""):
        self.random_number = random_number
        self.last_message: str = last_message

    async def on_get_message(self, request: ApiRequest) -> tuple[Response, State]:
        if self.last_message == "":
            response = Response(text=f"Random number: {self.random_number}. Request: {request.user_request.command}",
                                skill_state=request.skill_state)
        else:
            response = Response(text=f"Random number: {self.random_number}. Last request: {self.last_message}." +
                                     "Request: {request.user_request.command}", skill_state=request.skill_state)

        self.last_message = request.user_request.command
        return response, self

    def serialize(self) -> dict:
        return {
            "last_message": self.last_message,
            "random_number": self.random_number
        }

    @staticmethod
    def deserialize(data: dict) -> 'State':
        new_state = MainState(data["random_number"], data["last_message"])
        return new_state


class MyPostProcessing(ResponsePostProcessing):
    def process(self, response: Response, skill_state: SkillState, user_state: State) -> Response:
        response.add_button(Button(title="About skill", payload={"my_button_id": "ABOUT_SKILL"}, hide=True))
        return response


class MyTrigger(Trigger):
    async def on_new_message(self, message: ApiRequest) -> Optional[Response]:
        if isinstance(message.user_request, ButtonPressedUserRequest) and \
                message.user_request.payload["my_button_id"] == "ABOUT_SKILL":
            return Response(text="This is description of my skill", skill_state=message.skill_state)
        return None


bot.set_first_state(HelloState())
bot.add_post_processing_function(MyPostProcessing())
bot.add_trigger(MyTrigger())

bot.run(port=8050)

application = server.get_application()
