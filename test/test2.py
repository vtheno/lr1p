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
E = Vn("E")
#num = Vt("num")

#IF = Vt("if")
#THEN = Vt("then")
#ELSE = Vt("else")

g = Grammar([
    rule(S,[E]),
    rule(E,[E,add,E]),
    rule(E,[E,mul,E]),
    rule(E,[n]),
])
node = [
    lambda e:{'prog':e},
    lambda e1,e2:{'add':[e1,e2]},
    lambda e1,e2:{'mul':[e1,e2]},
    lambda e: {'id':e},
    ]
lr1 = LR1(g)
def show(I):
    for n,i in enumerate(I):
        print( f"{n} => {i!r}" )
from pprint import pprint
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
def str2vt(s):
    if isinstance(s,str):
        if s == '+':
            return add,None
        elif s == '*':
            return mul,None
        else:
            return n,s
    return s,None

inp = """
1 + 2 + 3
"""
inp = lex(inp)
ast = lr1.parse(inp,str2vt,node)
pprint( ast )

