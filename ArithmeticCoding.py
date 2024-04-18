import math


def getFrequencyTable(data: str) -> dict[str, int]:
    frequency_table: dict[str, int] = {}

    for char in data:
        if char in frequency_table:
            frequency_table[char] += 1
        else:
            frequency_table[char] = 1

    return frequency_table


def getFrequencyInterval(frequency_table: dict[str, int], length: int) -> dict[str, [float, float]]:
    frequencyInterval: dict[str, [float, float]] = {}
    delta = 0

    for key in frequency_table.keys():
        ftvalue = frequency_table[key] / length
        frequencyInterval[key] = [delta, delta + ftvalue]
        delta += ftvalue

    return frequencyInterval


def arithmeticCoding(data: str, frequency_table: [str, int]) -> float:
    if not data or not frequency_table:
        raise ValueError("Empty data or frequency table provided.")

    frequencyInterval: dict[str, [float, float]] = getFrequencyInterval(frequency_table, len(data))
    lower: float = 0
    upper: float = 1

    for char in data:
        interval = frequencyInterval[char]
        lowerOld = lower
        upperOld = upper
        lower = lowerOld + interval[0] * (upperOld - lowerOld)
        upper = lowerOld + interval[1] * (upperOld - lowerOld)

    return lower


def inverseArithmeticCoding(lower: float, frequency_table: [str, int], length: int) -> str:
    frequencyInterval: dict[str, [float, float]] = getFrequencyInterval(frequency_table, length)

    code = low
    originalData = ""
    upper = 1

    for i in range(length):
        for key in frequencyInterval.keys():
            interval = frequencyInterval[key]

            if interval[0] <= code <= interval[1]:
                upper = interval[1]
                lower = interval[0]
                originalData += key
                break

        code = (code - lower) / (upper - lower)

    return originalData



if __name__ == "__main__":
    # test_string = "a" + "b" + "c" + "a" * 9 + "c" * 14 + "d" * 7
    test_string = "abc"
    frequencyTable: [str, int] = getFrequencyTable(test_string)
    low = arithmeticCoding(test_string, frequencyTable)
    print(low)
    print(inverseArithmeticCoding(low, frequencyTable, len(test_string)))

    str_low = str(low).split(".")[1]
    bytes = math.log(int(str_low), 256)
    print(f"было: {len(test_string)}, стало: {bytes}")
