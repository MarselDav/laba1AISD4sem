import numpy as np

from source.AdaptiveHaffmanCoding.BitsBuffer import BitsBuffer
from source.AdaptiveHaffmanCoding.HaffmanTree import Tree, Node
from source.AdaptiveHaffmanCoding.ReorderingTreeMethods import ReorderingTreeMethods


class AHA_DECOMPRESS:
    def __init__(self):
        self.sequence_len = 2
        self.reorderingTreeMethods = ReorderingTreeMethods(self.sequence_len)
        self.tree = Tree()
        self.nodeCash = np.full(256**self.sequence_len, None, dtype=object)
        self.nodeList = [self.tree.ESCAPE_NODE()]

        self.mode_read_encode = False
        self.bitsBuffer = BitsBuffer()
        self.currentNode = None

    def handleBit(self, bit, file_writer):
        if not self.mode_read_encode:
            self.bitsBuffer.append(bit)
            if len(self.bitsBuffer.bits) >= 8 * self.sequence_len:
                byte_sequence = self.bitsBuffer.extract_byte(8 * self.sequence_len)
                self.reorderingTreeMethods.update_by_character(byte_sequence, self.nodeCash, self.tree, self.nodeList)
                file_writer.write(byte_sequence)
                self.mode_read_encode = True
                self.currentNode = self.tree.ROOT()
        else:
            if bit == 1:
                self.currentNode = self.currentNode.right
            else:
                self.currentNode = self.currentNode.left

            if self.currentNode == self.tree.ESCAPE_NODE():
                self.mode_read_encode = False

            if self.currentNode.byte_sequence is not None:
                self.reorderingTreeMethods.update_by_character(self.currentNode.byte_sequence, self.nodeCash, self.tree,
                                                               self.nodeList)
                file_writer.write(self.currentNode.byte_sequence)
                self.currentNode = self.tree.ROOT()

    def decode(self, input_path: str, output_path: str):
        with open(input_path, 'rb') as file_reader:  # Открываем файл в режиме чтения в двоичном формате
            last_bits_cnt = int.from_bytes(file_reader.read(1), byteorder="big")
            file_reader.seek(0, 2)
            file_size = file_reader.tell() - 1
            file_reader.seek(1)

            with open(output_path, "wb") as file_writer:
                for i in range(file_size):
                    byte = file_reader.read(1)  # Читаем один байт из файла
                    code = bin(int.from_bytes(byte, byteorder="big"))
                    if i == file_size - 1:
                        byte_string = code[2::].rjust(8, "0")[:last_bits_cnt:]
                    else:
                        byte_string = code[2::].rjust(8, "0")

                    for j in range(len(byte_string)):  # Цикл для извлечения битов из байта
                        self.handleBit(int(byte_string[j]), file_writer)
