#coding=utf-8
from grammar import *
from parsing import *
from lex import *
S = Vn("S")
A = Vn("A")
T = Vn("T")
F = Vn("F")
P = Vn("P")
i,n = Vt("i"),Vt("n")
add = Vt("+")
sub = Vt("-")
mul = Vt("*")
div = Vt("/")
lp,rp = Vt("("),Vt(")")
up = Vt("|")
#E = Vn("E")
#num = Vt("num")

#IF = Vt("if")
#THEN = Vt("then")
#ELSE = Vt("else")

g = Grammar([
    rule(S,[A]),
    rule(A,[T]),
    rule(A,[A,add,T]),
    rule(A,[A,sub,T]),
    rule(T,[F]),
    rule(T,[T,mul,F]),
    rule(T,[T,div,F]),
    rule(F,[P]),
    rule(F,[P,up,F]),
    rule(P,[i]),
    rule(P,[n]),
    rule(P,[lp,A,rp]),
])

"""
first_op = {}
last_op = {}
for lhs,rhs in g.R:
    first_op[lhs] = [ ]
    last_op[lhs] = [ ]

def first_op_point(lhs,rhs):
    i,l,out = 0,len(rhs),[ ]
    start = rhs[i]
    if isinstance(start,Vt):
        value = [i for i in [start] if i not in first_op[lhs]]
        if value:
            out += value
    elif isinstance(start,Vn):
        value = [i for i in [start] if i not in first_op[lhs]]
        if value:
            out += value
        if i + 1 < l:
            i += 1
            start = rhs[i]
            value = [i for i in [start] if i not in first_op[lhs]]
            if value:
                out += value
    return out
def last_op_point(lhs,rhs):
    l = len(rhs)
    out = [ ]
    i = l - 1
    start = rhs[i]
    if isinstance(start,Vt):
        value = [i for i in [start] if i not in last_op[lhs]]
        if value:
            out += value
    elif isinstance(start,Vn):
        value = [i for i in [start] if i not in last_op[lhs]]
        if value:
            out += value
        if i > 1:
            i -= 1
            start = rhs[i]
            value = [i for i in [start] if i not in last_op[lhs]]
            if value:
                out += value
    return out

changed = True
while changed:
    changed = False
    for lhs,rhs in g.R:
        value = [i for i in first_op_point(lhs,rhs) if i not in first_op[lhs]]
        if value:
            first_op[lhs] += value
            changed = True
        value = [i for i in last_op_point(lhs,rhs) if i not in last_op[lhs]]
        if value:
            last_op[lhs] += value
            changed = True

changed = True
while changed:
    changed = False
    for lhs,ops in first_op.items():
        for op in ops:
            if isinstance(op,Vn):
                value = [i for i in first_op[op] if i not in first_op[lhs] and i!=op]
                if value:
                    value = [i for i in first_op[lhs] + value if i!=op]
                    if value:
                        first_op[lhs] = value
                        changed = True

for lhs,ops in first_op.items():
    first_op[lhs] = [i for i in first_op[lhs] if not isinstance(i,Vn)]

changed = True
while changed:
    changed = False
    for lhs,ops in last_op.items():
        for op in ops:
            if isinstance(op,Vn):
                value = [i for i in last_op[op] if i not in last_op[lhs] and i!=op]
                if value:
                    value = [i for i in last_op[lhs] + value if i!=op]
                    if value:
                        last_op[lhs] = value
                        changed = True

for lhs,ops in last_op.items():
    last_op[lhs] = [i for i in last_op[lhs] if not isinstance(i,Vn)]
"""
from pprint import pprint
pprint( g.first_op )
print( "--------------------  --------------------" )
pprint( g.last_op )
# lr1 = LR1(g)
"""
from pprint import pprint
def show(I):
    for n,i in enumerate(I):
        print( f"{n} => {i!r}" )
print( "-------------------- nullable --------------------" )
pprint( g.nullable_set )
print( "--------------------  first   --------------------" )
pprint( g.first_set)
print( "--------------------  follow  --------------------" )
pprint( g.follow_set )
print( "--------------------  grammar --------------------" )
pprint( g.R )
print( "--------------------  Items   --------------------" )
items = lr1.items()
show( items )
print( "--------------------  atable   --------------------" )
act,goto = lr1.table(items)
show( act )
print( "--------------------  gtable   --------------------" )
show( goto )
print( "--------------------  parse   --------------------" )
show( node )
print( "--------------------  parse   --------------------" )
skips = [" ","\n","\t"]
spectab = {}
lex = Lexical(skips,spectab).lex
def str2vt(s):
    if isinstance(s,str):
        if s == "if":
            return IF,None
        elif s == "then":
            return THEN,None
        elif s == "else":
            return ELSE,None
        if s == '+':
            return add,None
        elif s == '*':
            return mul,None
        else:
            return num,s
    return s,None

inp = """
#1 + 2 + 3
"""
inp = lex(inp)
ast = lr1.parse(inp,str2vt,node)
pprint( ast )
"""
