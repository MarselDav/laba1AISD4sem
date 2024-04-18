from source.HaffmanCoding.HuffmanCoding import HuffmanCoding
from source.LempelZiv.LZ77 import LZ77


class LZ77_HA:  # LZ77 + HA
    def __init__(self):
        self.lz77 = LZ77()
        self.haffman = HuffmanCoding()
        self.intermediate_path = "intermediate_file1.txt"

    def encode(self, input_path: str, output_path: str):
        self.lz77.encode(input_path, self.intermediate_path)
        self.haffman.encode(self.intermediate_path, output_path)

    def decode(self, input_path: str, output_path: str):
        self.haffman.decode(input_path, self.intermediate_path)
        self.lz77.decode(self.intermediate_path, output_path)

def test_compress(length):
    test_data_path = "files/enwik8.txt"
    compressed_path = "compressed_text.txt"
    decompressed_path = "decompressed_text.txt"

    lz77_ha = LZ77_HA()
    lz77_ha.haffman.sequence_len = length
    lz77_ha.encode(test_data_path, compressed_path)
    # lz77_ha.decode(compressed_path, decompressed_path)

    with open(test_data_path, "rb") as file_reader:
        orig_data = file_reader.read()

    with open(compressed_path, "rb") as file_reader:
        encode_data = file_reader.read()

    # with open(decompressed_path, "rb") as file_reader:
    #     decode_data = file_reader.read()

    print(f"LZ77_HA {length}: ", len(encode_data))


if __name__ == "__main__":
    test_compress(1)
