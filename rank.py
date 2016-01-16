# Python interface to rank.c

import os
import sys
import numpy as np
from subprocess import Popen, PIPE

def binary_rank(m):
    m = np.array(m)
    r,c = m.shape
    if r > c: m = m.T
    r,c = m.shape

    message = "%d %d\n" % (r,c)
    for j in range(r):
        for k in range(c):
            message += "%d " % int(m[j,k])
#    print message

    p = Popen(["./rank"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate(message)
#    print stdout
    if "ERROR" in stdout:
        print passage
        print stdout
        assert False
    return int(stdout)
