import math

import numpy as np


def output_bit_plus_pending(bit_list, bit, pending_bits):
    bit_list.append(bit)
    while pending_bits:
        bit_list.append(not bit)
        pending_bits -= 1
    return pending_bits


def get_Probability(data):
    frequency = {}
    n = len(data)

    for char in data:
        if char not in frequency:
            frequency[char] = 0
        frequency[char] += 1

    return {i: round((frequency[i] / n) * 2 ** 16) for i in frequency}


def encode(data):
    P = get_Probability(data)
    P_intervals = {}
    current = 0
    for char in P:
        P_intervals[char] = (current, current + P[char])
        current += P[char]
    P_denominator = 2 ** 16
    bit_list = []

    R = np.uint32(0xFFFFFFFF)
    L = np.uint32(0)
    pending_bits = 0
    for char in data:
        distance = np.uint32(R - L)
        R = np.uint32(L + np.uint32(distance >> 16) * P_intervals[char][1])
        L = np.uint32(L + np.uint32(distance >> 16) * P_intervals[char][0])

        while True:
            if R < 0x80000000:
                pending_bits = output_bit_plus_pending(bit_list, 0, pending_bits)
                L = np.uint32(L << 1)
                R = np.uint32(R << 1)
                R = np.uint32(R | 1)
            elif L >= 0x80000000:
                pending_bits = output_bit_plus_pending(bit_list, 1, pending_bits)
                L = np.uint32(L << 1)
                R = np.uint32(R << 1)
                R = np.uint32(R | 1)
            elif L >= 0x40000000 and R < 0xC0000000:
                pending_bits += 1
                L = np.uint32(L << 1)
                L = np.uint32(L & 0x7FFFFFFF)
                R = np.uint32(R << 1)
                R = np.uint32(R | 0x80000001)
            else:
                break

    pending_bits += 1

    if pending_bits:
        if L < 0x40000000:
            pending_bits = output_bit_plus_pending(bit_list, 0, pending_bits)
        else:
            pending_bits = output_bit_plus_pending(bit_list, 1, pending_bits)
    return bit_list


# def decode(bit_list, original_length):
#     P = get_Probability(data)
#     P_intervals = {}
#     current = 0
#     for char in P:
#         P_intervals[char] = (current, current + P[char])
#         current += P[char]
#     P_denominator = 2 ** 16
#
#     result = []
#     R = np.uint32(0xFFFFFFFF)
#     L = np.uint32(0)
#     value = 0
#     for i in range(32):
#         value = np.uint32(value << 1)
#         value = np.uint32(value | (bit_list[i] if i < len(bit_list) else 0))
#
#     for _ in range(original_length):
#         distance = np.uint32(R - L)
#         target = np.uint32((value - L + 1) * P_denominator - 1) // distance
#         char = None
#         for c in P_intervals:
#             if P_intervals[c][0] <= target < P_intervals[c][1]:
#                 char = c
#                 break
#
#         result.append(char)
#         R = np.uint32(L + np.uint32(distance >> 16) * P_intervals[char][1])
#         L = np.uint32(L + np.uint32(distance >> 16) * P_intervals[char][0])
#
#         while True:
#             if L >= 0x80000000 or R < 0x80000000:
#                 L = np.uint32(L << 1)
#                 R = np.uint32(R << 1)
#                 R = np.uint32(R | 1)
#
#                 value = np.uint32(value << 1)
#                 value = np.uint32(value | (bit_list[i] if i < len(bit_list) else 0))
#             elif L >= 0x40000000 and R < 0xC0000000:
#                 L = np.uint32(L << 1)
#                 L = np.uint32(L & 0x7FFFFFFF)
#                 R = np.uint32(R << 1)
#                 R = np.uint32(R | 0x80000001)
#                 value = np.uint32(value - 0x4000000)
#
#                 value = np.uint32(value << 1)
#                 value = np.uint32(value | (bit_list[i] if i < len(bit_list) else 0))
#             else:
#                 break
#
#             L = np.uint32(L << 1)
#             R = np.uint32(R << 1)
#             value = np.uint32(value << 1)
#             value = np.uint32(value | (bit_list[i] if i < len(bit_list) else 0))
#             i += 1
#
#     return result
#
#
def getFreq(data):
    frequency = {}
    n = len(data)

    for char in data:
        if char not in frequency:
            frequency[char] = 0
        frequency[char] += 1
    return frequency


