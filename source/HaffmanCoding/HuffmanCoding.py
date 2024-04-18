# import pickle
# from queue import PriorityQueue
#
#
# class Node:
#     __slots__ = ["char", "freq", "left", "right"]
#     def __init__(self, char, f):
#         self.char = char
#         self.freq = f
#         self.left = None
#         self.right = None
#
#     def __lt__(self, other):
#         return self.freq < other.freq
#
#
# class HuffmanCoding:
#     def __init__(self):
#         self.huffmanCodes: dict[bytes, str] = {}
#         self.sequence_len = 1
#
#     @staticmethod
#     def writeSimbols(file_write, current_code) -> str:
#         while len(current_code) >= 8:
#             code_to_write = current_code[:8:]
#             num = int(code_to_write, 2)
#             file_write.write(num.to_bytes(1, byteorder="big"))
#             current_code = current_code[8::]
#         return current_code
#
#     def encode(self, input_path, output_path):
#         with open(input_path, "rb") as file_read:
#             data: bytes = file_read.read()
#
#             frequency: dict[bytes, int] = self.getFrequency(data)
#             node: Node = self.getHuffmanTree(frequency)
#             self.getHuffmanCodes(node, str())
#
#             current_code = ""
#             with open(output_path, "wb") as file_write:
#                 code_to_dump = {pair: int("1" + self.huffmanCodes[pair], 2) for pair in self.huffmanCodes}
#                 pickle.dump(code_to_dump, file_write)
#                 file_write.write(b'\n')
#                 end_dict_pos = file_write.tell()
#                 file_write.write(b'0')
#
#                 for i in range(0, len(data), self.sequence_len):
#                     current_code += self.huffmanCodes[data[i:i + self.sequence_len]]
#                     if len(current_code) >= 8:
#                         current_code = self.writeSimbols(file_write, current_code)
#
#                 current_code = self.writeSimbols(file_write, current_code)
#
#                 last_bits_cnt = len(current_code)
#                 if last_bits_cnt > 0:
#                     current_code = current_code.ljust(8, "0")
#                     self.writeSimbols(file_write, current_code)
#                 else:
#                     last_bits_cnt = 8
#                 file_write.seek(end_dict_pos)
#                 file_write.write(last_bits_cnt.to_bytes(1, byteorder="big"))
#
#     @staticmethod
#     def decode(input_path: str, output_path: str):
#         with open(input_path, "rb") as file_read:
#             huffman_dict = pickle.load(file_read)
#             huffmanReverseCodes: dict[bytes, str] = {bin(huffman_dict[i])[3::]: i for i in huffman_dict.keys()}
#             file_read.readline()
#             pos = file_read.tell()
#
#             with open(output_path, "wb") as file_write:
#                 file_read.seek(0, 2)
#                 file_size = file_read.tell() - pos - 1
#                 file_read.seek(pos)
#
#                 current_code_str = ""
#
#                 last_bits_cnt = int.from_bytes(file_read.read(1), byteorder='big')
#
#                 for i in range(file_size):
#                     byte = file_read.read(1)
#                     code = bin(int.from_bytes(byte, byteorder="big"))
#                     if i == file_size - 1:
#                         current_code_str += code[2::].rjust(8, "0")[:last_bits_cnt:]
#                     else:
#                         current_code_str += code[2::].rjust(8, "0")
#                     j = 0
#                     while j < len(current_code_str):
#                         code = current_code_str[:j:]
#                         if code in huffmanReverseCodes:
#                             file_write.write(huffmanReverseCodes[code])
#                             current_code_str = current_code_str[j::]
#                             j = 0
#                         j += 1
#                 file_write.write(huffmanReverseCodes[current_code_str])
#
#     def getFrequency(self, data: bytes) -> dict[bytes, int]:
#         frequency: dict[bytes, int] = {}
#
#         for i in range(0, len(data), self.sequence_len):
#             if data[i:i + self.sequence_len] not in frequency:
#                 frequency[data[i:i + self.sequence_len]] = 0
#             frequency[data[i:i + self.sequence_len]] += 1
#
#         return frequency
#
#     @staticmethod
#     def getHuffmanTree(frequency: dict[bytes, int]) -> Node:
#         q = PriorityQueue()
#         for char in frequency.keys():
#             node = Node(char, frequency[char])
#             q.put(node)
#
#         while q.qsize() > 1:
#             node1 = q.get()
#             node2 = q.get()
#             node = Node(node1.char + node2.char, node1.freq + node2.freq)
#             node.left = node1
#             node.right = node2
#
#             q.put(node)
#
#         node = q.get()
#
#         return node
#
#     def getHuffmanCodes(self, node: Node, code: str):
#         if node is None:
#             return
#
#         if (node.left is None) and (node.right is None):
#             self.huffmanCodes[node.char] = code
#
#         self.getHuffmanCodes(node.left, code + "0")
#         self.getHuffmanCodes(node.right, code + "1")


