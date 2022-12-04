from enum import Enum


class EnumContent(Enum):

    def __init__(self, text):
        if type(text) == str:
            # text = text.strip()
            if "\n===\n" in text:
                text = text.split("\n===\n")
            self._value_ = text

    def __str__(self):
        return self.value