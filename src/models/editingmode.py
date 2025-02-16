from enum import Enum


class EditingMode(Enum):
    """Represents an application state. VIEWING is used \
when the user is not defining the origin or scale and is \
not acquiring."""

    VIEWING = 0
    ACQUIRING = 1
    DEFINING_ORIGIN = 2
    DEFINING_SCALE = 3
