from source.BurrowsWheeleTransform.BWT import BWT
from source.RunLenEncode.RLE import RLE


class BWT_RLE:  # BWT + RLE
    def __init__(self):
        self.rle = RLE()
        self.bwt = BWT()
        self.intermediate_path = "../files/intermediate_file.txt"

    def encode(self, input_path: str, output_path: str):
        self.bwt.encode(input_path, self.intermediate_path)
        self.rle.encode(self.intermediate_path, output_path)

    def decode(self, input_path: str, output_path: str):
        self.rle.decode(input_path, self.intermediate_path)
        self.bwt.decode(self.intermediate_path, output_path)


if __name__ == "__main__":
    test_data_path = "../files/enwik7.txt"
    # test_data_path = "test.txt"
    compressed_path = "compressed_text.txt"
    decompressed_path = "decompressed_text.txt"

    bwt_rle = BWT_RLE()

    N_sizes = [100, 1000, 5_000, 10_000, 25_000, 50_000, 75_000, 100_000, 250_000, 350_000, 500_000, 750_000, 1_000_000]
    result_file_sizes = []
    for size in N_sizes:
        bwt_rle.bwt.N = size
        bwt_rle.encode(test_data_path, compressed_path)

        with open(compressed_path, "rb") as file_reader:
            encode_data = file_reader.read()

        result_file_sizes.append(len(encode_data))
    print(result_file_sizes)


    # bwt_rle.encode(test_data_path, compressed_path)
    # bwt_rle.decode(compressed_path, decompressed_path)
    #
    # with open(test_data_path, "rb") as file_reader:
    #     orig_data = file_reader.read()
    #
    # with open(compressed_path, "rb") as file_reader:
    #     encode_data = file_reader.read()
    #
    # with open(decompressed_path, "rb") as file_reader:
    #     decode_data = file_reader.read()
    #
    # print(len(orig_data))
    # print(len(encode_data))
    # print(len(decode_data))
    #
    # print(orig_data == decode_data)
