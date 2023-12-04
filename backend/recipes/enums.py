from enum import IntEnum


class TagEnums(IntEnum):
    NAME_MAX_LEN = 32
    SLUG_MAX_LEN = 32
    COLOR_MAX_LEN = 7


class IngredientEnums(IntEnum):
    NAME_MAX_LEN = 64
    MEASUREMENT_UNIT_MAX_LEN = 32


class RecipeEnums(IntEnum):
    NAME_MAX_LEN = 64
    NAME_MIN_LEN = 3
    TEXT_MAX_LEN = 2048
    COOKING_TIME_DEFAULT_VALUE = 5


class AmountIngredientEnums(IntEnum):
    AMOUNT_DEFAULT_VALUE = 1
    AMOUNT_MIN_VALUE = 1
