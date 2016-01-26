from data import *

import numpy as np
import matplotlib.pyplot as plt
import math


def log2(x):
    if x <= 0: return float('-inf')
    return math.log(x)/math.log(2)





# raw_data is (a-L)xKx(# records)
raw_data = np.array(sort_data)
print "data has shape", raw_data.shape

s = raw_data[0][0][1] # number of solutions = <mc> when k = 0
print "|s| = %d" % s

al = np.zeros((raw_data.shape[0],raw_data.shape[1]))
k = np.zeros((raw_data.shape[0],raw_data.shape[1]))
for k_ in range(raw_data.shape[1]):
    for a_ in range(raw_data.shape[0]):
        al[a_,k_] = a_
        k[a_,k_] = k_
        


if False:
    d = np.log(s - 1 + 2**al)/np.log(2) - k # delta
    g = al - log2(s) # \gamma
    kl = np.log ( (1 + 2**(-g)) * (1 + 2**(-d) )) / np.log(2)
    CS = plt.contour(k, al, kl)
    plt.clabel(CS, inline=1, fontsize=10)


# pull out statistics from the data
p_no_survivors = raw_data[:,:,4]
#print p_no_survivors
et = raw_data[:,:,2]
p_aq = np.reciprocal(et) + p_no_survivors # probability of accepting a sample from Q
p_aq[p_aq < 0] = 0
p_aq[p_aq > 1] = 1
mc = raw_data[:,:,1] # expected model count

embeddingSize = 2**k / p_no_survivors

kl = np.log(1 + 2**k / embeddingSize - 1/embeddingSize)/np.log(2)  - np.log(p_aq)/np.log(2) #+ 2*np.log(1 - p_no_survivors)/np.log(2)

# upper bound on the kl divergence
d = np.log(s - 1 + 2**al)/np.log(2) - k # delta
g = al - log2(s) # \gamma
kl_ub = np.log ( (1 + 2**(-g)) * (1 + 2**(-d) )) / np.log(2)



#plt.matshow(kl, cmap=plt.cm.gray)
#plt.colorbar()



#tt = [ [ x[3] for x in a ] for a in raw_data ]
tt = raw_data[:,:,3]
print tt
scale = s+1  # |S|+1, which is the baseline
tt[tt < 0] = scale
tt[tt > scale] = scale
plt.matshow(np.log(tt), cmap=plt.cm.gray)
plt.xlabel('# random projections')
plt.ylabel('alpha - |x_*|')
#plt.title('Expected solver invocations')
plt.colorbar()

CS = plt.contour(k,al,np.log(kl))
plt.clabel(CS, inline=1, fontsize=8)



plt.show()
