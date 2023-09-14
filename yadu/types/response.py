from yadu.types.gui_response_elements import Card, Button
from yadu.types.request import SkillState


class Response:
    def __init__(self,
                 is_end: bool = False,
                 skill_state: SkillState = None,
                 text: str = "",
                 tts: str = "",
                 buttons: list[Button] = None,
                 card: Card = None,
                 version: str = "1.0"):
        self.text: str = text
        self.tts: str = tts
        self.buttons: list[Button] = buttons if buttons is not None else []
        self.is_end: bool = is_end
        self.card: Card = card
        self.version: str = version
        self.skill_state: SkillState = skill_state

    def serialize(self) -> dict:
        response: dict = {
            "response": {
                "end_session": self.is_end,
                "directives": {},
            },
            "version": self.version,
        }

        if self.text is not None and self.text != "":
            response["response"]["text"] = self.text
        if self.tts is not None and self.tts != "":
            response["response"]["tts"] = self.tts

        if self.card is not None:
            response["response"]["card"] = self.card.serialize()

        if len(self.buttons) > 0:
            response["response"]["buttons"] = [button.serialize() for button in self.buttons]

        response.update(self.skill_state.serialize())

        return response

    def add_button(self, button: Button) -> None:
        if not isinstance(button, Button):
            raise TypeError("Argument 'button' must be of type Button")
        self.buttons.append(button)

    def add_buttons(self, buttons: list[Button]) -> None:
        for button in buttons:
            if button is not Button:
                raise TypeError("Argument 'buttons' must be of type list[Button]")
            self.add_button(button)

    def set_card(self, card: Card) -> None:
        if card is not Card:
            raise TypeError("Argument 'card' must be of type Card")
        self.card = card

    def text_response(self, text: str, tts: str = "") -> None:
        self.text = text
        self.tts = tts

    def validate(self):
        if self.text is None and self.text == "" and self.card is None:
            return False

        return True


class InternetResponse:
    def __init__(self, data: dict, status_code: int = 200):
        self.data: dict = data
        self.response_code: int = status_code
