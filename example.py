from compressor import JsonCompressor, JsonDecompressor
from json import dumps

json_data = ["Item1", 64, True, False, {"key1": 122}]

compressor = JsonCompressor(json_data)

compressor.compress()

compressed_buffer = compressor.get_compress_buffer()
print(f"Compressed length: {len(compressed_buffer)}")
print(f"Normal Length: {len(dumps(json_data))}")

decompressor = JsonDecompressor(compressed_buffer)
print(decompressor.decompress())


