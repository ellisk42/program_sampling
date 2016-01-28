import sys
from crypto import ProgramSolver


PIECES = 3

CHARACTERLENGTH = 6

sketchCharacterMap = ['null',' ','!','"','#','D','I','J','K','P','R','T','U','a','b']
def decode_character(c):
    if c < len(sketchCharacterMap):
        return "'" + sketchCharacterMap[c] + "'"
    return c

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


class FlashSolver(ProgramSolver):
    def parse_tape(self,t):
        p,m = parse_tape(t)
        return p,m

if __name__ == "__main__" and False:
    initial_tape = eval(sys.argv[1])
    print len(initial_tape)
    p,m = parse_tape(initial_tape)
    print p
    print m

if len(sys.argv) > 1:
    if ',' in sys.argv[1]:
        initial_tape = eval(sys.argv[1])
        print len(initial_tape)
        p,m = parse_tape(initial_tape)
        print p
        print sum(m)
        sys.exit()
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
