class MTF:
    def encode(self, file_path_read, file_path_write):
        with open(file_path_read, "rb") as file_read:
            data = file_read.read()
            with open(file_path_write, "wb") as file_write:
                alphabet = self.getAlphabet(data)
                file_write.write(len(alphabet).to_bytes(1, byteorder="big"))
                file_write.write(alphabet)
                for char in data:
                    index = alphabet.index(char)
                    file_write.write(index.to_bytes(1, byteorder="big"))

                    record = alphabet[:]
                    alphabet[1:index + 1] = record[:index]
                    alphabet[0] = record[index]

    @staticmethod
    def decode(file_path_read, file_path_write):
        with open(file_path_read, "rb") as file_read:
            alphabet = bytearray()
            alphabet_length = int.from_bytes(file_read.read(1), byteorder="big")
            for i in range(alphabet_length):
                alphabet.extend(file_read.read(1))
            data = file_read.read()
            with open(file_path_write, "wb") as file_write:
                for index in data:
                    file_write.write(alphabet[index:index + 1:])
                    record = alphabet[:]
                    alphabet[1:index + 1] = record[:index]
                    alphabet[0] = record[index]

    @staticmethod
    def getAlphabet(data: bytes) -> bytearray:
        alphabet: bytearray = bytearray()
        for i in range(len(data)):
            if data[i:i + 1] not in alphabet:
                alphabet.extend(data[i:i + 1])

        return alphabet


if __name__ == "__main__":
    mtf = MTF()

    test_data_path = "../../files/enwik7.txt"
    # test_data_path = "MTF/original_text.txt"
    compressed_path = "MTF/compressed_text.txt"
    decompressed_path = "MTF/decompressed_text.txt"

    mtf.encode(test_data_path, compressed_path)
    mtf.decode(compressed_path,decompressed_path)

    with open(test_data_path, "rb") as file_reader:
        original_data = file_reader.read()

    with open(decompressed_path, "rb") as file_reader:
        decode_data = file_reader.read()

    print(original_data == decode_data)
