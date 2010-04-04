from sexpr.parser import *

DEBUG = False
def debug(x):
    if DEBUG == True:
        print x

class Lambda:
    def __init__(self,params,body):
        self.params = params
        self.body   = body

    def __call__(self,*args):
        global FNS
        debug("""LAMBDA CALLED:
        My Params: %s
        My Body:   %s
        The Args:  %s"""%(self.params,self.body,args))
        ORIG_FNS = dict(FNS)
        for k,v in zip(self.params,args):
            if isinstance(v,Atom) or isinstance(v,SExpr):
                FNS[k] = ee(v)
            else:
                FNS[k] = v
        ran = map(ee,self.body)[-1]
        FNS = ORIG_FNS
        return ran

class EvalError:
    def __init__(self,msg):
        self.message = msg
    def __repr__(self):
        return self.message
    
def evalSExpr(e):
    if isinstance(e,Atom):
        if (e.type == symbol):
            try:
                debug("EVALUATING: %s to %s"%(e,FNS[e.value]))
                ev = FNS[e.value]
            except KeyError:
                raise EvalError("symbol `%s` is not defined."%e.value)
            return ev
        else:
            return e.type(e.value)
    else:
        n = evalSExpr(e.items[0])
        if callable(n):
            a = e.items[1:]
            return callWith(n,a)
        else:
            return n

ee = evalSExpr

def evalA(fn):
    def aux(*args):
        ls = map(ee,args)
        return fn(*ls)
    return aux


def callWith(fn,ls):
    return fn(*ls)


@evalA
def toList(*args): return list(args)

@evalA
def printIt(x): print x

def defineInFNS(k,v):
    global FNS
    FNS[k.value] = ee(v)

def doIf(b,t,f):
    if ee(b):
        return ee(t)
    else:
        return ee(f)

def doMap(f,ls):
    return map(ee(f),ee(ls))

def makeLambda(*args):
    fargs = [x.value for x in args[0].items]
    return Lambda(fargs,list(args[1:]))

def getChar():
    return input()

def doExist(x):
    return FNS.has_key(x.value)

FNS = {
     '+':evalA(lambda a,b: a+b)
    ,'*':evalA(lambda a,b: a*b)
    ,'-':evalA(lambda a,b: a-b)
    ,'==':evalA(lambda a,b: a == b)
    ,'>':evalA(lambda a,b: a > b)
    ,'<':evalA(lambda a,b: a < b)
    ,'or':lambda a,b: ee(a) or ee(b)
    ,'and':lambda a,b: ee(a) and ee(b)
    ,'upper':evalA(lambda a: a.upper())
    ,'concat':evalA(lambda a,b: a + b)
    ,'map':doMap
    ,'str':evalA(str)
    ,'list':toList
    ,'foldl':evalA(reduce)
    ,'cons':evalA(lambda x: x[0])
    ,'cdr' :evalA(lambda x: x[1:])
    ,'define':defineInFNS
    ,'print':printIt
    ,'if': doIf
    ,'lambda':makeLambda
    ,'range':evalA(lambda a,b:range(a,b))
    ,'id':lambda x: ee(x)
    ,'getchar':getChar
    ,'exist?':doExist
    ,'pass':None
    }


def runSource(fl):
    exprs = parse(open(fl).read())
    ret = []
    for e in exprs:
        if len(e.items) > 0:
            ret += [evalSExpr(e)]
    return ret



