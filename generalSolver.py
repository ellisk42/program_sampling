import os
import random
import sys
from crypto import ProgramSolver,log2
from subprocess import Popen, PIPE
from itertools import permutations

# if this is true we use a simple lower bound on the model count rather than comput it
useLowerBound = True

# should reconsider the case of a very tilted distribution?
# if this is true then were testing of baseline
TILTED = False


# Do not use an embedding
ORIGINALAPPROACH = True

def reverse(l):
    return list(reversed(l))

def countFirst(l):
    return len([ x for x in l[1:] if x == l[0] ])



production_lengths = {}
def record_production(p,d,l):
    global production_lengths
    if (p,d) in production_lengths:
        assert production_lengths[(p,d)] == l
    production_lengths[(p,d)] = l

def blank(l):
    return [0]*len(l)

tape_index = 0
def flip():
    global tape_index
    tape_index += 1
    return tape[tape_index-1]

def guard_expression(d,z):
    assert d > 0

    c1 = flip()
    c2 = flip()

    o = None
    if c1 and c2: o = 'eq'
    if not c1 and c2: o = 'gt'
    if not c2 and not c2: o = 'lt'

    program = "(%s %s)" % (o,z)
    mask = [1,1]

    record_production("guard",d,len(mask))
    
    return program,mask

def array_expression(d):
    assert d > 0

    c1 = flip()

    if d == 1:
        record_production("array",d,1)
        if c1: return "nil",[1]
        return "a",[1]

    choiceMask = [1,1,1]
    
    c2 = flip()
    c3 = flip()

    lp,lp_m = array_expression(d - 1)
    z,z_m = integer_expression(d - 1)
    g,g_m = guard_expression(d - 1,z)

    record_production("array",d,len(choiceMask+lp_m+z_m+g_m))
    shallow = False

    if (c1 and c2 and c3):
        return "nil",choiceMask+blank(lp_m)+blank(z_m)+blank(g_m)
    if (c1 and c2 and (not c3)):
        return "a",choiceMask+blank(lp_m)+blank(z_m)+blank(g_m)
    if (c1 and (not c2) and c3):
        return ("(cdr %s)" % lp), choiceMask+lp_m+blank(z_m)+blank(g_m)
    if (c1 and (not c2) and (not c3)):
        return ("(list %s)" % z), choiceMask+blank(lp_m)+z_m+blank(g_m)
    if (not c1) and c2 and c3:
        return ("(filter %s %s)" % (g,lp)), choiceMask+lp_m+z_m+g_m

    return "FAILURE_A",[0]*(len(choiceMask+lp_m+z_m+g_m))

def integer_expression(d):
    assert d > 0
    if d == 1:
        record_production("integer",d,0)
        return '0',[]

    c1 = flip()
    c2 = flip()
    c3 = flip()
    choiceMask = [1,1,1]
    
    zp,z_m = integer_expression(d - 1)
    l,l_m = array_expression(d - 1)

    record_production("integer",d,len(choiceMask+z_m+l_m))

    if c1 and c2 and c3: return '0',choiceMask+blank(z_m)+blank(l_m)
    if c1 and c2 and (not c3): return ("(p1 %s)" % zp),choiceMask+z_m+blank(l_m)
    if c1 and (not c2) and c3: return ("(m1 %s)" % zp),choiceMask+z_m+blank(l_m)
    if c1 and (not c2) and (not c3): return ("(car %s)" % l),choiceMask+blank(z_m)+l_m
    if (not c1) and c2 and c3: return ("(length %s)" % l),choiceMask+blank(z_m)+l_m

    return "FAILURE_Z",[0]*(len(choiceMask+z_m+l_m))
#    assert False

def parse_tape(t):
    global tape
    global tape_index
    tape_index = 0
    tape = [ f == 1 for f in t ]
    c,c_m = integer_expression(2)
    g,g_m = guard_expression(2,c)
    target,t_m = integer_expression(2)
    b,b_m = array_expression(2)
    x,x_m = array_expression(3)
    rx = flip()
    y,y_m = array_expression(3)
    ry = flip()
    z,z_m = array_expression(3)
    rz = flip()

    if rx: x = '(recur %s)' % x
    if ry: y = '(recur %s)' % y
    if rz: z = '(recur %s)' % z

    program = '(if (%s %s)\n    %s\n    (append %s\n            %s\n            %s))' % (g,target,b,x,y,z)
    mask = c_m+g_m+t_m+b_m+x_m+[1]+y_m+[1]+z_m+[1]

    return program,mask

