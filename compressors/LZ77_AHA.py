from source.AdaptiveHaffmanCoding.AdaptiveHaffmanCompress import AHA_COMPRESS
from source.AdaptiveHaffmanCoding.AdaptiveHaffmanDecompress import AHA_DECOMPRESS
from source.LempelZiv.LZ77 import LZ77


class LZ77_AHA:  # LZ77 + AHA
    def __init__(self):
        self.lz77 = LZ77()
        self.adaptive_haffman_compress = AHA_COMPRESS()
        self.adaptive_haffman_decompress = AHA_DECOMPRESS()
        self.intermediate_path = "intermediate_file1.txt"

    def encode(self, input_path: str, output_path: str):
        self.lz77.encode(input_path, self.intermediate_path)
        self.adaptive_haffman_compress.encode(self.intermediate_path, output_path)

    def decode(self, input_path: str, output_path: str):
        self.adaptive_haffman_decompress.decode(input_path, self.intermediate_path)
        self.lz77.decode(self.intermediate_path, output_path)


def test_compress():
    test_data_path = "files/enwik8.txt"
    compressed_path = "compressed_text.txt"
    decompressed_path = "decompressed_text.txt"

    lz77_aha = LZ77_AHA()
    lz77_aha.encode(test_data_path, compressed_path)
    # lz77_aha.decode(compressed_path, decompressed_path)

    with open(test_data_path, "rb") as file_reader:
        orig_data = file_reader.read()

    with open(compressed_path, "rb") as file_reader:
        encode_data = file_reader.read()

    # with open(decompressed_path, "rb") as file_reader:
    #     decode_data = file_reader.read()

    print("LZ77_AHA: ", len(encode_data))


if __name__ == "__main__":
    test_compress()
