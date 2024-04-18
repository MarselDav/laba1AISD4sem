from source.AdaptiveHaffmanCoding.AdaptiveHaffmanCompress import AHA_COMPRESS
from source.AdaptiveHaffmanCoding.AdaptiveHaffmanDecompress import AHA_DECOMPRESS


def test_compress():
    adaptiveHaffmanCompress = AHA_COMPRESS()
    adaptiveHaffmanDecompress = AHA_DECOMPRESS()

    test_data_path = "AHA/original_text.txt"
    compressed_path = "AHA/compressed_text.txt"
    decompressed_path = "AHA/decompressed_text.txt"

    adaptiveHaffmanCompress.encode(test_data_path, compressed_path)
    adaptiveHaffmanDecompress.decode(compressed_path, decompressed_path)

    with open(test_data_path, "rb") as file_reader:
        orig_data = file_reader.read()

    with open(compressed_path, "rb") as file_reader:
        encode_data = file_reader.read()

    with open(decompressed_path, "rb") as file_reader:
        decode_data = file_reader.read()


    print(orig_data == decode_data)
    print("Adaptive Haffman Compress: ", len(encode_data))


    # 5645362 - 2


if __name__ == "__main__":
    test_compress()
