from data import *

import numpy as np
import matplotlib.pyplot as plt
import math



plt.rc('text', usetex=True)
plt.rc('font', family='serif')

def log2(x):
    if x <= 0: return float('-inf')
    return math.log(x)/math.log(2)


def lse2(x,y):
    if x < y: return lse2(y,x)
    return x + log2(1 + 2**(y - x))




X = [26, 20, 38, 49, 49, 49, 49, 43, 32, 43, 32, 26, 38, 20, 43, 43]
logZ = reduce(lse2,[ -x for x in X ])
L = min(X)
def log_zq(d):
    return reduce(lse2,[ -d for x in X if x > d ] + [ -x for x in X if x<=d ])
def log_embeddingSize(d):
    return reduce(lse2,[ 0 for x in X if x > d ] + [ (d-x) for x in X if x<=d ])
def acceptQ(d):
    return 2**(logZ - log_zq(d))
def C(d,k):
    return 1.0 / (1 + 2**(k - log_embeddingSize(d)))
def tt(d,k):
    p = p_fail(d,k)
    if p < 1:
        survivors = 2**(reduce(lse2,[ min(0,(-k + d - min(x,d))) for x in X ]))
        return (1 + survivors)/(1 - p)
    else:
        return len(X)
def p_fail(d,k):
    p = 1 + 2**(k - log_embeddingSize(d)) - C(d,k) * acceptQ(d)
    if p < 1 and p > 0: return p
    return 1
def kl(d,k):
    c = C(d,k)
    if log2(c + (1 - c)/acceptQ(d)) - log2(c) <= 0:
        print d, k, c, acceptQ(d)
        assert False
    return log2(c + (1 - c)/acceptQ(d)) - log2(c)

MAXK = 20
MAXTILT = 20

d_ = np.array([[d for k in range(0,MAXK) ] for d in range(L,L+MAXTILT) ])
k_ = np.array([[k for k in range(0,MAXK) ] for d in range(L,L+MAXTILT) ])

time = np.array([[tt(d,k) for k in range(0,MAXK) ] for d in range(L,L+MAXTILT) ])
time[time > len(X)] = len(X)



print plt.matshow(time, cmap=plt.cm.gray)
plt.xlabel(r'$K$ = (\# random projections)')
ax = plt.gca()
ax.xaxis.set_ticks_position('bottom')
plt.ylabel(r'$d-|x_*|$ = $\log_2 ($ Tilt of $q(x))$')
#plt.title('Expected solver invocations')
plt.colorbar()

accuracy = np.array([[np.log(kl(d,k)) for k in range(0,MAXK) ] for d in range(L,L+MAXTILT) ])
#accuracy[accuracy > 0] = 0

CS = plt.contour(accuracy)
plt.clabel(CS, inline=1, fontsize=8)


plt.show()
assert False



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
