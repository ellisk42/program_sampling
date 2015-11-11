
tape_index = 0
def flip():
    global tape_index
    tape_index += 1
    return tape[tape_index-1]

def guard_expression(d):
    assert d > 0
    z = integer_expression(d - 1)
    c1 = flip()
    c2 = flip()

    o = None
    if c1: o = '= '
    if not c1 and c2: o = '< '
    if not c2 and not c2: o = '> '

    return "(%s %s)" % (o,z)

def array_expression(d):
    assert d > 0

    c1 = flip()

    if d == 1:
        if c1: return 'nil'
        return "a"
    
    c2 = flip()

    lp = array_expression(d - 1)
    z = integer_expression(d - 1)

    if d == 2:
        if c2 and c1: return 'nil'
        if c2 and not c1: return 'a'
        if not c2 and c1:
            return '(cdr %s)' % lp
        if not c2 and not c1:
            return '(list %s)' % z
    assert d > 2
    c3 = flip()
    g = guard_expression(d - 1)
    if c1 and c2 and c3: return 'nil'
    if c1 and c2 and not c3: return 'a'
    if c1 and not c2 and c3: return '(cdr %s)' % lp
    if c1 and not c2 and not c3: return '(list %s)' % z
    if not c1 and c2 and c3: return '(filter %s %s)' % (g,lp)

    assert False

def integer_expression(d):
    assert d > 0
    if d == 1: return '0'
    zp = integer_expression(d - 1)
    l = array_expression(d - 1)

    c1 = flip()
    c2 = flip()
    c3 = flip()

    if c1 and c2: return '0'
    if c1 and not c2: return '(+1 %s)' % zp
    if not c1 and c2: return '(-1 %s)' % zp
    if c3: return '(car %s)' % l
    return '(length %s)' % l

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

    return '(if (%s %s)\n%s\n(append\n%s\n%s\n%s))' % (g,target,b,x,y,z)
    
print main([0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,1,1,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1,1,0,1,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,1,1,0,1,0,1,1,0,0,0,1,1,1,1,0,0,0,0,0,1,0,0,0,1,1,1,1,0,0,1,0,0,0,1,0,1,1,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,1,0,1,1,0,1,0,0,0,0,0,0,0])
print main([0,0,0,0,1,1,0,1,1,0,0,0,0,1,0,0,1,0,1,0,1,0,0,0,0,1,0,0,0,0,0,1,0,1,0,1,0,0,0,1,0,0,0,0,0,1,1,0,1,0,1,0,1,0,0,1,0,1,1,0,0,0,0,1,1,0,0,0,1,0,0,1,0,1,0,0,1,0,0,0,1,0,1,1,0,0,0,1,1,1,1,0,0,0,1,0,0,1,1,0,0,0,0,1,0,1,0,0,0,0,1,0,1,1,0,0,1,0,0,0,0,1,0,0,0,0,1,1,0,1,1,0,0,0,0,1,0,0,0,0,0,0,0])
