import time
import random
import re
import sys

from pycryptosat import Solver

s = Solver(threads = 3)

tt = 0

hs = [] # holes
clauses = []
with open(sys.argv[1],'r') as f:
    for l in f:
        if len(l) > len('c hole ') and l[:len('c hole ')] == 'c hole ':
            ms = re.findall(r'(\d+) \- (\d+)', l)[0]
            ms = range(int(ms[0]),int(ms[1])+1)
            hs = hs + ms
        elif len(l) > 0 and not 'c' in l and not 'p' in l:
            vs = re.findall(r'(\-?\d+)',l)
            assert vs[-1] == '0'
            clause = [int(v) for v in vs[:-1] ]
            clauses.append(clause)
            s.add_clause(clause)
print "Loaded",len(clauses),"clauses with",len(hs),"holes"
subspace_dimension = int(sys.argv[2])

def random_projection():
    s.add_xor_clause([v for v in hs if random.random() > 0.5 ],random.random() > 0.5)

def try_solving():
    global tt
    print "About to run solver ==  ==  ==  > "
    start_time = time.time()
    result = s.solve()
    dt = (time.time() - start_time)
    tt += dt
    print "Ran solver in time",dt
    if result[0]:
        bindings = {}
        for v in range(len(result[1])):
            if v in hs:
                bindings[v] = result[1][v]
        print "Satisfiable."
        return bindings
    else:
        print "Unsatisfiable."
        return False


def try_sampling():
    for j in range(subspace_dimension):
        random_projection()
    result = try_solving()
    if result:
        print "Random projection satisfied"
        print result
        s.add_clause([ (-1 if result[h] else 1)*h for h in result ])
        if try_solving():
            print "Sample rejected"
        else:
            print "Unique so sample accepted"

def adaptive_sample():
    global subspace_dimension
    result = try_solving()
    if result:
        print "Formula satisfied"
        for j in range(subspace_dimension):
            random_projection()
        while try_solving():
            print "Satisfied %d constraints" % subspace_dimension
            random_projection()
            subspace_dimension += 1
        print "Rejected %d projections" % subspace_dimension

        
            
#try_sampling()
adaptive_sample()

print "total time =",tt
