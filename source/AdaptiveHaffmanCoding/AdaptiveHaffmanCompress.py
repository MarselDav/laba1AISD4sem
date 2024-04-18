import numpy as np

from source.AdaptiveHaffmanCoding.BitsBuffer import BitsBuffer
from source.AdaptiveHaffmanCoding.HaffmanTree import Tree
from source.AdaptiveHaffmanCoding.ReorderingTreeMethods import ReorderingTreeMethods


class AHA_COMPRESS:
    def __init__(self):
        self.sequence_len = 2
        self.reorderingTreeMethods = ReorderingTreeMethods(self.sequence_len)
        self.tree = Tree()
        self.nodeCash = np.full(256**self.sequence_len, None, dtype=object)
        self.nodeList = [self.tree.ESCAPE_NODE()]

        self.bitsBuffer = BitsBuffer()

    def encode(self, input_path: str, output_path: str):
        with open(input_path, "rb") as file_reader:
            with open(output_path, "wb") as file_writer:
                file_writer.write(b'0')
                while True:
                    byte_sequence = file_reader.read(self.sequence_len)
                    if not byte_sequence:
                        break

                    code = self.reorderingTreeMethods.update_by_character(byte_sequence, self.nodeCash, self.tree, self.nodeList)
                    self.bitsBuffer.writeAppend(code, file_writer)
                last_bits_cnt = len(self.bitsBuffer.bits)
                self.bitsBuffer.writeRemainingBits(file_writer)
                file_writer.seek(0)
                file_writer.write(last_bits_cnt.to_bytes(1, byteorder="big"))
