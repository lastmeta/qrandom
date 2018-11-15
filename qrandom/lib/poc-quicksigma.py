'''
quick_sigma_detect using numpy
'''

import numpy as np


def test_quick_sigma_detect_anywhere():
    ''' test the concept '''
    counts = np.array([])
    history = np.array([])

    # get from the device, while this is computing, get some more to add to future
    # find the right balance. so that we're not getting one at a time, but we're
    # also not waiting 2 seconds and doing no calculations, waiting for the next batch.
    # getting random bits and doing calculations should both be done in parrallel with
    # the actor model, and the message queue should remain nearly empty, if it gets
    # to be over a certian threshold, get bigger chuncks, if it's under a threshold,
    # get smaller chucks, faster chunks. 
    future = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]


    maximums = [5, 4, 4, 4, 3, 2]  # computed before hand for 2 sigma
    minimums = [3, 3, 2, 1, 0, -1]  # computed before hand for 2 sigma, or 3 or whatever.
    limit = len(maximums)
    for enum, i in enumerate(future):
        counts += i
        counts = np.append(counts, i)
        history = np.append(history, i)
        if enum >= limit:
            # reindex to keep same size
            counts = counts[1:]
            history = history[1:]

            # calculate sigma occurance
            max_triggers = counts - maximums
            min_triggers = minimums - counts
            print('max', np.sum(max_triggers.clip(min=0)))  # this is what matters, if this reaches a threshold, do the thing.
            print('min', np.sum(min_triggers.clip(min=0)))  # this is what matters, if this reaches a threshold, do the thing.

    print('h', history)
    print('c', counts)

test_quick_sigma_detect_anywhere()
