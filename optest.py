#coding=utf-8
from grammar import *
from parsing import *
from lex import *
from util import *

from pprint import pprint

S,E,T,F = make(Vn,"S","E","T","F")
n,add,mul = make(Vt,"n","+","*")
IF,THEN,ELSE = make(Vt,"if","then","else")
g = Grammar([
    rule(S,[E]),
    rule(E,[E,add,T]),
    rule(E,[T]),
    rule(T,[T,mul,F]),
    rule(T,[F]),
    rule(F,[n]),
    rule(F,[IF,E,THEN,E,ELSE,E]),
])
node = [
    lambda e:{'s_prog':e},
    lambda e,t:{'add':[e,t]},
    lambda t : t,
    lambda t,f:{'mul':[t,f]},
    lambda f : f,
    lambda n:n,
    lambda e1,e2,e3:{'if':[e1,e2,e3]},
    ]
def str2vt(s):
    if isinstance(s,str):
        if s == '+':
            return add,None
        elif s == '*':
            return mul,None
        elif s == 'if':
            return IF,None
        elif s == 'then':
            return THEN,None
        elif s == 'else':
            return ELSE,None
        else:
            return n,s
    return s,None

lr1 = LR1(g)

print( "-------------------- fop --------------------" )
pprint( g.first_set )
print( "-------------------- lop --------------------") 
pprint( g.follow_set )
print( "--------------------  atable   --------------------" )
act,goto = lr1.table(lr1.items())
show( act )
print( "--------------------  gtable   --------------------" )
show( goto )
print( "--------------------  parse   --------------------" )
skips = [" ","\n","\t"]
spectab = {}
lex = Lexical(skips,spectab).lex
inp = """
if 1 * 2
then if it + it 
     then it
     else 0
else it * it
"""
inp = lex(inp)
ast = lr1.parse(inp,str2vt,node)
pprint( ast )
