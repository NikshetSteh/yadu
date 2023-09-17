# Triggers
Tasks for processing user requests often appear, regardless of the current user state. Triggers are used for such tasks.
They handle all incoming requests. If they are triggered and return a response, it will be returned, and the user_state 
request handler will not work.

To create a trigger, you need to create a class inherited from the `Trigger` class and redefine the abstract method `on_new_message`.
And add it to instance of bot using ```bot.add_trigger(MyTrigger())```

## Example
```python
from typing import Optional

from yadu import *

bot = Bot()


@bot.state("Hello State")
class HelloState(State):
    def serialize(self) -> dict:
        pass

    @staticmethod
    def deserialize(state_data: dict) -> State:
        pass

    async def on_get_message(self, message: ApiRequest) -> tuple[Response, State]:
        return Response(text=f"Hello, world", skill_state=message.skill_state), self


class MyPostProcessing(ResponsePostProcessing):
    def process(self, response: Response, skill_state: SkillState, user_state: State) -> Response:
        response.add_button(Button(title="About skill", payload={"my_button_id": "ABOUT_SKILL"}, hide=True))
        return response


# Create trigger class
class MyTrigger(Trigger):
    async def on_new_message(self, message: ApiRequest) -> Optional[Response]:
        # If response has type `ButtonPressedUserRequest` and payload my_button_id is `ABOUT_BUTTON` we return description
        # Else we return None (it means, what trigger did not work)
        if isinstance(message.user_request, ButtonPressedUserRequest) and \
                message.user_request.payload["my_button_id"] == "ABOUT_SKILL":
            return Response(text="This is description of my skill", skill_state=message.skill_state)
        return None


bot.set_first_state(HelloState())
bot.add_post_processing_function(MyPostProcessing())
# Add trigger to bot instance
bot.add_trigger(MyTrigger())

bot.run()
```