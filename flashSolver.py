import random
import math
from subprocess import Popen, PIPE
import os
import sys
from crypto import ProgramSolver,log2

from interpretFlash import interpret
from flashProblems import *

from composite1_5 import samples1_5

random.seed(os.urandom(10))
dumpPrefix = str(random.random())[2:]
print "Dumping to prefix",dumpPrefix

# should reconsider the case of a very tilted distribution?
# if this is true then were testing of baseline
#TILTED = True
# should we consider the case of arbitrarily enumerating programs?
DUMBBASELINE = False
# should we not even use an embedding, and sample bit strings uniformly?
OLDAPPROACH = True


PIECES = 3

CHARACTERLENGTH = 6

sketchCharacterMap = []
def decode_character(c):
    if c < len(sketchCharacterMap):
        return sketchCharacterMap[c]
    return c
def character_sketch(c):
    global sketchCharacterMap
    sketchCharacterMap = []
    output,errors = Popen(c, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True).communicate()
    print errors
    readingCharacters = False
    for l in output.split("\n"):
        if 'Printing out characters' in l:
            readingCharacters = True
        elif '[+] Printed out' in l:
            readingCharacters = False
        elif readingCharacters:
            sketchCharacterMap.append(eval(l))
    print "character map",sketchCharacterMap
    

def parse_tape(tape):
    tape_index = [0]
    def flip():
        tape_index[0] += 1
        return tape[tape_index[0]-1]
    def random_number():
        b1 = flip()
        b2 = flip()
        b3 = flip()
        b4 = flip()
        return 8*b1 + 4*b2 + 2*b3 + 1*b4
    def random_character():
        b1 = flip()
        b2 = flip()
        b3 = flip()
        b4 = flip()
        b5 = flip()
        b6 = flip()
        return 32*b1 + 16*b2 + 8*b3 + 4*b4 + 2*b5 + 1*b6

    def random_little_number():
        b1 = flip()
        b2 = flip()
        return 2*b1 + b2

    def term():
        r1 = [random_character(),random_character(),random_character()]
        r2 = [random_character(),random_character(),random_character()]

        r1l = random_little_number()
        r1l_p = random_little_number()
        r2l = random_little_number()
        r2l_p = random_little_number()

        
        p1_k = random_number()
        if p1_k > 7: p1_k = 7-p1_k
        p2_k = random_number()
        if p2_k > 7: p2_k = 7 - p2_k

        k1 = flip()
        k2 = flip()

        p1_occurrence = random_little_number()
        p2_occurrence = random_little_number()

        effective_r1l = max(0,
                            0 if k1 else r1l,
                            0 if k2 else r1l_p)
        effective_r2l = max(0,
                            0 if k1 else r2l,
                            0 if k2 else r2l_p)

        return_constant = flip()
        if return_constant:
            bit_mask = [1]*(r1l*CHARACTERLENGTH) + [0]*(CHARACTERLENGTH*(3-r1l)) # r1
            bit_mask += [0]*(3*CHARACTERLENGTH) # r2
            bit_mask += [1]*2 # r1l
            bit_mask += [0]*(2+2+2+ 4+4+ 1+1+ 2+2)
            bit_mask += [1] # return_constant
            return ("Const(%s)" % [ decode_character(c) for c in r1[0:r1l] ]), bit_mask
        if k1:
            p1 = str(p1_k)
        else:
            p1 = "Pos(%s,%s,%s)" % ([ decode_character(c) for c in r1[0:r1l] ],
                                    [ decode_character(c) for c in r2[0:r2l] ],
                                    p1_occurrence)

        if k2:
            p2 = str(p2_k)
        else:
            p2 = "Pos(%s,%s,%s)" % ([ decode_character(c) for c in r1[0:r1l_p] ],
                                    [ decode_character(c) for c in r2[0:r2l_p] ],
                                    p2_occurrence)

        bit_mask = [1]*(effective_r1l*CHARACTERLENGTH) + [0]*(CHARACTERLENGTH*(3-effective_r1l))
        bit_mask += [1]*(effective_r2l*CHARACTERLENGTH) + [0]*(CHARACTERLENGTH*(3-effective_r2l))
        bit_mask += [0 if k1 else 1]*2 # r1l
        bit_mask += [0 if k2 else 1]*2 # r1l_p
        bit_mask += [0 if k1 else 1]*2 # r2l
        bit_mask += [0 if k2 else 1]*2 # r2l_p
        bit_mask += [1 if k1 else 0]*4 # p1_k
        bit_mask += [1 if k2 else 0]*4 # p2_k
        bit_mask += [1,1] # k1,k2
        bit_mask += [0 if k1 else 1]*2 # p1_occurrence
        bit_mask += [0 if k2 else 1]*2 # p2_occurrence
        bit_mask += [1] # return_constant
        return ("SubString(%s,%s)" % (p1,p2)),bit_mask

    total_program,total_mask = [],[]
    for j in range(PIECES):
        p,m = term()
        total_program.append(p)
        total_mask += m

        composite = reduce(lambda a,x: "Append(%s,%s)" % (a,x),total_program)
        if j == PIECES-1: # last piece
            return composite, total_mask + [0]*(len(tape) - len(total_mask))
        #'++'.join(total_program)
        total_mask += [1]
        if flip():
            return composite, total_mask + [0]*(len(tape) - len(total_mask))


