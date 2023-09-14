from abc import abstractmethod

from yadu.handling.state import State
from yadu.types.response import Response
from yadu.types.skill_state import SkillState


class ResponsePostProcessing:
    @abstractmethod
    def process(self, response: Response, skill_state: SkillState, user_state: State) -> Response:
        return response
