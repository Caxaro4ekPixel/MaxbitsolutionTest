from enum import Enum, auto


class RegistrationState(Enum):
    ENTERING_NAME = auto()
    ENTERING_LOGIN = auto()


class TaskCreationState(Enum):
    ENTERING_TITLE = auto()
    ENTERING_DESCRIPTION = auto()
