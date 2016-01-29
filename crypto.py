import math
import os
import time
import random
import re
import sys

from pycryptosat import Solver

from rank import binary_rank


def log2(x):
    if x <= 0: return float('-inf')
    return math.log(x)/math.log(2)


def lse2(x,y):
    if x < y: return lse2(y,x)
    return x + log2(1 + 2**(y - x))

def sample_distribution(d):
    r = random.random()
    a = 0
    for p,x in d:
        a += p
        if r < a: return x
    assert False
    
def sample_log2_distribution(d):
    lz = float('-inf')
    for l,_ in d: lz = lse2(lz,l)
    d = [ (2**(l-lz), x) for l,x in d ]
    return sample_distribution(d)



# h = # unused bits
# k = # random constraints
def exact_survival_probability(h,k):
    # how many mxn matrices have rank r?
    def count_matrices(m,n,r):
        if r == 0: return 1
        p = 1.0
        for i in range(r):
            p = p*(2.0**m - 2.0**i)*(2.0**n - 2.0**i)/(2.0**r - 2.0**i)
        return p

    s = 0 # summation accumulator
    for r in range(min(h,k)+1):
        rank_probability = 2**(-h*k) * count_matrices(h,k,r)
        s += rank_probability*2**(r-k)
    return s


        
        
