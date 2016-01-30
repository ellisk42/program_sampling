
def Append(x,y): return x + y
def Const(x): return ''.join(x)

currentString = "zebra monkey"
def Pos(r1,r2,k):
    r1 = ''.join(r1)
    r2 = ''.join(r2)
    n1 = len(r1)
    n2 = len(r2)
             
    found = False

    for i in range(len(currentString)):
        if r1 == currentString[i : (i+n1)] and r2 == currentString[(i+n1) : (i+n1+n2)]:
            if k == 0:
                return i+n1
            else:
                if k < 3:
                    k -= 1
                else:
                    found = True
                    saved = i + n1

    assert found
    return saved

def SubString(p1,p2):
    if p1 < 0: p1 = len(currentString) + p1 + 1
    if p2 < 0: p2 = len(currentString) + p2 + 1
    if p1 == p2: p2 = p1 + 1
    assert p2 > p1
    return currentString[p1:p2]



def interpret(p,i):
    global currentString
    currentString = i
    try:
        return eval(p)
    except AssertionError:
        return ""

#print interpret("SubString(0,-1)","zebra")
