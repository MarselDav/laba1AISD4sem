from source.BurrowsWheeleTransform.BWT import BWT
from source.MoveToFront.MTF import MTF
from source.AdaptiveHaffmanCoding.AdaptiveHaffmanCompress import AHA_COMPRESS
from source.AdaptiveHaffmanCoding.AdaptiveHaffmanDecompress import AHA_DECOMPRESS
from source.RunLenEncode.RLE import RLE


class BWT_MTF_RLE_AHA:  # BWT + MTF + RLE + AHA
    def __init__(self):
        self.mtf = MTF()
        self.bwt = BWT()
        self.rle = RLE()
        self.adaptive_haffman_compress = AHA_COMPRESS()
        self.adaptive_haffman_decompress = AHA_DECOMPRESS()
        self.intermediate1_path = "intermediate_file1.txt"
        self.intermediate2_path = "intermediate_file2.txt"

    def encode(self, input_path: str, output_path: str):
        self.bwt.encode(input_path, self.intermediate1_path)
        self.mtf.encode(self.intermediate1_path, self.intermediate2_path)
        self.rle.encode(self.intermediate2_path, self.intermediate1_path)
        self.adaptive_haffman_compress.encode(self.intermediate1_path, output_path)

    def decode(self, input_path: str, output_path: str):
        self.adaptive_haffman_decompress.decode(input_path, self.intermediate1_path)
        self.rle.decode(self.intermediate1_path, self.intermediate2_path)
        self.mtf.decode(self.intermediate2_path, self.intermediate1_path)
        self.bwt.decode(self.intermediate1_path, output_path)

def test_compress():
    test_data_path = "files/enwik8.txt"
    compressed_path = "compressed_text.txt"
    decompressed_path = "decompressed_text.txt"

    bwt_mtf_aha = BWT_MTF_RLE_AHA()
    bwt_mtf_aha.encode(test_data_path, compressed_path)
    # bwt_mtf_aha.decode(compressed_path, decompressed_path)

    with open(test_data_path, "rb") as file_reader:
        orig_data = file_reader.read()

    with open(compressed_path, "rb") as file_reader:
        encode_data = file_reader.read()

    # with open(decompressed_path, "rb") as file_reader:
    #     decode_data = file_reader.read()

    print("BWT_MTF_RLE_AHA: ", len(encode_data))

if __name__ == "__main__":
    test_compress()
