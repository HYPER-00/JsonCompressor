from typing import Union, Optional
from .exceptions import BinaryStreamError

class BinaryStream:
    """
    A class for reading from and writing to a binary stream.

    Attributes:
        _buffer (bytearray): The internal buffer for storing binary data.
        _read_offset (int): The current read position in the buffer.
        _write_offset (int): The current write position in the buffer.

    Methods:
        __init__(buffer: Optional[Union[str, bytes]] = bytearray()) -> None:
            Initializes the BinaryStream with an optional buffer.
        
        read_byte() -> int:
            Reads a single byte from the buffer.
        
        read_string() -> str:
            Reads a string from the buffer. The string is prefixed by its length as a single byte.
        
        write_byte(integer: int) -> None:
            Writes a single byte to the buffer. The value must be less than 255.
        
        write_bool(boolean: bool) -> None:
            Writes a boolean value to the buffer as a byte.
        
        write_string(string: str) -> None:
            Writes a string to the buffer. The string is prefixed by its length as a single byte.
        
        get_buffer() -> bytes:
            Returns the internal buffer as bytes.
        
        get_current_readoffset() -> int:
            Returns the current read offset in the buffer.
    """

    def __init__(self, buffer: Optional[Union[str, bytes]] = bytearray()) -> None:
        """
        Initializes the BinaryStream with an optional buffer.

        Args:
            buffer (Optional[Union[str, bytes]]): An optional initial buffer, either as a string or bytes. 
                                                  If not provided, an empty bytearray is used.
        """
        if isinstance(buffer, str):
            buffer = bytearray(buffer.encode())
        self._buffer = buffer
        self._read_offset = 0
        self._write_offset = 0

    def read_byte(self) -> int:
        """
        Reads a single byte from the buffer.

        Returns:
            int: The byte read from the buffer.

        Raises:
            BinaryStreamError: If the read offset exceeds the buffer length.
        """
        if len(self._buffer) <= self._read_offset:
            raise BinaryStreamError(
                f"Invalid read offset {self._read_offset}, perhaps the entire buffer has been read?"
            )
        byte = self._buffer[self._read_offset]
        self._read_offset += 1
        return byte

    def read_string(self) -> str:
        """
        Reads a string from the buffer. The string is prefixed by its length as a single byte.

        Returns:
            str: The string read from the buffer.
        """
        length = self.read_byte()
        string = self._buffer[self._read_offset : self._read_offset + length].decode()
        self._read_offset += length
        return string

    def write_byte(self, integer: int) -> None:
        """
        Writes a single byte to the buffer.

        Args:
            integer (int): The byte to write. Must be less than 255.

        Raises:
            ValueError: If the integer is greater than 255.
        """
        if integer > 255:
            raise ValueError(f"Integer must be less than 255, received {integer}")
        self._buffer.append(integer)
        self._read_offset += 1

    def write_bool(self, boolean: bool) -> None:
        """
        Writes a boolean value to the buffer as a byte.

        Args:
            boolean (bool): The boolean value to write.
        """
        self.write_byte(boolean)

    def write_string(self, string: str) -> None:
        """
        Writes a string to the buffer. The string is prefixed by its length as a single byte.

        Args:
            string (str): The string to write.

        Raises:
            ValueError: If the string length exceeds 255.
        """
        length = len(string)
        if length > 255:
            raise ValueError(f"String length must be less than 255, received {length}")
        self.write_byte(length)
        self._buffer.extend(string.encode())

    def get_buffer(self) -> bytes:
        """
        Returns the internal buffer as bytes.

        Returns:
            bytes: The internal buffer.
        """
        return bytes(self._buffer)

    def get_current_readoffset(self) -> int:
        """
        Returns the current read offset in the buffer.

        Returns:
            int: The current read offset.
        """
        return self._read_offset
