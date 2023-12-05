from enum import IntEnum


class UserEnums(IntEnum):
    FIRST_NAME_MAX_LEN = 32
    LAST_NAME_MAX_LEN = 32
    USERNAME_MAX_LEN = 32
    USERNAME_MIN_LEN = 3
    PASSWORD_MAX_LEN = 128
    PASSWORD_MIN_LEN = 8
    EMAIL_MAX_LEN = 256
