# Get N random numbers /w function Y=x^2, where x is in [-2;2] range
from random import random


def get_random_sequence(count: int):
    if count < 1:
        raise Exception('Count of the random elements should be at least one')

    sequence = []

    for _ in range(count):
        number = random()
        x = number * 4 - 2

        sequence.append(x**2)

    return sequence
