import sys

def blank(l):
    return [0]*len(l)

tape_index = 0
def flip():
    global tape_index
    tape_index += 1
    return tape[tape_index-1]

def guard_expression(d):
    assert d > 0

    c1 = flip()
    c2 = flip()

    z,zm = integer_expression(d - 1)

    o = None
    if c1 and c2: o = 'eq'
    if not c1 and c2: o = 'gt'
    if not c2 and not c2: o = 'lt'

    program = "(%s %s)" % (o,z)
    mask = [1,1]+zm
    return program,mask

def array_expression(d):
    assert d > 0
    shallow = not (d > 2)

    c1 = flip()

    if d == 1:
        if c1: return "nil",[1]
        return "a",[1]

    choiceMask = [1,1]
    if not shallow: choiceMask += [1]
    
    c2 = flip()
    c3 = None
    if not shallow: c3 = flip()

    lp,lp_m = array_expression(d - 1)
    z,z_m = integer_expression(d - 1)
    g,g_m = None,[]
    if not shallow:
        g,g_m = guard_expression(d - 1)

    if (shallow and c1 and c2) or ((not shallow) and c1 and c2 and c3):
        return "nil",choiceMask+blank(lp_m)+blank(z_m)+blank(g_m)
    if (shallow and c1 and (not c2)) or ((not shallow) and c1 and c2 and (not c3)):
        return "a",choiceMask+blank(lp_m)+blank(z_m)+blank(g_m)
    if (shallow and (not c1) and c2) or ((not shallow) and c1 and (not c2) and c3):
        return ("(cdr %s)" % lp), choiceMask+lp_m+blank(z_m)+blank(g_m)
    if (shallow and (not c1) and (not c2)) or ((not shallow) and c1 and (not c2) and (not c3)):
        return ("(list %s)" % z), choiceMask+blank(lp_m)+z_m+blank(g_m)
    if (not shallow) and (not c1) and c2 and c3:
        return ("(filter %s %s)" % (g,lp)), choiceMask+lp_m+blank(z_m)+g_m

    return "FAILURE_A",[]

def integer_expression(d):
    assert d > 0
    if d == 1: return '0',[]

    c1 = flip()
    c2 = flip()
    c3 = flip()
    choiceMask = [1,1,1]
    
    zp,z_m = integer_expression(d - 1)
    l,l_m = array_expression(d - 1)

    if c1 and c2 and c3: return '0',choiceMask+blank(z_m)+blank(l_m)
    if c1 and c2 and (not c3): return ("(+1 %s)" % zp),choiceMask+z_m+blank(l_m)
    if c1 and (not c2) and c3: return ("(-1 %s)" % zp),choiceMask+z_m+blank(l_m)
    if c1 and (not c2) and (not c3): return ("(car %s)" % l),choiceMask+blank(z_m)+l_m
    if (not c1) and c2 and c3: return ("(length %s)" % l),choiceMask+blank(z_m)+l_m

    return "FAILURE_Z",[]
#    assert False

def main(t):
    global tape
    global tape_index
    tape_index = 0
    tape = [ f == 1 for f in t ]
    g,g_m = guard_expression(3)
    target,t_m = integer_expression(3)
    assert tape_index == 16
    b,b_m = array_expression(4)
    x,x_m = array_expression(4)
    rx = flip()
    y,y_m = array_expression(4)
    ry = flip()
    z,z_m = array_expression(4)
    rz = flip()

    if rx: x = '(sort %s)' % x
    if ry: y = '(sort %s)' % y
    if rz: z = '(sort %s)' % z

    program = '(if (%s %s)\n    %s\n    (append %s\n            %s\n            %s))' % (g,target,b,x,y,z)
    mask = g_m+t_m+b_m+x_m+[1]+y_m+[1]+z_m+[1]

    return program,mask


input_tape = "[%s]" % sys.argv[1]
p,m = main(eval(input_tape))
print p
print m
