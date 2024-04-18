# import divsufsort
import sufarray

class BWT:
    def __init__(self):
        self.N = 100_000_000
        self.bytes_to_write_index = 4

    def encode(self, file_path_read, file_path_write):
        with open(file_path_read, "rb") as file_read:
            with open(file_path_write, "wb") as file_write:
                temp = 0
                while True:
                    data: bytes = file_read.read(self.N)
                    if not data:
                        break
                    index_pos = file_write.tell()
                    file_write.write(temp.to_bytes(self.bytes_to_write_index, byteorder="big"))

                    simb = 1
                    data += simb.to_bytes(1, byteorder="big")

                    sarray = sufarray.SufArray(data)
                    suffix_array = sarray.get_array()

                    # suffix_array = divsufsort.divsufsort(data)
                    index = suffix_array.index(0)

                    for i in range(len(suffix_array)):
                        j = suffix_array[i] - 1
                        if j < 0:
                            j += len(suffix_array)
                        file_write.write(data[j:j + 1:])

                    current_pos = file_write.tell()
                    file_write.seek(index_pos)
                    file_write.write(index.to_bytes(self.bytes_to_write_index, byteorder="big"))
                    file_write.seek(current_pos)

    @staticmethod
    def decode_algorithm(file_write, data, ind):
        shifts = [(data[i:i + 1:], i) for i in range(len(data))]
        shifts.sort()
        new_indexes = list(zip(*shifts))[1]
        index = ind
        for _ in range(len(data) - 1):
            index = new_indexes[index]
            file_write.write(data[index:index + 1:])

    def decode(self, input_path, output_path):
        with open(input_path, "rb") as file_read:
            with open(output_path, "wb") as file_write:
                while True:
                    index = int.from_bytes(file_read.read(self.bytes_to_write_index), byteorder="big")
                    data = file_read.read(self.N + 1)
                    if not data:
                        break
                    self.decode_algorithm(file_write, data, index)


if __name__ == "__main__":
    # test_data_path = "../../files/enwik7.txt"
    test_data_path = "BWT/original_text.txt"
    compressed_path = "BWT/compressed_text.txt"
    decompressed_path = "BWT/decompressed_text.txt"

    # N_sizes = [100, 1000, 10_000, 100_000, 10_000_000]
    # for size in N_sizes:
    #     pass

    bwt = BWT()
    bwt.encode(test_data_path, compressed_path)
    bwt.decode(compressed_path, decompressed_path)

    with open(test_data_path, "rb") as file_reader:
        orig_data = file_reader.read()

    with open(compressed_path, "rb") as file_reader:
        encode_data = file_reader.read()

    with open(decompressed_path, "rb") as file_reader:
        decode_data = file_reader.read()

    print(orig_data == decode_data)
