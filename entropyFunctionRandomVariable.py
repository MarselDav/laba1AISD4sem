import math


def entropyFunction(probabilities: list[float]) -> float:
    entropy: float = 0

    for p in probabilities:
        entropy += p * math.log2(p)

    return entropy