def createTrainingSet(problem,examples):
    body = "// automatically generated\ninclude \"flashSample.sk\";\nharness void main() {\n"
    maximumLength = 0
    characters = ""
    for e in range(5):
        if e + 1 in examples:
            [i,o] = flashProblems[problem - 1][e]
            maximumLength = max(maximumLength,len(i),len(o))
            characters += (i+o)            
            body += "testCase(\"%s\",\"%s\");\n" % (i,o)
    body += "}\n"
    print body
    print len(set(list(characters))),"distinct characters"
    with open("%s/flashProblems%s.sk" % (dumpPrefix,dumpPrefix),"w") as f:
        f.write(body)
    return maximumLength + 1

if False:
    for p in range(1,20):
        createTrainingSet(p,[1,2]) #[1,2,3,4,5])
    assert False

def printAccuracyCurve(samples,problem):
    if True:
        sampleAccuracy = {}
        for sample in list(set(samples)):
            print sample
            correct = 0
            for [i,o] in flashProblems[problem - 1]:
                prediction = interpret(sample,i)
                print i,"\t",prediction,"\t",o,"\t",prediction == o
                if prediction == o: correct += 1
            print "%d/5 correct\n" % correct
            sampleAccuracy[sample] = correct
        
        accuracyCurve = []
        for k in range(1,6):
            # what fraction got at least k correct?
            count = 0
            for s in sampleAccuracy:
                accuracy = sampleAccuracy[s]
                if accuracy > k-1:
                    count += len([ z for z in samples if s == z])
            averageAccuracy = float(count)/len(samples)
            print averageAccuracy,"got at least",k,"correct"
            accuracyCurve += [averageAccuracy]
        print accuracyCurve

#printAccuracyCurve(samples1_5,5)
#assert False
        
class FlashSolver(ProgramSolver):
    def parse_tape(self,t):
        p,m = parse_tape(t)
        assert len(m) == len(self.tape2variable)
        return p,m

if len(sys.argv) > 1:
    if ',' in sys.argv[1]:
        initial_tape = eval(sys.argv[1])
        print len(initial_tape)
        p,m = parse_tape(initial_tape)
        print p
        print sum(m)
    elif 'everything' == sys.argv[1]:
        examples = (len(sys.argv[2]) + 1)/2
        for p in range(1,20):
            os.system("python flashSolver.py problem%d %s" % (p,sys.argv[2]))
