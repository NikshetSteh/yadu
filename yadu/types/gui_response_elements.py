from abc import abstractmethod


class Button:
    def __init__(self, title: str, url: str = "", payload: dict = None, hide: bool = False):
        self.title: str = title
        self.url: str = url
        self.payload: dict = payload if payload is not None else {}
        self.hide: bool = hide

    def serialize(self) -> dict:
        result = {
            "title": self.title,
            "hide": self.hide,
        }

        if self.url is not None and self.url != "":
            result["url"] = self.url

        if self.payload is not None:
            result["payload"] = self.payload

        return result


class Card:
    @abstractmethod
    def serialize(self) -> dict:
        pass


class ImageOnCard:
    def __init__(self, image_id: str, title: str, description: str, buttons: list[Button] = None):
        self.image_id: str = image_id
        self.title: str = title
        self.description: str = description
        self.buttons: list[Button] = buttons if buttons is not None else []

    def serialize(self) -> dict:
        result = {
            "type": "BigImageCard",
            "image_id": self.image_id,
            "title": self.title,
            "description": self.description,
        }

        if len(self.buttons) > 0:
            result["button"] = [button.serialize() for button in self.buttons]

        return result


class BigImageCard(Card):
    def __init__(self, image: ImageOnCard):
        self.image = image

    def serialize(self) -> dict:
        return self.image.serialize()


class ItemsListCard(Card):
    def __init__(self,
                 title: str,
                 items:
                 list[ImageOnCard],
                 buttons: list[Button] = None,
                 footer_text: str = ""):
        self.title: str = title
        self.items: list[ImageOnCard] = items
        self.buttons: list[Button] = buttons if buttons is not None else []
        self.footer_text: str = footer_text

    def serialize(self) -> dict:
        result = {
            "type": "ItemsList",
            "header": {
                "text": self.title,
            },
            "items": [item.serialize() for item in self.items]
        }

        if self.footer_text != "" or len(self.buttons) > 0:
            result["footer"] = {}
            if self.footer_text != "":
                result["footer"]["text"] = self.footer_text
            if len(self.buttons) > 0:
                result["footer"]["button"] = [button.serialize() for button in self.buttons]

        return result


class ImageGalleryCard(Card):
    def __init__(self, images: list[ImageOnCard]):
        self.images: list[ImageOnCard] = images

    def serialize(self) -> dict:
        return {
            "type": "ImageGallery",
            "items": [image.serialize() for image in self.images]
        }