def decode1(bit_stream_lst, alph_freq_lst: list, len_str: int) -> str:
    # bit_stream_lst  = []
    # for symbol_ind in range(len(bytes)):
    #     symbol = bytes[symbol_ind]
    #     bit_symbol = bin(symbol)[2:].zfill(8)
    #     for k in range(0,8):
    #         bit_stream_lst.append(bit_symbol[k])
    bit_stream_str = "".join(bit_stream_lst)

    alphabet_list = []
    cum_sum = 0
    cum_list = [0]
    TOTAL_CUM = 0  # !total cumulitive frequency

    for i in range(len(alph_freq_lst)):
        cum_sum += alph_freq_lst[i][1]

        alphabet_list.append(alph_freq_lst[i][0])
        TOTAL_CUM += alph_freq_lst[i][1]
        cum_list.append(cum_sum)

    alph_indexes = [i for i in range(len(alph_freq_lst))]
    alphabet_dict = dict(zip(alphabet_list, alph_indexes))

    max_len = math.log2(TOTAL_CUM)
    if max_len.is_integer():
        max_len += 1
    bitlen = math.ceil(max_len)
    max_len = 2 ** bitlen

    alh_reverse_dict = {value: key for key, value in alphabet_dict.items()}
    left = 0
    right = max_len - 1

    decoded_mgs = []

    TAG = int(bit_stream_str[:bitlen], 2)

    curr_symbol_ind = bitlen
    while curr_symbol_ind < len(bit_stream_str):

        k = 0
        val = math.floor(((TAG - left + 1) * TOTAL_CUM - 1) / (right - left + 1))
        while val >= cum_list[k]:
            k += 1

        decoded_mgs.append(alh_reverse_dict[k - 1])

        lenght = right - left + 1
        left_freq = cum_list[k - 1] / TOTAL_CUM
        righ_freq = cum_list[k] / TOTAL_CUM
        left, right = left + math.floor(lenght * left_freq), left + math.floor(lenght * righ_freq) - 1

        if len(decoded_mgs) == len_str - 1:
            break

        while left >= max_len / 2 or right <= max_len / 2 or (
                max_len / 4 <= left < max_len / 2 < right <= 3 * max_len / 4):

            if left >= max_len / 2 or right <= max_len / 2:
                left = int(bin(left)[2:].zfill(bitlen)[1:] + '0', 2)  # ? shift left by 1; LSB = 0
                right = int(bin(right)[2:].zfill(bitlen)[1:] + '1', 2)  # ? shift left by 1; LSB = 1
                TAG = int(bin(TAG)[2:].zfill(bitlen)[1:] + bit_stream_str[curr_symbol_ind], 2)

                binary = bin(TAG)[2:].zfill(bitlen)[1:]
                curr_symbol_ind += 1

            if max_len / 4 <= left < max_len / 2 < right <= 3 * max_len / 4:
                binary = bin(left)[2:].zfill(bitlen)[1:]
                left = int(str(int(not int(binary[0]))) + binary[1:] + '0',
                           2)  # ? shift left by 1; inverse MSB; LSB = 0
                binary = bin(right)[2:].zfill(bitlen)[1:]
                right = int(str(int(not int(binary[0]))) + binary[1:] + '1',
                            2)  # ? shift left by 1; inverse MSB; LSB = 1

                binary = bin(TAG)[2:].zfill(bitlen)[1:]

                TAG = int(str(int(not int(binary[0]))) + binary[1:] + bit_stream_str[curr_symbol_ind], 2)

                curr_symbol_ind += 1

    return "".join(decoded_mgs)

