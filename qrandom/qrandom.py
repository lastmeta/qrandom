import time
import sys

from .lib.TrueRNG import TrueRNG
from .lib.two_sigma import get_2_sigma_score
from .lib.bayesian import bayesian_score


def build_generator(blocksize=1):
    random_number_generator = TrueRNG(blocksize=blocksize, numloops=1)
    return random_number_generator


def generate_and_count(random_number_generator):
    random_string = ''.join(random_number_generator.generate())
    bit_count = len(random_string)
    one_count = sum([int(s) for s in random_string])
    return random_string, bit_count, one_count


def run_for_seconds(random_number_generator, seconds, verbose=False):
    total_count = 0
    total_ones = 0
    start = time.time()
    finish = time.time()
    while abs(start - finish) < seconds:
        random_string, bit_count, one_count = generate_and_count(random_number_generator)
        total_count += bit_count
        total_ones += one_count
        if verbose:
            print(random_string, end='', file=sys.stdout)
        finish = time.time()
    print()
    return total_count, total_ones


def get_two_sigma_scoring(bit_count, ones_count):
    return get_2_sigma_score(bit_count, ones_count)


def deduce_zero_or_one(random_number_generator):
    one_count = 0
    bit_count = 0
    while (bit_count / 2) == one_count or bit_count == 0:
        _, bit_count, one_count = generate_and_count(random_number_generator)
    return 0 if bit_count / 2 > one_count else 1
