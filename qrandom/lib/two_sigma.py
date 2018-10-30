import math #alternative: sqrt = n**(1/2.0)


def get_2_sigma_size(n):
    return 2*math.sqrt(n)


def get_2_sigma_ranges(n):
    size = get_2_sigma_size(n)/2
    return n/2-size, n/2+size


def get_2_sigma_score(bit_count, one_count):
    lower, higher = get_2_sigma_ranges(bit_count)
    if one_count < lower:
        return -1, (lower, higher), one_count / lower
    elif one_count > higher:
        return 1, (lower, higher), one_count / higher
    else:
        return 0, (lower, higher), one_count / (bit_count / 2)


#print(get_2_sigma_ranges(10))
#print(get_2_sigma_ranges(16))
#print(get_2_sigma_ranges(25))
#print(get_2_sigma_ranges(50))
#print(get_2_sigma_ranges(100))
#print(get_2_sigma_ranges(10000))
#print(get_2_sigma_ranges(16384))
#print(get_2_sigma_ranges(1000000))
