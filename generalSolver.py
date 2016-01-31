import os
import random
import sys
from crypto import ProgramSolver,log2
from subprocess import Popen, PIPE
from itertools import permutations


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
        p,m = parse_tape(t)
        return p,m

def marginal_sort(p,n):
    multiset = {}
    for pp in p:
        multiset[pp] = 1 + multiset.get(pp,0)
    
    l = list(range(1,n+1))
    successes = 0
    attempts = 50
    for attempt in range(attempts):
        lp = list(range(1,n+1))
        random.shuffle(lp)
        lp = "(list %s)" % (str(list(lp)).replace(',',' ').replace(']','').replace('[',''))
        for pp in multiset:
            w = multiset[pp]
            pp = pp.replace('append','safe-append').replace("\n"," ")
            po = Popen(["./evaluateGeneral.scm",pp,lp], stdin=PIPE, stdout=PIPE, stderr=PIPE)
            stdout, stderr = po.communicate()
            if "bottom" in stdout or stderr != "": continue
            try:
                output = map(int,stdout.replace("(","").replace(")","").split(" "))
                if output == l: successes += w
            except:
                continue
    return float(successes)/len(p)/attempts

def outputTestCases(ts):
    global dumpPrefix
    with open(dumpPrefix+"/generalTests.sk","w") as f:
        f.write("include \"general.sk\";\nharness void main() { enforce(); \n")
        for t in range(len(ts)):
            i = ",".join(map(str,ts[t][0]))
            o = ",".join(map(str,ts[t][1]))
            l = "test_case({%s},{%s});\n" % (i,o)
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


            

if False:
    samples = []
    marginal_sort(samples,2)
    assert False

def reverse(l):
    return list(reversed(l))


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
    elif 'sort' == sys.argv[1] or 'reverse' == sys.argv[1]:
        print "%s test cases:" % sys.argv[1]
        
        os.system("mkdir %s" % dumpPrefix)
        outputTestCases(makeTestCases(int(sys.argv[2]),sorted if sys.argv[1] == "sort" else reverse))
        os.system("cat %s/generalTests.sk" % dumpPrefix)
        def generateFormula(el,ml):
            command = "sketch %s/generalTests.sk" % dumpPrefix
            command += " --fe-def EMBEDDINGLENGTH=%d,MINIMUMLENGTH=%d" % (el,ml)
            command += " --beopt:outputSatNamed %s" % dumpPrefix
            os.system(command)
        generateFormula(64,23)
        shortest,L = GeneralSolver(filename = dumpPrefix + "_1.cnf").shortest_program()
        generateFormula(1,L)
        S = GeneralSolver(filename = dumpPrefix + "_1.cnf",fakeAlpha = 0).model_count()
        print "S =",S
        a = min(int(L + log2(S)),64)
        generateFormula(a,L)
        N = GeneralSolver(filename = dumpPrefix + "_1.cnf").model_count()
        print "N =",N
        lowerBound = 2**(int(a)-L) + S - 1
        print "Bounded by",lowerBound
        print "Generating samples"
        K = int(log2(lowerBound))
        samples = sum([ GeneralSolver(filename = dumpPrefix + "_1.cnf").enumerate_solutions(K)[1]
                        for j in range(5) ],[])
        print samples
        print "Got",len(samples),"samples"
        for l in range(1,15):
            print marginal_sort(samples,l)
        os.system("rm %s_1.cnf" % dumpPrefix)
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
        

        
