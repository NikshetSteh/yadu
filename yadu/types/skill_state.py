from typing import Optional


class SkillState:
    def __init__(self, request: Optional[dict] = None):
        if request is not None:
            self.session_vars = request["session"]
            self.user_vars = request["user"]
            self.application_vars = request["application"]
        else:
            self.session_vars = {}
            self.user_vars = {}
            self.application_vars = {}

    def serialize(self) -> dict:
        return {
            "session_state": self.session_vars,
            "user_state_update": self.user_vars,
            "application_state_update": self.application_vars,
        }
