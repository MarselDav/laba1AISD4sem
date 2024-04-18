def getAverageSequenceLen(data: str) -> float:
    generalLen: int = 0
    cnt: int = 0

    different_counter = 1
    repeat_counter = 1

    data_len = len(data)

    for i in range(1, data_len):
        if data[i] == data[i - 1]:
            if different_counter > 1:
                if (different_counter - 1) >= 2:
                    generalLen += different_counter - 1
                    cnt += 1
                different_counter = 1
            repeat_counter += 1
        else:
            if repeat_counter > 1:
                if repeat_counter >= 2:
                    generalLen += repeat_counter
                    cnt += 1
                repeat_counter = 1
            else:
                different_counter += 1

    if different_counter > 1:
        generalLen += different_counter
        cnt += 1

    if repeat_counter >= 2:
        generalLen += repeat_counter
        cnt += 1

    # print(generalLen)
    # print(cnt)
    return (generalLen - 2 * cnt) / data_len


if __name__ == "__main__":
    test = "рдакрааааббa"
    print(getAverageSequenceLen(test))
