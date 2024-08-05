from .binary_stream import BinaryStream
from .dtypes import CompressTypes
from typing import Any, List, Dict

class JsonDecompressor:
    """
    A class for decompressing binary data into JSON-like data structures using specified data types.

    Attributes:
        _json (bytes): The binary data to decompress.
        _stream (BinaryStream): A BinaryStream instance for reading binary data.

    Methods:
        __init__(json_data: bytes) -> None:
            Initializes the JsonDecompressor with binary data.
        
        _read_type() -> CompressTypes:
            Reads and returns the next data type from the binary stream.
        
        decompress() -> Any:
            Decompresses the binary data into its original data structure.
        
        _decompress_string() -> str:
            Decompresses a string from the binary data.
        
        _decompress_integer() -> int:
            Decompresses an integer from the binary data.
        
        _decompress_boolean() -> bool:
            Decompresses a boolean from the binary data.
        
        _decompress_object() -> Dict[Any, Any]:
            Decompresses a dictionary object from the binary data.
        
        _decompress_list() -> List[Any]:
            Decompresses a list from the binary data.
        
        _decompress_data() -> Any:
            Determines the data type and decompresses the data accordingly.
    """

    def __init__(self, json_data: bytes) -> None:
        """
        Initializes the JsonDecompressor with binary data.

        Args:
            json_data (bytes): The binary data to decompress.
        """
        self._json = json_data
        self._stream = BinaryStream(self._json)
        
    def _read_type(self) -> CompressTypes:
        """
        Reads and returns the next data type from the binary stream.

        Returns:
            CompressTypes: The data type read from the binary stream.
        """
        return CompressTypes(self._stream.read_byte())
    
    def decompress(self) -> Any:
        """
        Decompresses the binary data into its original data structure.

        Returns:
            Any: The decompressed data, which can be a dictionary, list, string, integer, or boolean.
        """
        return self._decompress_data()
        
    def _decompress_string(self) -> str:
        """
        Decompresses a string from the binary data.

        Returns:
            str: The decompressed string.
        """
        return self._stream.read_string()
    
    def _decompress_integer(self) -> int:
        """
        Decompresses an integer from the binary data.

        Returns:
            int: The decompressed integer.
        """
        return self._stream.read_byte()

    def _decompress_boolean(self) -> bool:
        """
        Decompresses a boolean from the binary data.

        Returns:
            bool: The decompressed boolean.
        """
        return bool(self._stream.read_byte())
    
    def _decompress_object(self) -> Dict[Any, Any]:
        """
        Decompresses a dictionary object from the binary data.

        Returns:
            Dict[Any, Any]: The decompressed dictionary.
        """
        size = self._stream.read_byte()
        object = {}
        for _ in range(size):
            key = self._stream.read_string()
            value = self._decompress_data()
            object[key] = value
        return object
    
    def _decompress_list(self) -> List[Any]:
        """
        Decompresses a list from the binary data.

        Returns:
            List[Any]: The decompressed list.
        """
        list_size = self._stream.read_byte()
        if not list_size:
            return []
        
        decompress_list: List[Any] = []
        for _ in range(list_size):
            decompress_list.append(self._decompress_data())
        return decompress_list
    
    def _decompress_data(self) -> Any:
        """
        Determines the data type and decompresses the data accordingly.

        Returns:
            Any: The decompressed data.
        """
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
