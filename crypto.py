import math
import os
import time
import random
import re
import sys

from pycryptosat import Solver

from decodeFlash import parse_tape

def lse(x,y):
    if x < y: return lse(y,x)
    return x + math.log(1 + math.exp(y - x))

#subspace_dimension = int(sys.argv[2])

class ProgramSolver():
    def __init__(self,filename):
        self.s = Solver(threads = 1,verbose = 0)
        self.tt = 0

        h2v = {} # hole 2 variable
                
        self.maximum_variable = -1
        with open(filename,'r') as f:
            for l in f:
                if len(l) > len('c hole ') and l[:len('c hole ')] == 'c hole ':
                    ms = re.findall(r'(\d+) \- (\d+)', l)[0]
                    assert int(ms[0]) == int(ms[1])
                    ms = int(ms[0])
                    n = int(re.findall(r'H__\S+_(\S+)\s',l)[0])
                    h2v[n] = ms
                elif len(l) > 0 and not 'c' in l and not 'p' in l:
                    vs = re.findall(r'(\-?\d+)',l)
                    assert vs[-1] == '0'
                    clause = [int(v) for v in vs[:-1] ]
                    self.maximum_variable = max([self.maximum_variable] +
                                                [abs(v) for v in clause ])
                    self.s.add_clause(clause)
        print "Loaded",filename," with",len(h2v),"holes"
        # convert the tape index into a sat variable
        self.tape2variable = [ v for h,v in sorted(h2v.items()) ]
        
        # converts a sat variable to a tape index
        self.variable2tape = dict([ (v,h) for h,v in h2v.items() ])



    def generate_variable(self):
        self.maximum_variable += 1
        return self.maximum_variable
    
    def random_projection(self):
        self.s.add_xor_clause([v for v in self.variable2tape if random.random() > 0.5 ],random.random() > 0.5)
        
    def try_solving(self,assumptions = None):
        print "About to run solver ==  ==  ==  > "
        start_time = time.time()
        if assumptions != None:
            result = self.s.solve(assumptions)
        else:
            result = self.s.solve()
        dt = (time.time() - start_time)
        self.tt += dt
        print "Ran solver in time",dt
        if result[0]:
            bindings = {}
            for v in range(len(result[1])):
                if v in self.variable2tape:
                    bindings[v] = result[1][v]
            print "Satisfiable."
            return bindings
        else:
            print "Unsatisfiable."
            return False

    def uniqueness_clause(self,tape):
        p,bit_mask = parse_tape(tape)
        clause = []
        for j in range(len(tape)):
            if bit_mask[j] == 1 or True:
                # jth tape position
                v = self.tape2variable[j]
                if tape[j] == 1: v = -v
                clause += [v]
        return clause
        
    def is_solution_unique(self,tape):
        d = self.generate_variable()
        clause = [d] + self.uniqueness_clause(tape)
        print "uniqueness clause",clause
        self.s.add_clause(clause)
        result = self.try_solving([-d])
        self.s.add_clause([d]) # make the clause documents they satisfied
        if result:
            tp = self.holes2tape(result)
            print "alternative:",parse_tape(tp)
            print "alternative tape:",tp
            return False
        else:
            return True
                

    def holes2tape(self,result):
        return [ (1 if result[v] else 0) for v in self.tape2variable ]

    def try_sampling(self,subspace_dimension):
        for j in range(subspace_dimension):
            self.random_projection()
        result = self.try_solving()
        if result:
            print "Random projection satisfied"
            tp = self.holes2tape(result)
            print parse_tape(tp)[0]
            if self.is_solution_unique(tp):
                print "Unique. Accepted."
            else:
                print "Sample rejected"

    def adaptive_sample(self):
        subspace_dimension = 1
        result = self.try_solving()
        if result:
            print "Formula satisfied"
            for j in range(subspace_dimension):
                self.random_projection()
            while True:
                print "\n\niterating:"
                result = self.try_solving()
                if result:
                    print "Satisfied %d constraints" % subspace_dimension
                    tp = self.holes2tape(result)
                    print parse_tape(tp)
                    print "tape = ",tp
                    if self.is_solution_unique(tp):
                        print "UNIQUE"
                        print "<<< ==  ==  == >>>"
                    self.random_projection()
                    subspace_dimension += 1
                else:
                    print "Rejected %d projections" % subspace_dimension
                    print "total time = ",self.tt
                    break


    def enumerate_solutions(self,subspace_dimension = 0):
        for j in range(subspace_dimension):
            self.random_projection()
        solutions = []
        result = self.try_solving()
        d = self.generate_variable()
        logZ = float('-inf')
        while result:
            tp = self.holes2tape(result)
            program,mask = parse_tape(tp)
            if program in solutions:
                print "DUPLICATEPROGRAM",tp
                print mask
                break
            solutions = solutions + [program]
            specified = sum(mask)
            logZ = lse(logZ, -specified * 0.693)
            print "Enumerated program", program, "with", specified, "specified bits."
            #self.s.add_clause([d] + self.uniqueness_clause(tp))
            self.s.add_clause(self.uniqueness_clause(tp))
            result = self.try_solving()
        print "|s| =",len(solutions), "\tlog(z) =",logZ, "\t1/p =", math.exp(-logZ)
        return solutions
            
            
        
x = ProgramSolver(sys.argv[1])
#x.adaptive_sample()
x.enumerate_solutions(int(sys.argv[2]))
#x.try_sampling(int(sys.argv[2]))
print "total time = ",x.tt
