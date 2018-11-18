'''
quick_sigma_detect using numpy

After testing this isn't as quick as I thought it would be. Must find out why
perhsp it's because comparing against min max? and making lists?
'''

import numpy as np


def test_quick_sigma_detect_anywhere(future=None, maximums=None, minimums=None):
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
    future = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1] if future is None else future
    # computed before hand for 2 sigma
    maximums = [5, 4, 4, 4, 3, 2]   if maximums is None else maximums
    # computed before hand for 2 sigma, or 3 or whatever.
    minimums = [3, 3, 2, 1, 0, -1]   if minimums is None else minimums
    limit = len(maximums)
    max_sum = []
    min_sum = []
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
            max_sum.append(np.sum(max_triggers.clip(min=0)))
            min_sum.append(np.sum(min_triggers.clip(min=0)))

    print('h', history)
    print('c', counts)
    print('max', max_sum)  # this is what matters, if this reaches a threshold, do the thing.
    print('min', min_sum)  # this is what matters, if this reaches a threshold, do the thing.
    return min_sum, max_sum

import numpy as np
def densest(array, size):
    density = np.convolve(array, np.ones([size]), mode='valid')
    return np.argmax(density)

example = np.array([0,0,0,1,1,1,1,1,1,1,0,1,1,1,1,0,0,0,1,0,0,1,1,0,1,0,0,0,0,0,1,0])

print( densest(example, 10) )

def get_normal_sigma(total_length, desired_sigma):
    sigma = math.sqrt(total_length*(.5)*(.5))
    return (total_length/2)-(sigma/2), (total_length/2)+(sigma/2)



if __name__=="__main__":
    test_quick_sigma_detect_anywhere()
