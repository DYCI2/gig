from enum import IntEnum


class Status(IntEnum):
    INVALID_STATUS = -1
    OFFLINE = 0
    PARENT_OBJ_MISSING = 1
    PARENT_OBJ_NOT_READY = 2
    UNINITIALIZED = 3
    INITIALIZING = 4
    READY = 5
    NO_RESPONSE = 6
    DELETED = 7
    WORKING = 8
    TERMINATED = 9
