from typing import Union, Optional
from .exceptions import BinaryStreamError


class BinaryStream:
    def __init__(self, buffer: Optional[Union[str, bytes]] = bytearray()) -> None:
        if isinstance(buffer, str):
            buffer = bytearray(buffer.encode())
        self._buffer = buffer
        self._read_offset = 0
        self._write_offset = 0

    def read_byte(self) -> int:
        if len(self._buffer) <= self._read_offset:
            raise BinaryStreamError(
                f"Invalid read offset {self._read_offset}, perhaps the entire buffer has been read?"
            )
        byte = self._buffer[self._read_offset]
        self._read_offset += 1
        return byte

    def read_string(self) -> str:
        length = self.read_byte()
        string = self._buffer[self._read_offset : self._read_offset + length].decode()
        self._read_offset += length
        return string

    def write_byte(self, integer: int) -> None:
        if integer > 255:
            raise ValueError(f"Integer must be less than 255, received {integer}")
        self._buffer.append(integer)
        self._read_offset += 1
        
    def write_bool(self, boolean: bool) -> None:
        self.write_byte(boolean)

    def write_string(self, string: str) -> None:
        length = len(string)
        if length > 255:
            raise ValueError(f"String length must be less than 255, received {length}")
        self.write_byte(length)
        self._buffer.extend(string.encode())

    def get_buffer(self) -> bytes:
        return bytes(self._buffer)

    def get_current_readoffset(self) -> int:
        return self._read_offset
