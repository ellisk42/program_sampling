from subprocess import Popen, PIPE
import os
import sys
from crypto import ProgramSolver

from flashProblems import *

PIECES = 3

CHARACTERLENGTH = 6

sketchCharacterMap = []
def decode_character(c):
    if c < len(sketchCharacterMap):
        return "'" + sketchCharacterMap[c] + "'"
    return c
def character_sketch(c):
    global sketchCharacterMap
    sketchCharacterMap = []
    output,errors = Popen(c, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True).communicate()
    print errors
    readingCharacters = False
    for l in output.split("\n"):
        print l
        if 'Printing out characters' in l:
            readingCharacters = True
        elif '[+] Printed out' in l:
            readingCharacters = False
        elif readingCharacters:
            sketchCharacterMap.append(l)
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
            return ("Const%s" % [ decode_character(c) for c in r1[0:r1l] ]), bit_mask
        if k1:
            p1 = str(p1_k)
        else:
            p1 = "pos(%s,%s,%s)" % ([ decode_character(c) for c in r1[0:r1l] ],
                                    [ decode_character(c) for c in r2[0:r2l] ],
                                    p1_occurrence)

        if k2:
            p2 = str(p2_k)
        else:
            p2 = "pos(%s,%s,%s)" % ([ decode_character(c) for c in r1[0:r1l_p] ],
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

        if j == PIECES-1: # last piece
            return '++'.join(total_program), total_mask + [0]*(len(tape) - len(total_mask))
        
        total_mask += [1]
        if flip():
            return '++'.join(total_program), total_mask + [0]*(len(tape) - len(total_mask))


def createTrainingSet(problem,examples):
    body = "// automatically generated\n"
    maximumLength = 0
    characters = ""
    for e in range(5):
        if e + 1 in examples:
            [i,o] = flashProblems[problem - 1][e]
            maximumLength = max(maximumLength,len(i),len(o))
            characters += (i+o)            
            body += "testCase(\"%s\",\"%s\");\n" % (i,o)
    print body
    print len(set(list(characters))),"distinct characters"
    with open("flashProblems.h","w") as f:
        f.write(body)
    return maximumLength + 1

if False:
    for p in range(1,20):
        createTrainingSet(p,[1,2]) #[1,2,3,4,5])
    assert False
        
class FlashSolver(ProgramSolver):
    def parse_tape(self,t):
        p,m = parse_tape(t)
        return p,m

if len(sys.argv) > 1:
    if ',' in sys.argv[1]:
        initial_tape = eval(sys.argv[1])
        print len(initial_tape)
        p,m = parse_tape(initial_tape)
        print p
        print sum(m)
    elif 'problem' in sys.argv[1]:
        problem = int(sys.argv[1][len('problem'):])
        examples = map(int,sys.argv[2].split(','))
        maximumLength = createTrainingSet(problem,examples)
        print maximumLength
        character_sketch("sketch flashSample.sk --fe-custom-codegen customcodegen.jar --be:outputSat --bnd-unroll-amnt %d --bnd-arr-size %d --bnd-arr1d-size %d" % (maximumLength,maximumLength,maximumLength))
#        print FlashSolver(fakeAlpha = 0).model_count()
        print FlashSolver().shortest_program()
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
