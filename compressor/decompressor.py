from .binary_stream import BinaryStream
from .dtypes import CompressTypes
from typing import Any, List, Dict


class JsonDecompressor:
    def __init__(self, json_data: bytes) -> None:
        self._json = json_data
        self._stream = BinaryStream(self._json)
        
    def _read_type(self) -> CompressTypes:
        return CompressTypes(self._stream.read_byte())
    
    def decompress(self) -> bytes:
        return self._decompress_data()
        
    def _decompress_string(self) -> str:
        return self._stream.read_string()
    
    def _decompress_integer(self) -> int:
        return self._stream.read_byte()

    def _decompress_boolean(self) -> bool:
        return bool(self._stream.read_byte())
    
    def _decompress_object(self) -> Dict[Any, Any]:
        size = self._stream.read_byte()
        object = {}
        print(f"Size: {size}")
        for _ in range(size):
            key = self._stream.read_string()
            value = self._decompress_data()
            object[key] = value
        return object
    
    def _decompress_list(self) -> List[Any]:
        list_size = self._stream.read_byte()
        if not list_size:
            return []
        
        decompress_list: List[Any] = []
        for _ in range(list_size):
            decompress_list.append(self._decompress_data())
        return decompress_list
    
    def _decompress_data(self) -> Any:
        dtype = self._read_type()
        if dtype == CompressTypes.INTEGER:
            return self._decompress_integer()
        
        if dtype == CompressTypes.STRING:
            return self._decompress_string()
        
        if dtype == CompressTypes.BOOLEAN:
            return self._decompress_boolean()
        
        if dtype == CompressTypes.LIST:
            return self._decompress_list()
        
        if dtype == CompressTypes.OBJECT:
            return self._decompress_object()
        
