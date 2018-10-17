#coding=utf-8
from grammar import *
from parsing import *
from lex import *
from util import make,show

E,E1,T,T1,F = make(Vn,"E","E1","T","T1","F")
add,mul = make(Vt,"+","*")
x,y = make(Vt,"x","y")
lp,rp = make(Vt,"(",")")
g = Grammar([
    rule(E,[T,E1]),
    rule(E1,[add,T,E1]),
    rule(E1,[bottom]),
    rule(T,[F,T1]),
    rule(T1,[mul,F,T1]),
    rule(T1,[bottom]),
    rule(F,[lp,E,rp]),
    rule(F,[x]),
    rule(F,[y]),
])
node = [
    lambda t,e1:[t,e1],
    lambda t,e1:{'add':[t,e1]},
    lambda b:b,
    lambda f,t1:[f,t1],
    lambda f,t1:{'mul':[f,t1]},
    lambda b:b,
    lambda e:e,
    lambda a:a,
    lambda b:b,
    ]
def str2vt(s):
    if s == 'x':
        return x,s
    elif s == 'y':
        return y,s
    elif s == "(":
        return lp,None
    elif s == ")":
        return rp,None
    elif s == '+':
        return add,None
    elif s == '*':
        return mul,None
    else:
        return s,None
from pprint import pprint

print ( "----------------------------------------" )
pprint(g.first_set)
print ( "----------------------------------------" )
pprint(g.follow_set)
print ( "----------------------------------------" )
lr1 = LR1(g)

items = lr1.items()
act,goto = lr1.table(items)
show( act )
print ( "----------------------------------------" )
show( goto )
print ( "----------------------------------------" )
lex = Lexical([" ","\n","\t"],{}).lex
inp = """
x
"""
inp = lex(inp)
ast = lr1.parse(inp,str2vt,node)
pprint( ast )
