__all__ = ['parse','Atom','SExpr','symbol']
           
class Atom:
    def __init__(self,value,type):
        self.value = value
        self.type  = type
    def __repr__(self):
        return "Atom %s(%s)"%(str(self.type.__name__),repr(self.value))

class SExpr:
    def __init__(self,items):
        self.items = items
    def __str__(self):
        return "SExpr(%s)"%repr(self.items)
    def __repr__(self): return str(self)

class symbol:
    def __init__(self,name):
        self.name = name
    def __repr__(self):
        return self.name
    
tail = lambda x: x[1:]

def findEndBracket(m1,m2,st):
    n = 0
    d = 0
    for s in st:
        if s == m1:
            n += 1
            d += 1
        elif s == m2 and d > 0:
            n += 1
            d -= 1
        elif s == m2 and d == 0:
            return n+1
        else: n += 1

def getBetween(m1,m2,st):
    p = findEndBracket(m1,m2,tail(st))
    if not p: return tail(st)
    else: return st[1:p]


def dropTill(fn,ul):
    n = 0
    for li in ul:
        if not fn(li):
            n += 1
        else: break
    return ul[n:]

def dropWhile(fn,ul):
    n = 0
    for li in ul:
        if fn(li):
            n += 1
        else: break
    return ul[n:]

def takeTill(fn,ul):
    n = 0
    for li in ul:
        if not fn(li):
            n += 1
        else: break
    return ul[0:n]


def breakAt(m,st):
    try:
        i = st.index(m)
        return (st[0:i],st[i+1:])
    except ValueError:
        return (st,"")


def parseItem(st):
    ret = []
    while True:
        s = dropTill(lambda x: not x in " \n"  or x in "()",st)
        if not s: break
        n = s[0]

        if n == "\"":                                               
            s1  = tail(s)
            end = s1.index("\"")

            st  = s1[end+1:]
            ret += [Atom(s1[:end],str)] 

        elif n == ";" and s[1] == ";":
            st = s[s.index("\n"):]

        elif n == ')': st = tail(s)                      

        elif n == '(':                                                
            expr = SExpr(parseItem(getBetween("(",")",s)))
            end  = findEndBracket("(",")",tail(s)) or len(s)
            st   = s[end+1:].strip()
            ret += [expr]

        else:                                                       
            (a,st) = breakAt(" ",s)
            if all(map(lambda x: x in "0123456789" + ".",a)):
                if "." in a:
                    t = float
                else:
                    t = int
            else:
                t = symbol
            ret += [Atom(a.strip(),t)] 
    return ret

def parse(st):
    ret = []
    while True:
        step = dropWhile(lambda x: x in " \n",st)
        if step:
            if step[0:2] == ";;":
                if "\n" in step:
                    st = step[step.index("\n"):]
                else:
                    st = []
            else:
                top  = "(%s)"%getBetween("(",")",step)
                ex   = parseItem(top)
                end  = findEndBracket("(",")",tail(step)) or (len(step)-1)
                rest = step[end+1:]
                if not ex or not ex[0].items:
                    st = rest
                else:
                    ret += ex
                    st = rest
        else:
            break
        
    return ret