m_frozen = False
cumulative_frequency = [0] * 258

def reset():
    for i in range(258):
        cumulative_frequency[i] = i
    m_bytesProcessed = 0
    m_frozen = False


def update(c):
    for i in range(c + 1, 258):
        cumulative_frequency[i] += 1
    if cumulative_frequency[257] >= 257:  # MAX_FREQ
        m_frozen = True


def getProbability(c):
    p = [cumulative_frequency[c], cumulative_frequency[c + 1], cumulative_frequency[257]]
    if not m_frozen:
        update(c)
    return p


def getChar(scaled_value):
    for i in range(257):
        if scaled_value < cumulative_frequency[i + 1]:
            c = i
            p = [cumulative_frequency[i], cumulative_frequency[i + 1], cumulative_frequency[257]]
            if not m_frozen:
                update(c)
            return p, c


def getCount():
    return cumulative_frequency[257]


def decode(bit_list, data):
    P = get_Probability(data)
    P_intervals = {}
    current = 0
    for char in P:
        P_intervals[char] = (current, current + P[char])
        current += P[char]
    P_denominator = 2 ** 16

    current_bit_cnt = 0
    original_data = ""

    R = np.uint32(0xFFFFFFFF)
    L = np.uint32(0)
    value = np.uint32(0)
    for i in range(min(32, len(bit_list))):
        value = np.uint32(value << 1)
        value = np.uint32(value + bit_list[current_bit_cnt])
        current_bit_cnt += 1

    while True:
        distance = np.uint32(R - L)

        count = ((value - L + 1) * getCount() - 1) / distance
        p, c = getChar(count)

        if c == 256:
            break
        original_data += chr(c)

        R = L + (distance * p[1]) / p[2] - 1
        L = L + (distance * p[0]) / p[2]

        while True:
            if L >= 0x80000000 or R < 0x80000000:
                L = np.uint32(L << 1)
                R = np.uint32(R << 1)
                R = np.uint32(R | 1)

                value = np.uint32(value << 1)
                value = np.uint32(value + bit_list[current_bit_cnt])
                current_bit_cnt += 1
            elif L >= 0x40000000 and R < 0xC0000000:
                L = np.uint32(L << 1)
                L = np.uint32(L & 0x7FFFFFFF)
                R = np.uint32(R << 1)
                R = np.uint32(R | 0x80000001)
                value = np.uint32(value - 0x4000000)

                value = np.uint32(value << 1)
                value = np.uint32(value + bit_list[current_bit_cnt])
                current_bit_cnt += 1
            else:
                break

    return original_data


data = "abc"
# data = """'''Anarchism''' originated as a term of abuse first used against early [[working class]] [[radical]]s including the [[Diggers]] of the [[English Revolution]] and the [[sans-culotte|''sans-culottes'']] of the [[French Revolution]].[http://uk.encarta.msn.com/encyclopedia_761568770/Anarchism.html] Whilst the term is still used in a pejorative way to describe ''&quot;any act that used violent means to destroy the organization of society&quot;''&lt;ref&gt;[http://www.cas.sc.edu/socy/faculty/deflem/zhistorintpolency.html History of International Police Cooperation], from the final protocols of the &quot;International Conference of Rome for the Social Defense Against Anarchists&quot;, 1898&lt;/ref&gt;, it has also been taken up as a positive label by self-defined anarchists."""

# test_data_path = "files/enwik7.txt"
# test_data_path = "files/RLE/original_text.txt"
# with open(test_data_path, "r", encoding="utf8") as file_reader:
#     data = file_reader.read()
#     data = data + chr(256)

result = encode(data)
P = getFreq(data)
P = [(i, P[i]) for i in P]
orig_data = decode1([str(i) for i in result], P, 4)
# orig_data = decode(result, data)
print(orig_data)