class GeneralSolver(ProgramSolver):
    def parse_tape(self,t):
        if len(t) == 64:
            p,m = parse_tape(t)
            return p,m
        if len(t) == 67:
            global tape
            global tape_index
            tape_index = 0
            tape = [ f == 1 for f in t ]
            return integer_expression(5)
        assert False

def marginal_evaluation(p,n,f):
    multiset = {}
    for pp in p:
        multiset[pp] = 1 + multiset.get(pp,0)
    
    successes = 0
    attempts = 50
    for attempt in range(attempts):
        testCase = list(range(1,n+1))
        random.shuffle(testCase)
        lp = "(list %s)" % (str(list(testCase)).replace(',',' ').replace(']','').replace('[',''))
        for pp in multiset:
            w = multiset[pp]
            pp = pp.replace('append','safe-append').replace("\n"," ")
            po = Popen(["./evaluateGeneral.scm",pp,lp], stdin=PIPE, stdout=PIPE, stderr=PIPE)
            stdout, stderr = po.communicate()
            if "bottom" in stdout or stderr != "": continue
            try:
                output = map(int,stdout.replace("(","").replace(")","").split(" "))
                if output == f(testCase): successes += w
            except:
                continue
    return float(successes)/len(p)/attempts

def marginal_counting(p,n):
    multiset = {}
    for pp in p:
        multiset[pp] = 1 + multiset.get(pp,0)
    
    successes = 0
    attempts = 50
    for attempt in range(attempts):
        (testCase,target) = countTestCases(1,forceL = n)[0]
        lp = "(list %s)" % (str(testCase).replace(',',' ').replace(']','').replace('[',''))
        for pp in multiset:
            w = multiset[pp]
            po = Popen(["./evaluateGeneral.scm",pp,lp], stdin=PIPE, stdout=PIPE, stderr=PIPE)
            stdout, stderr = po.communicate()
            if "bottom" in stdout or stderr != "": continue
            try:
                output = int(stdout.strip())
                if output == target: successes += w
            except:
                continue
    return float(successes)/len(p)/attempts


def outputTestCases(ts):
    global dumpPrefix
    enforce = "enforce" if isinstance(ts[0][1],list) else "enforce_counting"
    testCase= "test_case" if isinstance(ts[0][1],list) else "counting_case"
    with open(dumpPrefix+"/generalTests.sk","w") as f:
        f.write("include \"general.sk\";\nharness void main() { %s(); \n" % enforce)
        for t in range(len(ts)):
            i = ",".join(map(str,ts[t][0]))
            if isinstance(ts[0][1],list):
                o = "{" + ",".join(map(str,ts[t][1])) + "}"
            else:
                o = str(ts[t][1])
            l = "%s({%s},%s);\n" % (testCase,i,o)
            f.write(l)
        f.write("}")

def makeTestCases(n,f):
    ts = []
    while len(ts) < n:
        p = random.random()
        if p < 0.6:
            l = 3
        elif p < 0.8:
            l = 2
        elif p < 0.9:
            l = 1
        elif p < 1.0:
            l = 0
            
        i = [ random.randint(0,7) for j in range(l) ]
        if l == len(list(set(i))):
            o = f(i)
            t = (i,o)
            if str(t) in [str(x) for x in ts ]:
                continue
            ts += [t]
    return ts

def countTestCases(n, forceL = None):
    tests = []
    while len(tests) < n:
        if forceL == None:
            l = random.randint(1,4)
        else:
            l = forceL
        k = random.randint(1,l)
        target = random.randint(0,7)

        i = [ random.randint(0,7) for j in range(l-k) ] + [target]*k
        random.shuffle(i)
        i = [target] + i
        if countFirst(i) == k and not str((i,k)) in map(str,tests):
            tests += [(i,k)]
    return tests




random.seed(os.urandom(10))
dumpPrefix = str(random.random())[2:]
print "Dumping to prefix",dumpPrefix

if len(sys.argv) == 1:
    x = GeneralSolver(filename = "sat_SYN_1.cnf")
    x.analyze_problem()
    print "total time = ",x.tt
