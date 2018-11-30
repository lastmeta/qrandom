import numpy as np

from qrandom.lib import quicksigma as qs


def test_densest_example_small():
    example = np.array([0,0,0,1,1,1,1,1,1,1,0,1,1,1,1,0,0,0,1,0,0,1,1,0,1,0,0,0,0,0,1,0])
    index, partial_example = qs.densest(example, 10)
    ## look for larger lengths too. zero in on highest by length, that means trim zeros at least.
    low, high = qs.get_normal_sigma(len(partial_example), 2)
    ones = np.sum(partial_example)
    if ones > high or ones < low:
        print("trigger", "check other streams after to make sure triggers overlap" )
    assert index == 3
    assert list(partial_example) == [1,1,1,1,1,1,1,0,1,1,]
    assert low < 4
    assert high > 6
    assert ones == 9

def try_example_big():
    example = np.random.choice([0, 1], size=1_000_000, p=[.5, .5])
    index, partial_example = qs.densest(example, 100_000)
    #print(index, partial_example)
    ## look for larger lengths too. zero in on highest by length, that means trim zeros at least.
    high, low = qs.get_normal_sigma(len(partial_example), 2)
    #print(high, low)

    ones = np.sum(partial_example)
    #print(ones)

    if ones > high or ones < low:
        print("trigger", "check other streams after to make sure triggers overlap" )
