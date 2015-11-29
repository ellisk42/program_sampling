def blank(x):
    return [None for y in x ]


def guard_expression(e,d):
    assert d > 0
    z = integer_expression(e[1], d - 1)
    o = e[0]
    if o == 'eq':
        return [1,None] + z
    if o == 'lt':
        return [0,1] + z
    if o == 'gt':
        return [0,0] + z

def array_expression(e,d):
    assert d > 0
    shallow = not (d > 2)

    if d == 1:
        if e == 'nil': return [1]
        if e == 'a': return [0]
        assert False

    ba = blank(array_expression('a',d - 1))
    bi = blank(integer_expression(0,d - 1))
    bg = None
    if not shallow: bg = blank(guard_expression(('eq',0),d - 1))
    
    if e == 'nil':
        if shallow:
            return [1,1] + ba + bi
        return [1,1,1] + ba + bi + bg
    if e == 'a':
        if shallow:
            return [1,0] + ba + bi
        return [1,1,0] + ba + bi + bg
    
    f = e[0]
    if f == 'cdr':
        if shallow:
            return [0,1] + array_expression(e[1],d - 1) + bi
        return [1,0,1] + array_expression(e[1],d - 1) + bi + bg
    if f == 'list':
        if shallow:
            return [0,0] + ba + integer_expression(e[1],d - 1)
        return [1,0,0] + ba + integer_expression(e[1],d - 1) + bg
    if f == 'filter':
        assert not shallow
        return [0,1,1] + array_expression(e[2],d - 1) + bi + guard_expression(e[1],d - 1)

    assert False

def integer_expression(e,d):
    assert d > 0
    if d == 1:
        assert e == 0
        return [] # only one choice 0

    bi = blank(integer_expression(0,d - 1))
    ba = blank(array_expression('a',d - 1))

    if e == 0:
        return [1,1,1] + bi + ba
    f = e[0]
    if f == '+1':
        return [1,1,0] + integer_expression(e[1],d - 1) + ba
    if f == '-1':
        return [1,0,1] + integer_expression(e[1],d - 1) + ba
    if f == 'car':
        return [1,0,0] + bi + array_expression(e[1],d - 1)
    if f == 'length':
        return [0,1,1] + bi + array_expression(e[1],d - 1)
    assert False

g = guard_expression(('eq',0),3)
target = integer_expression(('length','a'),3)
b = array_expression('nil',4)
x = array_expression(('filter', ('lt',('car','a')),
                      ('cdr','a')),4)
y = array_expression(('list', ('car','a')),4)
z = array_expression(('filter', ('gt',('car','a')),
                      ('cdr','a')),4)
tape = g + target + b + x + [1] + y + [0] + z + [1]

def replace_none(x):
    if x == None: return 1
    return x
print len(tape)
print map(replace_none,tape)
print len([ t for t in tape if t != None ])
'''
[0, 1, 1, # filter
 1, 1, 0, # 'a'
 None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
 0, 0, # <
 0, 0, 1, # car
 0] # 'a'
'''