else:
    if 'parse' in sys.argv[1]:
        input_tape = "[%s]" % sys.argv[2]
        p,m = parse_tape([ (x == 1) for x in eval(input_tape) ])
        print p
        print m
        print len(m)
        print production_lengths
    elif 'sort' == sys.argv[1] or 'reverse' == sys.argv[1] or 'count' == sys.argv[1]:

        # = len(sys.argv) == 2 or sys.argv[2] == 'lb'
        
        print "%s test cases:" % sys.argv[1]

        if sys.argv[1] == "sort":
            correctImplementation = sorted
            testCases = makeTestCases(int(sys.argv[2]),sorted)
            tapeLength = 64
            MAXLIST = 3
            MINLENGTH = 23
        if sys.argv[1] == "count":
            correctImplementation = countFirst
            testCases = countTestCases(int(sys.argv[2]))
            tapeLength = 67
            MAXLIST = 5
            MINLENGTH = 3
        if sys.argv[1] == "reverse":
            correctImplementation = reverse
            testCases = makeTestCases(int(sys.argv[2]),reverse)
            tapeLength = 64
            MAXLIST = 3
            MINLENGTH = 23

        os.system("mkdir %s" % dumpPrefix)
        outputTestCases(testCases)
        os.system("cat %s/generalTests.sk" % dumpPrefix)

        # el = embedded length
        # ml = minimum length
        def generateFormula(el,ml,originalApproach = False):
            command = "sketch %s/generalTests.sk" % dumpPrefix
            command += " --bnd-unroll-amnt %d --bnd-arr1d-size %d --bnd-arr-size %d" % (MAXLIST,MAXLIST,MAXLIST)
            command += " --fe-def BOUND=%d,EMBEDDINGLENGTH=%d,MINIMUMLENGTH=%d,ORIGINALAPPROACH=%d" % (tapeLength,el,ml,originalApproach)
            command += " --beopt:outputSatNamed /tmp/%s" % dumpPrefix
            os.system(command)
        
        dumpCNF = "/tmp/%s_1.cnf" % dumpPrefix
        generateFormula(tapeLength,MINLENGTH)

        if False:
            print "everything:"
            everything = GeneralSolver(filename = dumpPrefix + "_1.cnf",fakeAlpha = 0).enumerate_solutions(0,subsamples = 0)[0]
            for p in everything:
                print (p,everything[p][1]),","
        if False: # baseline: repeatedly querying the solver with different random seeds
            print "Samples from different random seeds:"
            stupidSamples = []
            for j in range(1000):
                stupidSamples += GeneralSolver(filename = dumpPrefix + "_1.cnf").arbitrarily_enumerate(1)
            print stupidSamples

        shortest,L = GeneralSolver(filename = dumpCNF).shortest_program()
        samples = [shortest]
        if False: # accuracy of MAP
            for l in range(1,15):
                if sys.argv[1] == 'count':
                    print marginal_counting(samples,l),',',
                else:
                    print marginal_evaluation(samples,l,correctImplementation),',',
                assert False # force death of process

        if ORIGINALAPPROACH:
            generateFormula(1,L,True)
            n = len(GeneralSolver(filename = dumpCNF).tape2variable)
            k = int(n - L) + 1 # start with 1/2 probability of survival of mdl estimate
            print "L = ",L
            for _ in range(10):
                print "k = ",k
                sample = GeneralSolver(filename = dumpCNF).sampleOldApproach(k)
                if sample == "duplicate": k += 1
                elif sample == "unsatisfiable": k -= 1
            assert False
        
        generateFormula(1,L)

        # S = number of consistent programs
        S = GeneralSolver(filename = dumpCNF,fakeAlpha = 0).model_count()
        print "S =",S
        a = min(int(L + log2(S)+4),tapeLength)
        if TILTED:
            a = tapeLength
            print "ignoring alpha,using",a
        
        generateFormula(a,L)

        lowerBound = 2**(int(a)-L) + S - 1
        if useLowerBound:
            print "|E| bounded by",lowerBound
            K = int(log2(lowerBound))
        else:
            N = GeneralSolver(filename = dumpCNF).model_count()
            print "|E| ~",N
            lowerBound = 2**(int(a)-L) + S - 1
            print "Bounded by",lowerBound
            K = int(log2(N) - 3)
        print "Generating samples"
        
        samples = []
        while len(samples) < 5:
            samples += GeneralSolver(filename = dumpCNF).enumerate_solutions(K,subsamples=1)[1]

        print samples
        print "Got",len(samples),"samples with",len(set(samples)),"unique solutions\n[",
        if False:
            for l in range(1,15):
                if sys.argv[1] == 'count':
                    print marginal_counting(samples,l),',',
                else:
                    print marginal_evaluation(samples,l,correctImplementation),',',
        print ']'
        os.system("rm %s" % dumpCNF)
        os.system("rm -r %s" % dumpPrefix)
    else:
        random_projections = int(sys.argv[1])
        a = None
        if len(sys.argv) > 2:
            a = int(sys.argv[2])
        x = GeneralSolver(fakeAlpha = a)
        solutions,samples = x.enumerate_solutions(random_projections)
        print "total time = ",x.tt

        marginal_sort(samples,4)
        

        
