class RLE:
    def __init__(self):
        self.MAX_LEN: int = 127

        self.MIN_LEN_DIFFRENT_SEQUENCE = 1
        self.MIN_LEN_SIMILAR_SEQUENCE = 2

        self.SIMILAR_TYPE = 0
        self.DIFFRENT_TYPE = 1

        self.MIN_LEN_SEQUENCE = 3

        self.LAST_DIFFRENT_SEQUENCE_LEN = 0
        self.LAST_DIFFRENT_SEQUENCE_POS = 0

    @staticmethod
    def find_duplets(data: bytes) -> set[tuple]:
        duplets_set = set()

        left = 0
        right = 2

        while right < len(data):
            if data[left] == data[left + 1] and data[left + 1] != data[right]:
                duplets_set.add((left, left + 1))
                left += 1
                right += 1
            left += 1
            right += 1

        return duplets_set

    def writeData(self, file_writer, type_: int, data: bytes, length: int):
        subtracted = self.MIN_LEN_SIMILAR_SEQUENCE if type_ == 0 else self.MIN_LEN_DIFFRENT_SEQUENCE

        MAX_LEN = self.MAX_LEN + subtracted

        while length > MAX_LEN:
            byte_value = (MAX_LEN - subtracted << 1) | type_
            file_writer.write(byte_value.to_bytes(1, byteorder="big"))

            if type_ == 0:
                file_writer.write(data)
            else:
                file_writer.write(data[0:MAX_LEN])
                data = data[MAX_LEN::]

            length -= MAX_LEN

        if length < subtracted:
            byte_value = (length - self.MIN_LEN_DIFFRENT_SEQUENCE << 1) | self.DIFFRENT_TYPE
            self.LAST_DIFFRENT_SEQUENCE_POS = file_writer.tell()
            self.LAST_DIFFRENT_SEQUENCE_LEN = length
        else:
            byte_value = (length - subtracted << 1) | type_
            self.LAST_DIFFRENT_SEQUENCE_LEN = 0

        file_writer.write(byte_value.to_bytes(1, byteorder="big"))
        file_writer.write(data)


    def encode(self, input_path: str, output_path: str):
        with open(input_path, "rb") as file_reader:
            file_data = file_reader.read()
            with open(output_path, "wb") as file_writer:
                duplets = self.find_duplets(file_data)
                # duplets = {}

                i = 0
                j = 0
                data_len = len(file_data)

                while i < data_len - 1:

                    j = i
                    while j + 1 < data_len and file_data[j] == file_data[j + 1]:
                        j += 1

                    if j != i:
                        self.writeData(file_writer, self.SIMILAR_TYPE, file_data[i:i + 1], j - i + 1)
                        i = j + 1

                    j = i
                    while j + 1 < data_len and (file_data[j] != file_data[j + 1] or (j, j + 1) in duplets):
                        j += 1

                    if j != i:
                        if j == data_len - 1:
                            self.writeData(file_writer, self.DIFFRENT_TYPE, file_data[i:j + 1], j - i + 1)
                            return

                        self.writeData(file_writer, self.DIFFRENT_TYPE, file_data[i:j], j - i)
                        i = j

                if j == data_len - 1:
                    self.writeData(file_writer, self.DIFFRENT_TYPE, file_data[j:j + 1], 1)

    def decode(self, input_path: str, output_path: str):
        with open(input_path, "rb") as file_reader:
            with open(output_path, "wb") as file_writer:
                while True:
                    byte_value = file_reader.read(1)
                    if not byte_value:
                        break

                    byte_value = int.from_bytes(byte_value, byteorder="big")
                    type_ = byte_value & 1
                    length = byte_value >> 1

                    if type_ == 0:  # повторяющийся символ
                        symbol = file_reader.read(1)
                        file_writer.write(symbol * (length + self.MIN_LEN_SIMILAR_SEQUENCE))
                    else:  # неповторяющиеся символы
                        data = file_reader.read(length + self.MIN_LEN_DIFFRENT_SEQUENCE)
                        file_writer.write(data)


if __name__ == "__main__":
    # test_data_path = "../../files/enwik7.txt"
    test_data_path = "RLE/original_text.txt"
    compressed_path = "RLE/compressed_text.txt"
    decompressed_path = "RLE/decompressed_text.txt"

    # print("a" * 258) # 260
    rle = RLE()
    rle.encode(test_data_path, compressed_path)
    rle.decode(compressed_path, decompressed_path)

    with open(test_data_path, "rb") as file_reader:
        orig_data = file_reader.read()

    with open(compressed_path, "rb") as file_reader:
        encode_data = file_reader.read()

    with open(decompressed_path, "rb") as file_reader:
        decode_data = file_reader.read()


