# User states
The processing of user requests is based on the state machine. Depending on the current state of the user, a suitable 
handler is selected and the current state of the user is deserialized

For create new state, you need create class inherited from the `State` class with decorator of bot instance 
`bot.state(state_name)` and redefine the abstract methods `on_new_message`, `deserialize`, `serialize`

For set first user state using ```bot.set_first_state(MyFirstState())```

## Methods
### ```on_new_message```
```python
# noinspection all
async def on_get_message(self, message: ApiRequest) -> tuple[Response, State]:
    pass
```

This method is request handler. It gets user message and need return response and new state.

Examples:
```python
# noinspection all
async def on_get_message(self, message: ApiRequest) -> tuple[Response, State]:
    random_number = random.randint(0, 100)
    return Response(text=f"Hello, world!", skill_state=message.skill_state), self
```
```python
# noinspection all
async def on_get_message(self, message: ApiRequest) -> tuple[Response, State]:
    random_number = random.randint(0, 100)
    return Response(text=f"Hello, world! {random_number}", skill_state=message.skill_state), MySecondState(random_number)
```

### ```deserialize```
This method using for deserialize state from key-value container. It gets dict and need return instance of this state
```python
# noinspection all
@staticmethod
def deserialize(state_data: dict) -> State:
    pass
```

Example:
```python
# noinspection all
@staticmethod
def deserialize(data: dict) -> 'State':
    current_state = ThisState(data["first_arg"], data["second_arg"])
    return current_state
```

### ```serialize```
This method using to serialize current user state to key-value container (dict)
```python
# noinspection all
def serialize(self) -> dict:
    pass
```

Example:
```python
# noinspection all
def serialize(self) -> dict:
    return {
        "some_arg": self.some_arg
    }
```



## Example
```python
import random

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
                                     f"Request: {request.user_request.command}", skill_state=request.skill_state)

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


bot.set_first_state(HelloState())

bot.run()
```