from enum import Enum


class Status(str, Enum):
    ACTIVE = "ACTIVE"
    PASSIVE = "PASSIVE"
    DELETED = "DELETED"
