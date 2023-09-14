from abc import abstractmethod
from typing import Type

from yadu.logger import yadu_logger
from yadu.types.request import ApiRequest
from yadu.types.response import Response
from yadu.types.skill_state import SkillState
from yadu.types.yadl_exception import YadlException


class State:
    @abstractmethod
    async def on_get_message(self, request: ApiRequest) -> tuple[Response, 'State']:
        pass

    @abstractmethod
    def serialize(self) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def deserialize(data: dict) -> 'State':
        pass


class UserStateConvertor:
    def __init__(self, state_list: dict[str, Type[State]]):
        self.state_list = state_list

    def serialize(self, user_state: State, skill_state: SkillState) -> SkillState:
        if type(user_state) not in self.state_list.values():
            raise Exception("State not found")

        skill_state.session_vars["state_name"] = list(self.state_list.keys())[
            list(self.state_list.values()).index(type(user_state))]
        skill_state.session_vars["user_state"] = user_state.serialize()

        return skill_state

    def deserialize(self, skill_state: SkillState) -> State:
        if skill_state is None or skill_state.session_vars is None:
            yadu_logger.error("State of the request is invalid. It does not exist")
            raise YadlException("Session state is invalid. It does not exist")
        elif "state_name" not in skill_state.session_vars:
            yadu_logger.error("State of the request is invalid. It does not contain current state")
            raise YadlException("Session state is invalid. It does contain current state")

        now_state_name = skill_state.session_vars["state_name"]
        if now_state_name not in self.state_list:
            yadu_logger.error(
                f"Current skill state is invalid. User state is not available. State: {now_state_name}")
            raise YadlException("Session state is invalid")

        return self.state_list[now_state_name].deserialize(skill_state.session_vars["user_state"])