# class RLE:
#     def __init__(self):
#         self.MAX_LEN: int = 127
#
#         self.MIN_LEN_DIFFRENT_SEQUENCE = 1
#         self.MIN_LEN_SIMILAR_SEQUENCE = 2
#
#         self.SIMILAR_TYPE = 0
#         self.DIFFRENT_TYPE = 1
#
#         self.MIN_LEN_SEQUENCE = 3
#
#         self.LAST_DIFFRENT_SEQUENCE_LEN = 0
#         self.LAST_DIFFRENT_SEQUENCE_POS = 0
#
#     @staticmethod
#     def find_duplets(data: bytes) -> set[tuple]:
#         duplets_set = set()
#
#         left = 0
#         right = 2
#
#         while right < len(data):
#             if data[left] == data[left + 1] and data[left + 1] != data[right]:
#                 duplets_set.add((left, left + 1))
#                 left += 1
#                 right += 1
#             left += 1
#             right += 1
#
#         return duplets_set
#
#     def writeData(self, file_writer, type_: int, data: bytes, length: int):
#         subtracted = self.MIN_LEN_SIMILAR_SEQUENCE if type_ == 0 else self.MIN_LEN_DIFFRENT_SEQUENCE
#
#         MAX_LEN = self.MAX_LEN + subtracted
#
#         while length > MAX_LEN:
#             byte_value = (MAX_LEN - subtracted << 1) | type_
#             file_writer.write(byte_value.to_bytes(1, byteorder="big"))
#
#             if type_ == 0:
#                 file_writer.write(data)
#             else:
#                 file_writer.write(data[0:MAX_LEN])
#                 data = data[MAX_LEN::]
#
#             length -= MAX_LEN
#
#         if length < subtracted:
#             byte_value = (length - self.MIN_LEN_DIFFRENT_SEQUENCE << 1) | self.DIFFRENT_TYPE
#             self.LAST_DIFFRENT_SEQUENCE_POS = file_writer.tell()
#             self.LAST_DIFFRENT_SEQUENCE_LEN = length
#         else:
#             byte_value = (length - subtracted << 1) | type_
#             self.LAST_DIFFRENT_SEQUENCE_LEN = 0
#
#         file_writer.write(byte_value.to_bytes(1, byteorder="big"))
#         file_writer.write(data)
#
#     def writeToLastDiffrentSequenceData(self, file_writer, data: bytes, length: int):
#         # if 0 < self.LAST_DIFFRENT_SEQUENCE_LEN < self.MAX_LEN:
#         #     MAX_LEN = self.MAX_LEN - self.LAST_DIFFRENT_SEQUENCE_LEN + self.MIN_LEN_DIFFRENT_SEQUENCE
#         #
#         #
#         #     current_pos = file_writer.tell()
#         #     file_writer.seek(self.LAST_DIFFRENT_SEQUENCE_POS)
#         #
#         #     byte_value = (MAX_LEN - self.MIN_LEN_DIFFRENT_SEQUENCE << 1) | self.DIFFRENT_TYPE
#         #     file_writer.write(byte_value.to_bytes(1, byteorder="big"))
#         #
#         #     file_writer.seek(current_pos)
#         #     file_writer.write(data[0:MAX_LEN])
#         #
#         #     if length > MAX_LEN:
#         #         self.writeData(file_writer, self.DIFFRENT_TYPE, data[MAX_LEN::], length - MAX_LEN)
#         #         self.LAST_DIFFRENT_SEQUENCE_LEN = 0
#         #     else:
#         #         self.LAST_DIFFRENT_SEQUENCE_LEN = MAX_LEN - length
#         #
#         # self.writeData(file_writer, self.DIFFRENT_TYPE, data, length)
#
#         if 0 < self.LAST_DIFFRENT_SEQUENCE_LEN < self.MAX_LEN:
#             MAX_LEN = self.MAX_LEN - self.LAST_DIFFRENT_SEQUENCE_LEN + self.MIN_LEN_DIFFRENT_SEQUENCE
#
#             if length > MAX_LEN:
#                 current_pos = file_writer.tell()
#                 file_writer.seek(self.LAST_DIFFRENT_SEQUENCE_POS)
#
#                 byte_value = (MAX_LEN - self.MIN_LEN_DIFFRENT_SEQUENCE << 1) | self.DIFFRENT_TYPE
#                 file_writer.write(byte_value.to_bytes(1, byteorder="big"))
#
#                 file_writer.seek(current_pos)
#                 file_writer.write(data[0:MAX_LEN])
#
#                 self.writeData(file_writer, self.DIFFRENT_TYPE, data[MAX_LEN::], length - MAX_LEN)
#             else:
#                 current_pos = file_writer.tell()
#                 file_writer.seek(self.LAST_DIFFRENT_SEQUENCE_POS)
#                 # print(length + self.LAST_DIFFRENT_SEQUENCE_LEN - 2 * self.MIN_LEN_DIFFRENT_SEQUENCE )
#                 # 12
#                 byte_value = (length + self.LAST_DIFFRENT_SEQUENCE_LEN - self.MIN_LEN_DIFFRENT_SEQUENCE << 1) | self.DIFFRENT_TYPE
#                 file_writer.write(byte_value.to_bytes(1, byteorder="big"))
#
#                 file_writer.seek(current_pos)
#                 file_writer.write(data)
#                 self.LAST_DIFFRENT_SEQUENCE_LEN = MAX_LEN - length
#         else:
#             self.writeData(file_writer, self.DIFFRENT_TYPE, data, length)
#
#     def encode(self, input_path: str, output_path: str):
#         with open(input_path, "rb") as file_reader:
#             file_data = file_reader.read()
#             with open(output_path, "wb") as file_writer:
#                 duplets = self.find_duplets(file_data)
#                 # duplets = {}
#
#                 i = 0
#                 j = 0
#                 data_len = len(file_data)
#
#                 while i < data_len - 1:
#
#                     j = i
#                     while j + 1 < data_len and file_data[j] == file_data[j + 1]:
#                         j += 1
#
#                     if j != i:
#                         self.writeData(file_writer, self.SIMILAR_TYPE, file_data[i:i + 1], j - i + 1)
#                         i = j + 1
#
#                     j = i
#                     while j + 1 < data_len and (file_data[j] != file_data[j + 1] or (j, j + 1) in duplets):
#                         j += 1
#
#                     if j != i:
#                         if j == data_len - 1:
#                             self.writeToLastDiffrentSequenceData(file_writer, file_data[i:j + 1], j - i + 1)
#                             # self.writeData(file_writer, self.DIFFRENT_TYPE, file_data[i:j + 1], j - i + 1)
#                             return
#
#                         # self.writeData(file_writer, self.DIFFRENT_TYPE, file_data[i:j], j - i)
#                         self.writeToLastDiffrentSequenceData(file_writer, file_data[i:j], j - i)
#                         i = j
#
#                 if j == data_len - 1:
#                     # self.writeData(file_writer, self.DIFFRENT_TYPE, file_data[j:j + 1], 1)
#                     self.writeToLastDiffrentSequenceData(file_writer, file_data[j:j + 1], 1)
#
#     def decode(self, input_path: str, output_path: str):
#         with open(input_path, "rb") as file_reader:
#             with open(output_path, "wb") as file_writer:
#                 while True:
#                     byte_value = file_reader.read(1)
#                     if not byte_value:
#                         break
#
#                     byte_value = int.from_bytes(byte_value, byteorder="big")
#                     type_ = byte_value & 1
#                     length = byte_value >> 1
#
#                     if type_ == 0:  # повторяющийся символ
#                         symbol = file_reader.read(1)
#                         file_writer.write(symbol * (length + self.MIN_LEN_SIMILAR_SEQUENCE))
#                     else:  # неповторяющиеся символы
#                         data = file_reader.read(length + self.MIN_LEN_DIFFRENT_SEQUENCE)
#                         file_writer.write(data)
#
#
# if __name__ == "__main__":
#     # test_data_path = "../../files/enwik7.txt"
#     test_data_path = "RLE/original_text.txt"
#     compressed_path = "RLE/compressed_text.txt"
#     decompressed_path = "RLE/decompressed_text.txt"
#
#     # print("a" * 258) # 260
#     rle = RLE()
#     rle.encode(test_data_path, compressed_path)
#     rle.decode(compressed_path, decompressed_path)
#
#     with open(test_data_path, "rb") as file_reader:
#         orig_data = file_reader.read()
#
#     with open(compressed_path, "rb") as file_reader:
#         encode_data = file_reader.read()
#
#     with open(decompressed_path, "rb") as file_reader:
#         decode_data = file_reader.read()
#
#     # print(len(orig_data))
#     # print(len(encode_data))
#     # print(len(decode_data))
#     # print(orig_data == decode_data)
#
#     for i in range(10_000):
#         with open(test_data_path, "wb") as file_write:
#             file_write.write(b"sdasdgasdas" + b"a" * i + b"sdasdgasdas")
#
#         rle.encode(test_data_path, compressed_path)
#         rle.decode(compressed_path, decompressed_path)
#
#         with open(test_data_path, "rb") as file_reader:
#             orig_data = file_reader.read()
#
#         with open(compressed_path, "rb") as file_reader:
#             encode_data = file_reader.read()
#
#         with open(decompressed_path, "rb") as file_reader:
#             decode_data = file_reader.read()
#
#         # print(len(encode_data))
#         # print(decode_data)
#         # print(orig_data)
#         if orig_data != decode_data:
#             print(len(decode_data))
#             print(decode_data)
#             print(orig_data)
#             print(i)
#             break