#            os.system("longjob -o examples%d/%d python flashSolver.py problem%d %s" % (examples,p,p,sys.argv[2]))
    elif 'problem' in sys.argv[1]:
        os.system('mkdir %s' % dumpPrefix)
        dumpfile = "/tmp/" + dumpPrefix + "_1.cnf"
        problem = int(sys.argv[1][len('problem'):])
        examples = map(int,sys.argv[2].split(','))
        maximumLength = createTrainingSet(problem,examples)
        print maximumLength

        def generateFormula(aux, shortest, originalApproach = False):
            originalApproach = 1 if originalApproach else 0
            command = "sketch %s/flashProblems%s.sk --fe-custom-codegen customcodegen.jar" % (dumpPrefix,dumpPrefix)
            command += " --beopt:outputSatNamed /tmp/%s" % dumpPrefix
            command += " --bnd-unroll-amnt %d --bnd-arr-size %d --bnd-arr1d-size %d" % (maximumLength,maximumLength,maximumLength)
            command += " --fe-def SHORTEST=%d,EMBEDDINGLENGTH=%d,ORIGINALAPPROACH=%d" % (shortest,aux,originalApproach)
            character_sketch(command)
        if len(sys.argv) == 4 and 'enumerate' == sys.argv[3]:
            generateFormula(1,10)
            ss = FlashSolver(filename = dumpPrefix + "_1.cnf",fakeAlpha = 0).enumerate_solutions(subsamples = 0)[0]
            for s in ss:
                print "(%s,%d),"%(s,ss[s][1]),
            assert False


        generateFormula(60,10,False)

        if DUMBBASELINE:
            samples = FlashSolver(filename = dumpfile).arbitrarily_enumerate(100)
            printAccuracyCurve(samples,problem)
            sys.exit()
        
        p,mdl = FlashSolver(filename = dumpfile).shortest_program()
        
        print "MDL predictions:"
        mdl_accuracy = 0
        for [i,o] in flashProblems[problem - 1]:
            prediction = interpret(p,i)
            print i,"\t",prediction,"\t",o,"\t",prediction == o
            if prediction == o: mdl_accuracy += 1
        print "MDL accuracy: %d/5" % mdl_accuracy

        if OLDAPPROACH:
            generateFormula(1,mdl,True)
            n = len(FlashSolver(filename = dumpfile).tape2variable)
            k = int(n - mdl) + 1 # start with 1/2 probability of survival of mdl estimate
            for _ in range(10):
                print "k = ",k
                sample = FlashSolver(filename = dumpfile).sampleOldApproach(k)
                if sample == "duplicate": k += 1
                elif sample == "unsatisfiable": k -= 1
            assert False

        
#        print [(1.0 if mdl_accuracy>=j else 0) for j in range(1,6)  ]
#        sys.exit()

        
        generateFormula(1,mdl)

        if False:
            everything = FlashSolver(filename = dumpPrefix + "_1.cnf",fakeAlpha = 0).enumerate_solutions(0,subsamples = 0)[0]
            for p in everything:
                print (p,everything[p][1]),","
            assert False

        generateFormula(1,mdl)
        S = FlashSolver(filename = dumpfile,fakeAlpha = 0).mbound(2)[1]
        print "\n\n>>>>>>>>> S = %d\n\n" % S

        a = int(mdl + log2(max(S,1)))
        print "Starting value of Alpha = ",a
        if TILTED:
            a = 179
            print "ignoring that value of Alpha, using",a
        generateFormula(a,mdl)

        N = FlashSolver(filename = dumpfile).mbound(2)[0]
        print "\n\n>>>>>>>>> N = %d" % N
        print "Lower bound:", (S - 1 + 2**(a - mdl))
        if N < (S - 1 + 2**(a - mdl)):
            N = (S - 1 + 2**(a - mdl))
        K = max(0,int(math.ceil(log2(max(N,1)))-2))
        print "Using K =",K

        samples = []
        while len(samples) < 100:
            samples += FlashSolver(filename = dumpfile).enumerate_solutions(K,subsamples = 1)[1]
        print "Got %d samples" % len(samples)

        printAccuracyCurve(samples,problem)
        '''
        sampleAccuracy = {}
        for sample in list(set(samples)):
            print sample
            correct = 0
            for [i,o] in flashProblems[problem - 1]:
                prediction = interpret(sample,i)
                print i,"\t",prediction,"\t",o,"\t",prediction == o
                if prediction == o: correct += 1
            print "%d/5 correct\n" % correct
            sampleAccuracy[sample] = correct
        
        accuracyCurve = []
        for k in range(1,6):
            # what fraction got at least k correct?
            count = 0
            for s in sampleAccuracy:
                accuracy = sampleAccuracy[s]
                if accuracy > k-1:
                    count += len([ z for z in samples if s == z])
            averageAccuracy = float(count)/len(samples)
            print averageAccuracy,"got at least",k,"correct"
            accuracyCurve += [averageAccuracy]
        print accuracyCurve
'''            
        os.system("rm %s" % dumpfile)
        os.system("rm -r %s" % dumpPrefix)
    else:
        random_projections = int(sys.argv[1])
        a = None
        if len(sys.argv) > 2:
            a = int(sys.argv[2])
        x = FlashSolver(fakeAlpha = a)
        x.enumerate_solutions(random_projections)
        print "total time = ",x.tt
else:
    x = FlashSolver()
    x.analyze_problem()
    print "total time = ",x.tt
