from enum import Enum, auto


class StorageKeys(Enum):
    PREVIOUS_MESSAGE_DATE = auto()

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
