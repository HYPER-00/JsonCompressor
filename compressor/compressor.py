from json import loads
from .binary_stream import BinaryStream
from .dtypes import CompressTypes
from typing import Union, Dict, List, Any


class JsonCompressor:
    def __init__(self, json_data: Union[str, bytes, Dict[str, Any]]) -> None:
        if isinstance(json_data, str):
            json_data = loads(json_data)
        if isinstance(json_data, bytes):
            json_data = loads(json_data.decode())
            
        self._json = json_data
        self._stream = BinaryStream()
        
    def compress(self) -> bytes:
        return self._compress_data(self._json)
    
    def _push_type(self, dtype: CompressTypes) -> None:
        if dtype.value <= 0:
            raise ValueError(f"Invalid data type, data type must be in range 0 -> 255. got {dtype.value}")
        self._stream.write_byte(dtype.value)
            
    def _compress_object(self, object: Dict[Any, Any]) -> bytes:
        self._push_type(CompressTypes.OBJECT)
        self._stream.write_byte(len(object))
        for key, value in object.items():
            if not isinstance(key, str):
                raise TypeError(f"Object key type must be of 'str' type, got {type(key)}")
            self._stream.write_string(key)
            self._compress_data(value)
    
    def _compress_string(self, string: str) -> bytes:
        self._push_type(CompressTypes.STRING)
        self._stream.write_string(string)
    
    def _compress_int(self, integer: int) -> bytes:
        self._push_type(CompressTypes.INTEGER)
        self._stream.write_byte(integer)
            
    def _compress_list(self, data: List[Any]) -> bytes:
        compress_list = []
        self._push_type(CompressTypes.LIST)
        self._stream.write_byte(len(data))
        for item in data:
            compress_list.append(self._compress_data(item))
        return compress_list

    def _compress_data(self, data: Any) -> bytes:
        if isinstance(data, dict):
            return self._compress_object(data)
        
        if isinstance(data, str):
            return self._compress_string(data)
        
        if isinstance(data, int):
            return self._compress_int(data)

        if isinstance(data, list):
            return self._compress_list(data)

    def get_compress_buffer(self) -> bytes:
        return self._stream.get_buffer()

