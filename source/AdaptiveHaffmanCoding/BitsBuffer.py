class BitsBuffer:
    def __init__(self):
        self.bits = []

    def extract_byte(self, byte_cnt):
        if self.isReady():
            byte_bits = self.bits[:byte_cnt]  # Извлекаем первые 8 битов
            del self.bits[:byte_cnt]  # Удаляем извлеченные биты из буфера
            byte_sequence = int(''.join(map(str, byte_bits)), 2)  # Преобразуем биты в целое число
            return byte_sequence.to_bytes(byte_cnt // 8, byteorder="big")  # Возвращаем байт
        else:
            raise ValueError("Недостаточно битов в буфере для формирования байта")

    def writeAppend(self, bit_string, file_write):
        for bit in bit_string:
            self.append(int(bit))

        while self.isReady():
            file_write.write(self.extract_byte(8))

    def writeRemainingBits(self, file_write):
        while len(self.bits) < 8:
            self.bits.append(0)

        while self.isReady():
            file_write.write(self.extract_byte(8))

    def bits(self):
        return self.bits

    def isReady(self) -> bool:
        return len(self.bits) >= 8

    def append(self, bit):
        self.bits.append(bit)
