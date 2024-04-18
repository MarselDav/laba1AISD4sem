# # import time
# #
# # test_data_path = "files/enwik7.txt"
# # cnt = 100
# #
# # with open(test_data_path, "rb") as file_reader:
# #     orig_data = file_reader.read()
# #
# #     result = 0
# #     for i in range(cnt):
# #         start_time = time.time_ns()
# #         for j in range(len(orig_data)):
# #             pass
# #         end_time = time.time_ns()
# #         result += (end_time - start_time)
# #     result /= cnt
# #     print(result)
# #
# # result = 0
# # for i in range(cnt):
# #     start_time = time.time_ns()
# #     with open(test_data_path, "rb") as file_reader:
# #         byte = file_reader.read(1)
# #         if not byte:
# #             break
# #     end_time = time.time_ns()
# #     result += (end_time - start_time)
# # result /= cnt
# # print(result)
#
# class RangeEncoder:
#     def __init__(self, output_stream):
#         self.low = 0
#         self.high = 2**32 - 1  # Максимальное значение для 32-битного числа
#         self.range = self.high - self.low + 1
#         self.output_stream = output_stream
#         self.buffer = 0
#         self.bits_to_follow = 0
#
#     def encode_symbol(self, symbol, symbol_range):
#         self.range //= symbol_range
#         self.low += symbol * self.range
#         self.high = self.low + self.range - 1
#
#         while True:
#             if self.high < 0x80000000:
#                 self.output_bit(0)
#                 self.output_bit_sequence(1)
#             elif self.low >= 0x80000000:
#                 self.output_bit(1)
#                 self.output_bit_sequence(0)
#                 self.low -= 0x80000000
#                 self.high -= 0x80000000
#             elif self.low >= 0x40000000 and self.high < 0xC0000000:
#                 self.bits_to_follow += 1
#                 self.low -= 0x40000000
#                 self.high -= 0x40000000
#             else:
#                 break
#
#             self.low <<= 1
#             self.high <<= 1
#             self.high |= 1
#
#     def output_bit(self, bit):
#         self.buffer <<= 1
#         self.buffer |= bit
#         self.bits_to_follow -= 1
#         if self.bits_to_follow == 0:
#             self.output_stream.write(self.buffer)
#             self.buffer = 0
#             self.bits_to_follow = 8
#
#     def output_bit_sequence(self, bit):
#         while self.bits_to_follow > 0:
#             self.output_bit(bit)
#
#     def flush(self):
#         # Определяем размер буфера в байтах
#         buffer_size_bytes = min((self.bits_to_follow + 7) // 8, 8)  # Установка максимального размера буфера в 8 байтов
#         # Преобразование целого числа в объект типа bytes
#         byte_data = self.buffer.to_bytes(buffer_size_bytes, byteorder="big")
#         # Запись данных в выходной поток
#         self.output_stream.write(byte_data)
#
#
# # Пример использования
# if __name__ == "__main__":
#     import io
#
#     # Входные данные
#     symbols = [0, 1, 0, 2, 1, 2]
#     symbol_ranges = [3, 3, 3, 3, 3, 3]  # Возможные значения для каждого символа
#
#     # Инициализация кодера и выходного потока
#     output_stream = io.BytesIO()
#     encoder = RangeEncoder(output_stream)
#
#     # Кодирование символов
#     for symbol, symbol_range in zip(symbols, symbol_ranges):
#         encoder.encode_symbol(symbol, symbol_range)
#
#     # Завершение кодирования и выходной поток
#     encoder.flush()
#     compressed_data = output_stream.getvalue()
#     print(compressed_data)
#

a = "avc"
print(a[0:10])
