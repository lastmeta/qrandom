#from qrandom import qrandom
#qgen = qrandom.build_generator(5)
#qrandom.generate(qgen)

# get two examples streams
from qrandom.lib.TrueRNG import TrueRNG
gen = TrueRNG(12500)
streama = gen.generate(return_type='array')
streamb = gen.generate(return_type='array')
print(streama)
print(streamb)
print()

# precompute the min and max thresholds for two sigma
from qrandom.lib import two_sigma
two_sigmas_max = []
two_sigmas_min = []
for i in range(int(len(streama)/2)):
    mn, mx = two_sigma.get_2_sigma_ranges(i)
    two_sigmas_max.insert(0, mx)  # two_sigmas_max.append(mx)
    two_sigmas_min.insert(0, mn)  # two_sigmas_min.append(mn)
print(two_sigmas_max)
print(two_sigmas_min)
print()

# pass to proof of concept to see if it can detect 2 sigmas
from qrandom.lib import quicksigma
import numpy as np
min_sum, max_sum = quicksigma.test_quick_sigma_detect_anywhere(
    future=streama,
    maximums=two_sigmas_max,
    minimums=two_sigmas_min,
)
print('max',np.sum(max_sum), 'min', np.sum(min_sum))
min_sum, max_sum = quicksigma.test_quick_sigma_detect_anywhere(
    future=streamb,
    maximums=two_sigmas_max,
    minimums=two_sigmas_min,
)
print('max',np.sum(max_sum), 'min', np.sum(min_sum))
print()
