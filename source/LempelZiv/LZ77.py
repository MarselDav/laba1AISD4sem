class LZ77:
    def __init__(self):
        self.buff_size = 60_000
        self.bytes_cnt_for_offset_and_len = 2
        self.minimum_sequence_len = 3
        self.data = bytes()

    def findMatching(self, buffer: [int, int], pos: int) -> (int, int):
        start_buffer = buffer[0] if buffer[0] > 0 else 0
        length = 0
        buff_size = buffer[1] - start_buffer
        _index = buff_size
        for i in range(self.minimum_sequence_len, buff_size + 1):
            index = self.data[start_buffer:buffer[1]:].rfind(self.data[pos:pos + i:])
            if index != -1:
                _index = index
                length = i
            else:
                break

        return buff_size - _index, length

    @staticmethod
    def writeInFile(file_writer, type_, pos_start_sequence, cnt):
        current_pos = file_writer.tell()
        file_writer.seek(pos_start_sequence)
        byte_value = (cnt << 1) | type_
        file_writer.write(byte_value.to_bytes(1, byteorder="big"))

        file_writer.seek(current_pos)

    def encode(self, file_path_read, file_path_write):
        with open(file_path_read, "rb") as file_read:
            with open(file_path_write, "wb") as file_write:
                simb = 1
                self.data = file_read.read() + simb.to_bytes(1, byteorder="big")

                pos_start_sequence = 0
                cnt_solo = 0
                cnt_with_offset = 0

                buffer = [-self.buff_size, 0]  # start, end_index

                pos = 0
                while pos < len(self.data):
                    offset, length = self.findMatching(buffer, pos)

                    if buffer[0] + length == pos and length > 0:
                        j = pos
                        length_of_substring = length
                        while j + length_of_substring < len(self.data) - 1:
                            if self.data[j] == self.data[j + length_of_substring]:
                                length += 1
                            else:
                                break

                            j += 1

                    buffer[0] += length + 1
                    buffer[1] += length + 1
                    pos += length + 1

                    if offset == 0 and length == 0:
                        if pos >= len(self.data) or cnt_solo == 127:
                            self.writeInFile(file_write, 0, pos_start_sequence, cnt_solo)
                            cnt_solo = 0

                        if cnt_solo == 0:
                            if cnt_with_offset > 0:
                                self.writeInFile(file_write, 1, pos_start_sequence, cnt_with_offset)
                                cnt_with_offset = 0

                            pos_start_sequence = file_write.tell()
                            file_write.write(b'0')

                        cnt_solo += 1
                    else:
                        if cnt_with_offset == 127:
                            self.writeInFile(file_write, 1, pos_start_sequence, cnt_with_offset)
                            cnt_with_offset = 0

                        if cnt_with_offset == 0:
                            if cnt_solo > 0:
                                self.writeInFile(file_write, 0, pos_start_sequence, cnt_solo)
                                cnt_solo = 0

                            pos_start_sequence = file_write.tell()
                            file_write.write(b'0')

                        file_write.write(offset.to_bytes(self.bytes_cnt_for_offset_and_len, byteorder="big"))
                        file_write.write(length.to_bytes(self.bytes_cnt_for_offset_and_len, byteorder="big"))
                        cnt_with_offset += 1

                        if pos >= len(self.data):
                            self.writeInFile(file_write, 1, pos_start_sequence, cnt_with_offset)

                    if pos < len(self.data):
                        file_write.write(self.data[pos - 1:pos:])

    def decode(self, file_path_read, file_path_write):
        with open(file_path_read, "rb") as file_reader:
            with open(file_path_write, "w+b") as file_writer:
                data_len = 0

                while True:
                    byte_value = file_reader.read(1)
                    if not byte_value:
                        break

                    byte_value = int.from_bytes(byte_value, byteorder="big")
                    type_ = byte_value & 1
                    length = byte_value >> 1

                    if type_ == 0:
                        data = file_reader.read(length)
                        file_writer.write(data)
                        data_len += length
                    else:
                        i = 0
                        while i < length:
                            offset = int.from_bytes(file_reader.read(self.bytes_cnt_for_offset_and_len),
                                                    byteorder="big")
                            substr_length = int.from_bytes(file_reader.read(self.bytes_cnt_for_offset_and_len),
                                                           byteorder="big")
                            simbol_after_string = file_reader.read(1)

                            write_pos = file_writer.tell()

                            for j in range(substr_length):
                                file_writer.seek(data_len - offset)
                                byte_value = file_writer.read(1)
                                file_writer.seek(write_pos)
                                file_writer.write(byte_value)

                                data_len += 1
                                write_pos += 1

                            file_writer.write(simbol_after_string)
                            data_len += 1

                            i += 1


