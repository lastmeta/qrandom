'''
quick_sigma_detect using numpy

given a window size and an array quick sigma can give you the densest (most 1s)
area of that array (the first most dense area)

given an array length (number of observations) and the desired sigma, quicksigma
can give you the lower and upper bound, considering a prior of 50% (fair coin).
'''
import math

import typing as t
import numpy as np
from scipy import signal


def densest(observations: np.array, window_size: int) -> t.Tuple[int, np.array]:
    density = signal.convolve(observations, np.ones([window_size]), mode='valid')
    index = np.argmax(density)
    densest_sub_array = observations[index:index + window_size]
    return index, densest_sub_array


def get_normal_sigma(observation_count: int, desired_sigma: float = 2.0) -> t.Tuple[float, float]:
    sigma = math.sqrt(observation_count*(.5)*(.5)) * desired_sigma
    upper_bound = (observation_count/2)+(sigma/2)
    lower_bound = (observation_count/2)-(sigma/2)
    return lower_bound, upper_bound