class ProgramSolver():
    def __init__(self,fakeAlpha = None,filename = "sat_SYN_PREVIEW_1.cnf"):
        self.verbose = True
        self.s = Solver(threads = 1,verbose = 0)
        self.tt = 0

        h2v = {} # hole 2 variable
        a2v = {} # auxiliary 2 variable

        startTime = time.time()
        self.maximum_variable = -1
        readingComments = True
        with open(filename,'r') as f:
            for l in f:
                if readingComments and 'p cnf' in l:
                    readingComments = False
                    self.maximum_variable = int(l.split(' ')[2])
                    continue
                if readingComments and len(l) > len('c hole ') and l[:len('c hole ')] == 'c hole ':
                    ms = re.findall(r'(\d+) \- (\d+)', l)[0]
                    if not (int(ms[0]) == int(ms[1])):
                        print l
                        assert False
                    ms = int(ms[0])
                    n = re.findall(r'H__(\S+)_(\S+)\s',l)[0]
                    if n[0] == '0': # tape
                        h2v[int(n[1])] = ms
                    elif n[0] == '1': # auxiliary
                        a2v[int(n[1])] = ms
                elif len(l) > 0 and not ('c' == l[0]):
                    vs = l.split() #re.findall(r'(\-?\d+)',l)
                    assert vs[-1] == '0'
                    clause = [int(v) for v in vs[:-1] ]
                    self.s.add_clause(clause)
        print "Loaded",filename,"with",len(h2v),"holes and",len(a2v),"auxiliary variables in",(time.time()-startTime),"sec"

        # see if we are artificially decreasing alpha
        if fakeAlpha:
            if fakeAlpha > len(a2v):
                print "Attempting to fake an alpha value of",fakeAlpha,"which is larger than the actual",len(a2v)
                print "Increase maximum alpha within the sketch"
                assert False
        else:
            fakeAlpha = len(a2v)
        
        # convert the tape index into a sat variable
        self.tape2variable = [ v for h,v in sorted(h2v.items()) ]
        self.auxiliary2variable = [ v for h,v in sorted(a2v.items()) if h < fakeAlpha ]
        
        # converts a sat variable to a tape index
        self.variable2tape = dict([ (v,h) for h,v in h2v.items() ])
        self.variable2auxiliary = dict([ (v,h) for h,v in a2v.items() if h < fakeAlpha ])

        # rewaiting and rejection sampling
        self.alpha = len(self.auxiliary2variable)
        self.auxiliary_rows = []

        print "alpha =",self.alpha


    def parse_tape(self,tp):
        print "This should never be called"
        assert False
        
    def generate_variable(self):
        self.maximum_variable += 1
        return self.maximum_variable
    
    def random_projection(self):
        auxiliary_projection = [v for v in self.variable2auxiliary if random.random() > 0.5 ]
        self.auxiliary_rows.append([ (1 if v in auxiliary_projection else 0) for v in self.variable2auxiliary ])
        self.s.add_xor_clause(auxiliary_projection + 
                              [v for v in self.variable2tape if random.random() > 0.5 ],
                              random.random() > 0.5)

    # returns log_2 of the number of satisfying values of A given a description length
    def satisfying_auxiliaries(self,description_length):
        if description_length < self.alpha:
            # for each bit of description length, delete one column of A
            matrix_rows = [ r[description_length:] for r in self.auxiliary_rows ]
            r = binary_rank(matrix_rows)
            return self.alpha - description_length - r
        else:
            return 0
        
    def try_solving(self,assumptions = None):
        if self.verbose:
            print "About to run solver ==  ==  ==  > "
        start_time = time.time()
        if assumptions != None:
            result = self.s.solve(assumptions)
        else:
            result = self.s.solve()
        dt = (time.time() - start_time)
        self.tt += dt
        if self.verbose: print "Ran solver in time",dt
        if result[0]:
            bindings = {}
            for v in range(len(result[1])):
                if v in self.variable2tape:
                    bindings[v] = result[1][v]
            if self.verbose: print "Satisfiable."
            return bindings
        else:
            if self.verbose: print "Unsatisfiable."
            return False

    def uniqueness_clause(self,tape):
        p,bit_mask = self.parse_tape(tape)
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
            print "alternative:",self.parse_tape(tp)
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
            print self.parse_tape(tp)[0]
            if self.is_solution_unique(tp):
                print "Unique. Accepted."
            else:
                print "Sample rejected"


    def enumerate_solutions(self,subspace_dimension = 0):
        print "K =",subspace_dimension
        for j in range(subspace_dimension):
            self.random_projection()

        solutions = {}

        result = self.try_solving()
        while result:
            tp = self.holes2tape(result)
            program,mask = self.parse_tape(tp)
            description_length = sum(mask)
            if program in solutions:
                print "DUPLICATEPROGRAM",tp
                print mask
                print program
                assert False

            logNumberSolutions = self.satisfying_auxiliaries(description_length)
            solutions[program] = (logNumberSolutions, description_length)

            if self.verbose:
                print "Enumerated program", program, "with |x| =", description_length, "and",logNumberSolutions,"log satisfying auxiliary variables"
            if self.verbose or len(solutions)%1000 == 0: print self.tt,"cumulative solver time"

            self.s.add_clause(self.uniqueness_clause(tp))
            result = self.try_solving()

        # summary statistics
        logZ = float("-inf")
        for _,mdl in solutions.values(): logZ = lse2(logZ,-mdl)
        shortest = min([mdl for _,mdl in solutions.values() ])
        print "|s| =",len(solutions), "\tlog_2(z) =",logZ, "\t1/p =", 2**(-logZ), "\tshortest =",shortest,"bits"

        # How many solver queries did we save by the rank trick?
        implicitSolutionsEnumerated = sum([ 2**logNumberSolutions
                                            for p,(logNumberSolutions,mdl) in solutions.iteritems() ])
        print "Implicitly enumerated %d satisfying solutions" % implicitSolutionsEnumerated
        
        # sample a solution
        logDistribution = [ (logNumberSolutions, (p,mdl)) for p,(logNumberSolutions,mdl) in solutions.iteritems() ]
        acceptedSamples = []
        
        print "Samples:"
        for j in range(10):
            p,mdl = sample_log2_distribution(logDistribution)
            print p,mdl
            if mdl > self.alpha:
                # possibly reject
                acceptance_ratio = 2 ** (self.alpha - mdl)
                if random.random() < acceptance_ratio:
                    print "Accepted."
                    acceptedSamples += [p]
                else:
                    print "Rejected."
            else:
                print "Length bounded by alpha, so accepted."
                acceptedSamples += [p]
        return solutions,acceptedSamples
            

    def analyze_problem(self):
        # enumerate all solutions and their mdl
        # do an analysis of acceptance probability as a function of alpha
        solutions = {}
        result = self.try_solving()
        while result:
            tp = self.holes2tape(result)
            program,mask = self.parse_tape(tp)
            print program, sum(mask)
            description_length = sum(mask)
            if program in solutions:
                print "DUPLICATEPROGRAM",tp
                print mask
                print program
                assert False
            solutions[program] = description_length
            self.s.add_clause(self.uniqueness_clause(tp))
            result = self.try_solving()
        print "|S| =",len(solutions)
        logz = float('-inf')
        for _,mdl in solutions.iteritems(): logz = lse2(logz,-mdl)
        shortestLength = min([solutions[p] for p in solutions ])
        print "log_2 Z =",logz,"\t1/p =",2**(-logz),"\tshortest =",shortestLength

        def count(a):
            k = 0
            for p in solutions:
                if solutions[p] > a: k += 1
            return k
        def pa(a):
            lp = float('-inf')
            for p in solutions:
                if solutions[p] > a:
                    lp = lse2(lp,-solutions[p])
            return 2**(lp - logz)
        def full_satisfying_solutions(a):
            c = 0
            for p in solutions:
                if solutions[p] > a: c += 1
                else: c += 2**(a-solutions[p])
            return c

        print "["
        for a in range(shortestLength,shortestLength+21):
            # probability that a sample from Q is accepted
            p_acceptance = 1.0/(1 + count(a)*(2**(-a-logz)) - pa(a))
            
            print "#a =",a
            print "[ # (k,<mc>,<T>,(1+mc)<T>,P(no survivors),P(acceptance from Q),|E|)"

            for k in range(20):
                # expected number of surviving solutions
                ne = full_satisfying_solutions(a) # number of solutions in the embedding
                mu = 2**(-k) * ne
                # upper bound on probability of no survivors
                p_no_survivors = min(1,1/mu)

                # upper bound on expected number of trials to get a sample
                et = 1.0/(p_acceptance - p_no_survivors) if (p_acceptance - p_no_survivors) > 0 else -1
#                p_acceptance / (1 - p_no_survivors if p_no_survivors < 1 else float('inf'))

                mc = 2**(-k)*count(a) # expected number of surviving programs
                for s in solutions:
                    ls = solutions[s]
                    if not (ls > a): # has auxiliary bits
                        mc += exact_survival_probability(a-ls,k)
                print "(%s,%s,%s,%s,%s,%s,%s)," % (k,mc,et,et*(1+mc),p_no_survivors,p_acceptance,ne)
                #print "k =",k,"mc =",mc,"<T> =",et,"<tt> =",et*(1+mc),"||   ",
                #print " p_no_survivors", p_no_survivors
            print "],"
        print "]"
#            if et < 1.00001: break

        
            

        
#x = ProgramSolver()
#x.enumerate_solutions(int(sys.argv[1]))
#x.try_sampling(int(sys.argv[2]))
#print "total time = ",x.tt