if __name__ == "__main__":
    lz77 = LZ77()
    test_data_path = "../../files/enwik7.txt"
    # test_data_path = "LZ77/original_text.txt"
    compressed_path = "LZ77/compressed_text.txt"
    decompressed_path = "LZ77/decompressed_text.txt"

    # buff_sizes = [255, 1000, 5000, 10000, 25000, 35000, 45000, 60000]
    # # [255, 1000, 5000, 10000, 25000, 35000, 45000, 60000]
    # # [8409210, 9666360, 8519059, 7936130, 7196241, 6964148, 6800435, 6624621]
    # result_file_sizes = []
    # for size in buff_sizes:
    #     if size == 255:
    #         lz77.bytes_cnt_for_offset_and_len = 1
    #     else:
    #         lz77.bytes_cnt_for_offset_and_len = 2
    #     lz77.buff_size = size
    #     lz77.encode(test_data_path, compressed_path)
    #     with open(compressed_path, "rb") as file_reader:
    #         encode_data = file_reader.read()
    #         result_file_sizes.append(len(encode_data))
    #
    # print(result_file_sizes)

    lz77.encode(test_data_path, compressed_path)
    lz77.decode(compressed_path, decompressed_path)

    with open(test_data_path, "rb") as file_reader:
        orig_data = file_reader.read()

    with open(compressed_path, "rb") as file_reader:
        encode_data = file_reader.read()

    with open(decompressed_path, "rb") as file_reader:
        decode_data = file_reader.read()

    print(len(orig_data))
    print(len(encode_data))
    print(len(decode_data))

    print(orig_data == decode_data)

    # import io
    #
    #
    # class LZ77:
    #     def __init__(self):
    #         self.buff_size = 60_000
    #         self.buff_start_index = 0
    #         self.buffer = bytearray()
    #         self.bytes_cnt_for_offset_and_len = 2
    #         self.minimum_sequence_len = 3
    #         self.simb = 1
    #
    #
    #     def findMatching(self, byte, file_reader) -> (int, int):
    #         byte_sequence = b'' + byte
    #         # while len(byte_sequence) < self.minimum_sequence_len:
    #         #     byte_sequence += file_reader.read(1)
    #
    #         buff_size = len(self.buffer)
    #         length = 0
    #         _index = buff_size
    #         for i in range(1, buff_size + 1):
    #             index = self.buffer.rfind(byte_sequence)
    #             if index != -1:
    #                 _index = index
    #                 length = i
    #             else:
    #                 break
    #
    #             byte = file_reader.read(1)
    #             if byte:
    #                 byte_sequence += byte
    #             else:
    #                 break
    #         # print(buff_size - _index, length, byte_sequence)
    #         if length == 1:
    #             return 0, 0, byte_sequence
    #         return buff_size - _index, length, byte_sequence
    #
    #     @staticmethod
    #     def writeInFile(file_writer, type_, pos_start_sequence, cnt):
    #         current_pos = file_writer.tell()
    #         file_writer.seek(pos_start_sequence)
    #         byte_value = (cnt << 1) | type_
    #         file_writer.write(byte_value.to_bytes(1, byteorder="big"))
    #
    #         file_writer.seek(current_pos)
    #
    #     def encode(self, file_path_read, file_path_write):
    #         with open(file_path_read, "rb") as file_reader:
    #             file_is_end = False
    #             pos_start_sequence = 0
    #             cnt_solo = 0
    #             cnt_with_offset = 0
    #             pos = 0
    #             with open(file_path_write, "wb") as file_writer:
    #                 byte = file_reader.read(1)
    #
    #                 while True:
    #                     if not byte:
    #                         byte = self.simb.to_bytes(1, byteorder="big")
    #                         file_is_end = True
    #
    #
    #                     offset, length, byte_sequence = self.findMatching(byte, file_reader)
    #
    #                     byte = byte_sequence[len(byte_sequence) - 1: len(byte_sequence)]
    #
    #                     pos += length + 1
    #                     if offset == 0 and length == 0:
    #                         if file_is_end or cnt_solo == 127:
    #                             self.writeInFile(file_writer, 0, pos_start_sequence, cnt_solo)
    #                             cnt_solo = 0
    #
    #                         if cnt_solo == 0:
    #                             if cnt_with_offset > 0:
    #                                 self.writeInFile(file_writer, 1, pos_start_sequence, cnt_with_offset)
    #                                 cnt_with_offset = 0
    #
    #                             pos_start_sequence = file_writer.tell()
    #                             file_writer.write(b'0')
    #
    #                         cnt_solo += 1
    #                     else:
    #                         if cnt_with_offset == 127:
    #                             self.writeInFile(file_writer, 1, pos_start_sequence, cnt_with_offset)
    #                             cnt_with_offset = 0
    #
    #                         if cnt_with_offset == 0:
    #                             if cnt_solo > 0:
    #                                 self.writeInFile(file_writer, 0, pos_start_sequence, cnt_solo)
    #                                 cnt_solo = 0
    #
    #                             pos_start_sequence = file_writer.tell()
    #                             file_writer.write(b'0')
    #
    #                         file_writer.write(offset.to_bytes(self.bytes_cnt_for_offset_and_len, byteorder="big"))
    #                         file_writer.write(length.to_bytes(self.bytes_cnt_for_offset_and_len, byteorder="big"))
    #                         cnt_with_offset += 1
    #
    #                         if file_is_end:
    #                             self.writeInFile(file_writer, 1, pos_start_sequence, cnt_with_offset)
    #
    #                     if not file_is_end:
    #                         file_writer.write(byte)
    #
    #                     # print(f"({offset}, {length}, {byte})", end=", ")
    #
    #                     # print(byte_sequence)
    #                     # if len(byte_sequence) > 1:
    #                     #     byte = byte_sequence[len(byte_sequence) - 1: len(byte_sequence)]
    #                     #     for i in range(len(byte_sequence) - 1):
    #                     #         if len(self.buffer) >= self.buff_size:
    #                     #             self.buffer.pop(0)
    #                     #             self.buff_start_index += 1
    #                     #         self.buffer.extend(byte_sequence[i:i+1])
    #                     # else:
    #                     #     byte = file_reader.read(1)
    #                     #     self.buffer.extend(byte_sequence[0:1])
    #                     for i in range(len(byte_sequence)):
    #                         if len(self.buffer) >= self.buff_size:
    #                             self.buffer.pop(0)
    #                             self.buff_start_index += 1
    #                         self.buffer.extend(byte_sequence[i:i + 1])
    #
    #                     byte = file_reader.read(1)
    #
    #                     if file_is_end:
    #                         return
    #
    #     def decode(self, file_path_read, file_path_write):
    #         with open(file_path_read, "rb") as file_reader:
    #             with open(file_path_write, "w+b") as file_writer:
    #                 data_len = 0
    #
    #                 while True:
    #                     byte_value = file_reader.read(1)
    #                     if not byte_value:
    #                         break
    #
    #                     byte_value = int.from_bytes(byte_value, byteorder="big")
    #                     type_ = byte_value & 1
    #                     length = byte_value >> 1
    #
    #                     if type_ == 0:
    #                         data = file_reader.read(length)
    #                         file_writer.write(data)
    #                         data_len += length
    #                     else:
    #                         i = 0
    #                         while i < length:
    #                             offset = int.from_bytes(file_reader.read(self.bytes_cnt_for_offset_and_len),
    #                                                     byteorder="big")
    #                             substr_length = int.from_bytes(file_reader.read(self.bytes_cnt_for_offset_and_len),
    #                                                            byteorder="big")
    #                             simbol_after_string = file_reader.read(1)
    #
    #                             write_pos = file_writer.tell()
    #
    #                             for j in range(substr_length):
    #                                 file_writer.seek(data_len - offset)
    #                                 byte_value = file_writer.read(1)
    #                                 file_writer.seek(write_pos)
    #                                 file_writer.write(byte_value)
    #
    #                                 data_len += 1
    #                                 write_pos += 1
    #
    #                             file_writer.write(simbol_after_string)
    #                             data_len += 1
    #
    #                             i += 1