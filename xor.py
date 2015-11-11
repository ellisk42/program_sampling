import subprocess
import sys
import random #from random import randint
import os
import re

SKETCHOPTIONS = ' --bnd-inline-amnt 4 '

source = None
with open(sys.argv[1]) as h:
    source = h.read()

n = int(sys.argv[2]) # bits

if len(sys.argv) > 3:
    k = int(sys.argv[3]) # clauses
    adaptive = False
else:
    k = n
    adaptive = True

control_bits = [ 'tape[%d]' % j for j in range(n) ]

def random_constraint():
    v = ['false']
    for c in control_bits:
        if random.random() > 0.5:
            v.append(c)
    constraint = '^'.join(v)
    if random.random() > 0.5:
        constraint = '!(%s)'%constraint
    return constraint

def random_projection():
    p = []
    for j in range(k):
        p.append(random_constraint())
    return ' && '.join(p)

def run_with_suffix(suffix,temporary):
    with open(temporary,'w')  as h:
        h.write(source + suffix)
    try:
        return subprocess.check_output(['sketch %s %s'%(SKETCHOPTIONS, temporary)],
                                       stderr = subprocess.STDOUT, shell = True)
    except subprocess.CalledProcessError as e:
        return e.output


samples = 0
attempts = 0
while samples < 1 and attempts < 20:
#    attempts += 1
    print "k = ",k
    projection = "\nharness void projection() { assert %s; }" % random_projection()
    r = run_with_suffix(projection,"projection_output.sk")
    print r
#    print "output = ",r
    if '*** Rejected' in r:
        print 'Constraints rejected',r
#        k -= 1
        continue
    continue
    different = "\nharness void different() { assert %s; }" % tape_values(r)
    rd = run_with_suffix(projection + different,"different_output.sk")
    if '*** Rejected' in rd:
        print 'Got sample'
#        print r
        samples += 1
        with open('sample%d.sk'%samples,'w') as h:
            h.write(r)
    else:
        print 'duplicate,rd' #,rd
#        k += 1
