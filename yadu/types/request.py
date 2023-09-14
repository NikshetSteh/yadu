from typing import Optional, Union

from yadu.types.skill_state import SkillState


class UserRequest:
    def __init__(self, request: dict):
        self.type = request["type"]
        self.data = request


class Entities:
    def __init__(self, data: dict):
        self.value: str = data["value"]
        self.type: str = data["type"]
        self.tokens: dict = data["tokens"]


class UserIntents:
    def __init__(self, name: str, request: dict):
        self.name: str = name
        self.slots: dict = request["slots"]


class NluData:
    def __init__(self, data: dict):
        self.tokens: list[str] = data["tokens"]

        self.entities: list = list()
        for i in data["entities"]:
            self.entities.append(Entities(i))

        self.intents: dict = dict()
        for k in data["intents"]:
            self.intents[k] = UserIntents(k, data["intents"][k])


class SimpleUtteranceUserRequest(UserRequest):
    def __init__(self, request: dict):
        super().__init__(request)

        self.command: str = request["command"]
        self.original_utterance: str = request["original_utterance"]
        self.markup: dict = request["markup"] if "markup" in request else {}
        self.payload: dict = request["payload"] if "payload" in request else {}
        self.nlu: NluData = NluData(request["nlu"])


class ButtonPressedUserRequest(UserRequest):
    def __init__(self, request: dict):
        super().__init__(request)
        self.payload: dict = request["payload"]
        self.text_tokens: list[str] = request["nlu"]["tokens"]


class User:
    def __init__(self, request: Optional[dict]):
        if request is None:
            self.is_authenticated = False
            self.user_id = None
            self.access_token = None
        else:
            self.is_authenticated = True
            self.user_id = request["user_id"]
            self.access_token = request.get("access_token")


class Session:
    def __init__(self, request: dict):
        self.message_id = request["message_id"]
        self.session_id = request["session_id"]
        self.skill_id = request["skill_id"]
        self.user = User(request["user"] if "user" in request else None)
        self.application_id = request["application"]["application_id"]
        self.is_new = request["new"]


class InternetRequest:
    def __init__(self, request_data: dict):
        self.request_data: dict = request_data


class ApiRequest:
    def __init__(self, request: dict):
        self.version: str = request["version"]

        if request["request"]["type"] == "SimpleUtterance":
            self.user_request: UserRequest = SimpleUtteranceUserRequest(request["request"])
        elif request["request"]["type"] == "ButtonPressed":
            self.user_request: UserRequest = ButtonPressedUserRequest(request["request"])
        else:
            self.user_request: Union[UserRequest, SimpleUtteranceUserRequest, ButtonPressedUserRequest] = UserRequest(request["request"])

        self.session: Session = Session(request["session"])
        self.skill_state: SkillState = SkillState(request.get("state"))
        self.meta_data: dict = request["meta"]
