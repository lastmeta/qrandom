''' notes on detecting correlation
when they're zero they're moving togethers.
so we could take the inverse around the axis 0 of one and get the areas that are
on average zero or close to zero, if it's close to zero more often than it should
then we've detected a correlation...
'''
>>> import numpy as np
>>> a = [1,2,3,4,5,6,5,6,5,4,3,2,3,2,3,4,5,4,3,2,1]
>>> b = [1,2,1,2,1,2,3,4,3,2,1,0,1,2,3,4,5,6,7,6,7]
>>> np.array(a) - np.array(b)
array([ 0,  0,  2,  2,  4,  4,  2,  2,  2,  2,  2,  2,  2,  0,  0,  0,  0, -2, -4, -4, -6])
>>> np.array(b) - np.array(a) # not the inverse, just the reverse
array([ 0,  0, -2, -2, -4, -4, -2, -2, -2, -2, -2, -2, -2,  0,  0,  0,  0,  2,  4,  4,  6])