import pickle
from queue import PriorityQueue


class Node:
    __slots__ = ["char", "freq", "left", "right"]

    def __init__(self, char, f):
        self.char = char
        self.freq = f
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


class HuffmanCoding:
    def __init__(self):
        self.huffmanCodes: dict[bytes, str] = {}
        self.sequence_len = 1

    @staticmethod
    def writeSimbols(file_write, current_code) -> str:
        while len(current_code) >= 8:
            code_to_write = current_code[:8:]
            num = int(code_to_write, 2)
            file_write.write(num.to_bytes(1, byteorder="big"))
            current_code = current_code[8::]
        return current_code

    def encode(self, input_path, output_path):
        with open(input_path, "rb") as file_read:
            frequency: dict[bytes, int] = self.getFrequency(file_read)
            file_read.seek(0)
            node: Node = self.getHuffmanTree(frequency)
            self.getHuffmanCodes(node, str())

            current_code = ""
            with open(output_path, "wb") as file_write:
                code_to_dump = {pair: int("1" + self.huffmanCodes[pair], 2) for pair in self.huffmanCodes}
                pickle.dump(code_to_dump, file_write)
                file_write.write(b'\n')
                end_dict_pos = file_write.tell()
                file_write.write(b'0')

                while True:
                    byte = file_read.read(self.sequence_len)
                    if not byte:
                        break
                    current_code += self.huffmanCodes[byte]
                    if len(current_code) >= 8:
                        current_code = self.writeSimbols(file_write, current_code)

                current_code = self.writeSimbols(file_write, current_code)

                last_bits_cnt = len(current_code)
                if last_bits_cnt > 0:
                    current_code = current_code.ljust(8, "0")
                    self.writeSimbols(file_write, current_code)
                else:
                    last_bits_cnt = 8
                file_write.seek(end_dict_pos)
                file_write.write(last_bits_cnt.to_bytes(1, byteorder="big"))

    @staticmethod
    def decode(input_path: str, output_path: str):
        with open(input_path, "rb") as file_read:
            huffman_dict = pickle.load(file_read)
            huffmanReverseCodes: dict[bytes, str] = {bin(huffman_dict[i])[3::]: i for i in huffman_dict.keys()}
            file_read.readline()
            pos = file_read.tell()

            with open(output_path, "wb") as file_write:
                file_read.seek(0, 2)
                file_size = file_read.tell() - pos - 1
                file_read.seek(pos)

                current_code_str = ""

                last_bits_cnt = int.from_bytes(file_read.read(1), byteorder='big')

                for i in range(file_size):
                    byte = file_read.read(1)
                    code = bin(int.from_bytes(byte, byteorder="big"))
                    if i == file_size - 1:
                        current_code_str += code[2::].rjust(8, "0")[:last_bits_cnt:]
                    else:
                        current_code_str += code[2::].rjust(8, "0")
                    j = 0
                    while j < len(current_code_str):
                        code = current_code_str[:j:]
                        if code in huffmanReverseCodes:
                            file_write.write(huffmanReverseCodes[code])
                            current_code_str = current_code_str[j::]
                            j = 0
                        j += 1
                file_write.write(huffmanReverseCodes[current_code_str])

    def getFrequency(self, file_read) -> dict[bytes, int]:
        frequency: dict[bytes, int] = {}

        while True:
            byte = file_read.read(self.sequence_len)
            if not byte:
                break

            if byte not in frequency:
                frequency[byte] = 0
            frequency[byte] += 1

        return frequency

    @staticmethod
    def getHuffmanTree(frequency: dict[bytes, int]) -> Node:
        q = PriorityQueue()
        for char in frequency.keys():
            node = Node(char, frequency[char])
            q.put(node)

        while q.qsize() > 1:
            node1 = q.get()
            node2 = q.get()
            node = Node(node1.char + node2.char, node1.freq + node2.freq)
            node.left = node1
            node.right = node2

            q.put(node)

        node = q.get()

        return node

    def getHuffmanCodes(self, node: Node, code: str):
        if node is None:
            return

        if (node.left is None) and (node.right is None):
            self.huffmanCodes[node.char] = code

        self.getHuffmanCodes(node.left, code + "0")
        self.getHuffmanCodes(node.right, code + "1")


if __name__ == "__main__":
    haffmancoding = HuffmanCoding()

    test_data_path = "../../files/enwik7.txt"
    # test_data_path = "HC/original_text.txt"
    compressed_path = "HC/compressed_text.txt"
    decompressed_path = "HC/decompressed_text.txt"

    haffmancoding.encode(test_data_path, compressed_path)
    haffmancoding.decode(compressed_path, decompressed_path)

    with open(test_data_path, "rb") as file_read:
        original_data = file_read.read()

    with open(decompressed_path, "rb") as file_read:
        decode_data = file_read.read()

    print(original_data == decode_data)
