from json import loads
from .binary_stream import BinaryStream
from .dtypes import CompressTypes
from typing import Union, Dict, List, Any

class JsonCompressor:
    """
    A class for compressing JSON-like data into a binary format using specified data types.

    Attributes:
        _json (Dict[str, Any]): The parsed JSON data.
        _stream (BinaryStream): A BinaryStream instance for handling binary data operations.

    Methods:
        __init__(json_data: Union[str, bytes, Dict[str, Any]]) -> None:
            Initializes the JsonCompressor with JSON data in string, bytes, or dictionary format.
        
        compress() -> bytes:
            Compresses the JSON data into a binary format and returns it.
        
        _push_type(dtype: CompressTypes) -> None:
            Pushes the data type identifier to the binary stream.
        
        _compress_object(object: Dict[Any, Any]) -> bytes:
            Compresses a dictionary object into binary format.
        
        _compress_string(string: str) -> bytes:
            Compresses a string into binary format.
        
        _compress_int(integer: int) -> bytes:
            Compresses an integer into binary format.
        
        _compress_list(data: List[Any]) -> bytes:
            Compresses a list into binary format.
        
        _compress_data(data: Any) -> bytes:
            Determines the data type and compresses the data accordingly.
        
        get_compress_buffer() -> bytes:
            Returns the internal buffer of the BinaryStream as bytes.
    """

    def __init__(self, json_data: Union[str, bytes, Dict[str, Any]]) -> None:
        """
        Initializes the JsonCompressor with JSON data.

        Args:
            json_data (Union[str, bytes, Dict[str, Any]]): The JSON data to compress, which can be provided as a string,
                                                           bytes, or dictionary.
        """
        if isinstance(json_data, str):
            json_data = loads(json_data)
        if isinstance(json_data, bytes):
            json_data = loads(json_data.decode())
            
        self._json = json_data
        self._stream = BinaryStream()
        
    def compress(self) -> bytes:
        """
        Compresses the JSON data into a binary format.

        Returns:
            bytes: The compressed binary data.
        """
        return self._compress_data(self._json)
    
    def _push_type(self, dtype: CompressTypes) -> None:
        """
        Writes the data type identifier to the binary stream.

        Args:
            dtype (CompressTypes): The data type to push.

        Raises:
            ValueError: If the data type value is not in the valid range (0-255).
        """
        if dtype.value <= 0:
            raise ValueError(f"Invalid data type, data type must be in range 0 -> 255. got {dtype.value}")
        self._stream.write_byte(dtype.value)
            
    def _compress_object(self, object: Dict[Any, Any]) -> bytes:
        """
        Compresses a dictionary object into binary format.

        Args:
            object (Dict[Any, Any]): The dictionary to compress.

        Returns:
            bytes: The compressed binary data.
        
        Raises:
            TypeError: If the dictionary key is not a string.
        """
        self._push_type(CompressTypes.OBJECT)
        self._stream.write_byte(len(object))
        for key, value in object.items():
            if not isinstance(key, str):
                raise TypeError(f"Object key type must be of 'str' type, got {type(key)}")
            self._stream.write_string(key)
            self._compress_data(value)
    
    def _compress_string(self, string: str) -> bytes:
        """
        Compresses a string into binary format.

        Args:
            string (str): The string to compress.

        Returns:
            bytes: The compressed binary data.
        """
        self._push_type(CompressTypes.STRING)
        self._stream.write_string(string)
    
    def _compress_int(self, integer: int) -> bytes:
        """
        Compresses an integer into binary format.

        Args:
            integer (int): The integer to compress.

        Returns:
            bytes: The compressed binary data.
        """
        self._push_type(CompressTypes.INTEGER)
        self._stream.write_byte(integer)
            
    def _compress_list(self, data: List[Any]) -> bytes:
        """
        Compresses a list into binary format.

        Args:
            data (List[Any]): The list to compress.

        Returns:
            bytes: The compressed binary data.
        """
        compress_list = []
        self._push_type(CompressTypes.LIST)
        self._stream.write_byte(len(data))
        for item in data:
            compress_list.append(self._compress_data(item))
        return compress_list

    def _compress_data(self, data: Any) -> bytes:
        """
        Determines the data type and compresses the data accordingly.

        Args:
            data (Any): The data to compress.

        Returns:
            bytes: The compressed binary data.
        """
        if isinstance(data, dict):
            return self._compress_object(data)
        
        if isinstance(data, str):
            return self._compress_string(data)
        
        if isinstance(data, int):
            return self._compress_int(data)

        if isinstance(data, list):
            return self._compress_list(data)

    def get_compress_buffer(self) -> bytes:
        """
        Returns the internal buffer of the BinaryStream as bytes.

        Returns:
            bytes: The compressed binary data buffer.
        """
        return self._stream.get_buffer()
