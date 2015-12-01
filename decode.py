import sys

tape_index = 0
def flip():
    global tape_index
    tape_index += 1
    return tape[tape_index-1]

def guard_expression(d):
    assert d > 0

    c1 = flip()
    c2 = flip()

    z = integer_expression(d - 1)

    o = None
    if c1: o = 'eq'
    if not c1 and c2: o = 'gt'
    if not c2 and not c2: o = 'lt'

    return "('%s', %s)" % (o,z)

def array_expression(d):
    assert d > 0
    shallow = not (d > 2)

    c1 = flip()

    if d == 1:
        if c1: return "'nil'"
        return "'a'"
    
    c2 = flip()
    c3 = None
    if not shallow: c3 = flip()

    lp = array_expression(d - 1)
    z = integer_expression(d - 1)
    g = None
    if not shallow:
        g = guard_expression(d - 1)

    if (shallow and c1 and c2) or ((not shallow) and c1 and c2 and c3): return "'nil'"
    if (shallow and c1 and (not c2)) or ((not shallow) and c1 and c2 and (not c3)): return "'a'"
    if (shallow and (not c1) and c2) or ((not shallow) and c1 and (not c2) and c3):
        return "('cdr', %s)'" % lp
    if (shallow and (not c1) and (not c2)) or ((not shallow) and c1 and (not c2) and (not c3)):
        return "('list', %s)'" % z
    if (not shallow) and (not c1) and c2 and c3:
        return "('filter', %s, %s)" % (g,lp)

    assert False

def integer_expression(d):
    assert d > 0
    if d == 1: return '0'

    c1 = flip()
    c2 = flip()
    c3 = flip()

    zp = integer_expression(d - 1)
    l = array_expression(d - 1)

    if c1 and c2 and c3: return '0'
    if c1 and c2 and (not c3): return "('+1', %s)" % zp
    if c1 and (not c2) and c3: return "('-1', %s)" % zp
    if c1 and (not c2) and (not c3): return "('car', %s)" % l
    if (not c1) and c2 and c3: return "('length', %s)" % l

def main(t):
    global tape
    global tape_index
    tape_index = 0
    tape = [ f == 1 for f in t ]
    g = guard_expression(3)
    target = integer_expression(3)
    assert tape_index == 16
    b = array_expression(4)
    x = array_expression(4)
    rx = flip()
    y = array_expression(4)
    ry = flip()
    z = array_expression(4)
    rz = flip()

    if rx: x = '(sort %s)' % x
    if ry: y = '(sort %s)' % y
    if rz: z = '(sort %s)' % z

    return '(if (%s %s)\n    %s\n    (append %s\n            %s\n            %s))' % (g,target,b,x,y,z)


input_tape = "[%s]" % sys.argv[1]
print main(eval(input_tape))
