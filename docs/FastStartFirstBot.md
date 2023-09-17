# Fast start: first bot
Full code you can find in `examples/simple_bot`



## Content:
- [Preparation](./FastStartFirstBot.md#preparing)
- [Create bot instance](./FastStartFirstBot.md#create-bot-instance)
- [Create states](./FastStartFirstBot.md#create-bot-instance)
  - [Request](./FastStartFirstBot.md#requests)
  - [Response](./FastStartFirstBot.md#responses)
- [Add trigger](./FastStartFirstBot.md#add-triggers)
- [Add postprocessing](./FastStartFirstBot.md#add-postprocessing)
- [Select server](./FastStartFirstBot.md#select-server)
- [Create dialog](./FastStartFirstBot.md#create-dialog) in [Yandex Alice Dashboard](https://dialogs.yandex.ru/developer/skills/)



## Preparing
For first, lets create python venv and import using library. In this example using python 3.8

```bash
python3 -m venv venv
source venv/bin/activate
pip install git+https://github.com/NikshetSteh/yadu
```

You can read more about installing in [Installing.md](./Installing.md) file



## Create bot instance
Now we need create a bot instance
```python
from yadu import *

bot = Bot()
bot.run(host="0.0.0.0", port=8080, url="/api/v1/new_message")
```
An instance of the Bat class is needed to combine user request handlers and start the server



## Create states
The state machine is at the heart of query processing. Each request is processed by the handler of the state in which 
the user is currently or the initial state if this is the first request

Add initial state:
```python
# noinspection all
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
                        skill_state=message.skill_state), self
```
You can read more about user states in file [RequestHandling/UserStates.md](./RequestHandling/UserStates.md)

In this code block we create `HelloState` with name 'Hello state'. 
The name is necessary for serialization and deserialization of the user's state. 
It must be unique for each instance of bot.
After processing the user's request, it is necessary to return the following user state.

Also, then we create state, we need to implement ```serialize``` and ```deserialize```  methods. 
It requre for serialize state to session storage and deserialize state from it.

Let's now add the following user state:
```python
# noinspection all
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
```
And we will change the `on_get_message` method in the greeting state so that after it the user goes to the ```MainState``` state
```python
# noinspection all
async def on_get_message(self, message: ApiRequest) -> tuple[Response, State]:
    random_number = random.randint(0, 100)
    return Response(text=f"Hello, world! Random number: {random_number}",
                    skill_state=message.skill_state), MainState(random_number)
```

### Requests
There are several query options. Supported:
- [SimpleUtteranceUserRequest](./RequestHandling/Requests/SimpleUtteranceUserRequest.md)
- [ButtonPressedUserRequest](./RequestHandling/Requests/ButtonPressedUserRequest.md)

### Responses
Response has some field. The main of them is `text`, `tts`, `buttons`, `card`, `skill_state`.

- `text` - this is text of message
- `tts` - message in text-to-speech format. And, using it, you can play some sounds. It is optional. 
More in [Yandex Alice documentation](https://yandex.ru/dev/dialogs/alice/doc/speech-tuning.html) 
- `buttons` - you can add buttons to answer. [More](./RequestHandling/Response/Buttons.md)
- `card` - you also can display some image for user. [More](./RequestHandling/Response/Cards.md)
- `skill_state` - This is an object that stores information about the user. The data inside it is divided into three, 
depending on the storage context of the session: user application instance, authorized user


## Add triggers
Tasks for processing user requests often appear, regardless of the current user state. Triggers are used for such tasks.
They handle all incoming requests. If they are triggered and return a response, it will be returned, and the user_state 
request handler will not work.

This is example of trigger, which is triggered if the user clicked on the "About skill" button
```python
# noinspection all
class MyTrigger(Trigger):
    async def on_new_message(self, message: ApiRequest) -> Optional[Response]:
        if isinstance(message.user_request, ButtonPressedUserRequest) and \
                message.user_request.payload["my_button_id"] == "ABOUT_SKILL":
            return Response(text="This is description of my skill", skill_state=message.skill_state)
        return None
```

You can read more about trigger in [Triggers](./RequestHandling/Triggers.md)



## Add postprocessing
There are often tasks when you need to add some elements for all states. For example, the "About skill" button.

The Response Post Processing input receives the context of the current call and the generated response. 
It returns the modified response

This example add `About SKill` button to all responses
```python
# noinspection all
class MyPostProcessing(ResponsePostProcessing):
    def process(self, response: Response, skill_state: SkillState, user_state: State) -> Response:
        response.add_button(Button(title="About skill", payload={"my_button_id": "ABOUT_SKILL"}, hide=True))
        return response
```



## Select server
In different situations, a different choice of request handler is possible. 
By default, the library uses aaa http, but you can choose any other one by implementing a wrapper over it.

You can watch example of using Flask server in `examples/flask_server`



## Create dialog
To create your skill, you need to register with [Yandex](https://passport.yandex.ru/auth/reg). 
Next, you need to enter in [dialogs dashboard](https://dialogs.yandex.ru/developer/). Now you can create dialogs.
To create a skill, click on the `Create dialog` button and select `Skill for Alice` in the window that appears.
In the window that opens, you can fill in all the necessary information about your skill. 

### !!! It is absolutely necessary to enable `Storage` for the library to work correctly !!!


You can read more about creating skill in Yandex [Documentation](https://yandex.ru/dev/dialogs/alice/doc/about.html)