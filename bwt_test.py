# def bwt_algorithm(data) -> (str, int):
#     bwt_matrix = [data[i:] + data[:i] for i in range(len(data))]
#     bwt_matrix.sort()
#     last_letters_string = "".join([string[-1] for string in bwt_matrix])
#     i = bwt_matrix.index(data)
#
#     return last_letters_string, i
#
#
# def bwt(file_path_read, file_path_write, N):
#     with open(file_path_read, "r", encoding="utf-8") as file_read:
#         with open(file_path_write, "w", encoding="utf-8") as file_write:
#             isEof: bool = False
#             while not isEof:
#                 temp: str = file_read.read(N)
#                 if len(temp) == 0:
#                     isEof = True
#                 else:
#                     bwt_resalt, i = bwt_algorithm(temp)
#                     file_write.write(bwt_resalt)
#                     file_write.write('\n')
#                     file_write.write(str(i))
#                     file_write.write('\n')


def get_suffix_array(data: str) -> (list[int], int):
    suffix = [(i, data[i:]) for i in range(len(data))]
    suffix.sort(key=lambda x: x[1])
    ind = suffix.index((0, data))
    suffix_array = [i for i, _ in suffix]

    return suffix_array, ind


def bwt(file_path_read, file_path_write, N):
    with open(file_path_read, "r", encoding="utf-8") as file_read:
        with open(file_path_write, "w", encoding="utf-8") as file_write:
            isEof: bool = False
            while not isEof:
                data: str = file_read.read(N)
                if len(data) == 0:
                    isEof = True
                else:
                    suffix_array, ind = get_suffix_array(data)
                    for i in range(len(suffix_array)):
                        j = suffix_array[i] - 1
                        if j < 0:
                            j += len(suffix_array)
                        file_write.write(data[j])
                    file_write.write('\n')
                    file_write.write(str(ind))
                    file_write.write('\n')


# def bwt_reconversion_algorithm(conversion_letter_list, ind) -> str:
#     len_data: int = len(conversion_letter_list)
#
#     permutations: list = [None] * len_data
#     bwt_matrix = [""] * len_data
#
#     sorted_cll = sorted(conversion_letter_list, key=lambda x: x[0])
#     for i, letter_element in enumerate(sorted_cll):
#         permutations[letter_element[1]] = i
#         bwt_matrix[i] = sorted_cll[i][0] + bwt_matrix[i]
#
#     for j in range(len_data - 1):
#         for i in range(len_data):
#             bwt_matrix[i] = conversion_letter_list[i][0] + bwt_matrix[i]
#
#         bwt_matrix_new = [""] * len_data
#         for i, new_index in enumerate(permutations):
#             bwt_matrix_new[new_index] = bwt_matrix[i]
#         bwt_matrix = bwt_matrix_new.copy()
#
#     return bwt_matrix[ind]

def bwt_reconversion_algorithm(data, ind) -> str:
    shifts = [(data[i], i) for i in range(len(data))]
    shifts.sort()
    new_indexes = list(zip(*shifts))[1]
    original_data = ""
    index = ind
    for _ in range(len(data)):
        index = new_indexes[index]
        original_data += data[index]
    return original_data


def bwt_reconversion(file_path_read, file_path_write, N):
    with open(file_path_read, "r", encoding="utf-8") as file_read:
        with open(file_path_write, "w", encoding="utf-8") as file_write:
            data = file_read.readlines()
            for i in range(0, len(data) - 1, 2):
                ind = int(data[i + 1])
                file_write.write(bwt_reconversion_algorithm(data[i][:-1:], ind))


def max_equal_chain(file_path_read):
    max_cnt = 0
    with open(file_path_read, "r", encoding="utf-8") as file_read:
        data = file_read.readlines()
        for i in range(0, len(data)):
            cnt = 0
            for j in range(0, len(data[i]) - 1):
                if data[i][j] == data[i][j + 1]:
                    cnt += 1
                else:
                    max_cnt = max(max_cnt, cnt)
                    cnt = 0
            max_cnt = max(max_cnt, cnt)

    print(max_cnt)


PATH: str = "files/BWT/"
FILE_ORIGINAL_NAME: str = "original_text.txt"
FILE_BWT_NAME: str = "bwt_text.txt"
FILE_BWT_RECONVERSION_NAME: str = "bwt_text.txt_reconversion.txt"
N: int = 1000

if __name__ == "__main__":
    bwt(PATH + FILE_ORIGINAL_NAME, PATH + FILE_BWT_NAME, N)
    # max_equal_chain(PATH + FILE_BWT_NAME)
    bwt_reconversion(PATH + FILE_BWT_NAME, PATH + FILE_BWT_RECONVERSION_NAME, N)

    with open(PATH + FILE_ORIGINAL_NAME, "r", encoding="utf8") as file_reader:
        orig_data = file_reader.read()

    with open("files/BWT/decompressed_text.txt", "r", encoding="utf8") as file_reader:
        decode_data = file_reader.read()

    print(orig_data == decode_data)
