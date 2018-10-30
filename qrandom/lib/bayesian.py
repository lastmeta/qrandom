import numpy as np
import scipy.stats

#https://www.thomasjpfan.com/2015/09/bayesian-coin-flips/
def bayesian_score(heads, tails, alpha=2, beta=2):
    x = np.linspace(0, 1, 1000)
    y = scipy.stats.beta.pdf(x, heads+alpha, tails+beta)
    max_value = max(y)
    max_index = y.argmax(axis=0)
    return max_index, max_value


#print(bayesian_score(60, 40, 2, 2)[1])
#print(bayesian_score(12, 4, 2, 2)[1])
