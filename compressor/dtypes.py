from enum import Enum


class CompressTypes(Enum):
    """
    An enumeration for data types used in compression and decompression.

    Members:
        INTEGER (1): Represents an integer data type.
        STRING (2): Represents a string data type.
        BOOLEAN (3): Represents a boolean data type.
        LIST (4): Represents a list data type.
        OBJECT (5): Represents an object (dictionary) data type.
    """

    INTEGER = 1
    STRING = 2
    BOOLEAN = 3
    LIST = 4
    OBJECT = 5
