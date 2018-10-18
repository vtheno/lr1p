#coding=utf-8
from lr1p.grammar import *
from lr1p.parsing import *
from lr1p.lex import *
from lr1p.util import make,show

from pprint import pprint

S1,S,C = make(Vn,"S1","S","C")
c,d = make(Vt,"c","d")

g = Grammar([
    rule(S1,[S]),
    rule(S,[C,C]),
    rule(C,[c,C]),
    rule(C,[d])
])
node = [
    lambda s:{"S":s},
    lambda c1,c2:{"CC":[c1,c2]},
    lambda c,C:{"cC":[c,C]},
    lambda d:{"d":[d]},
    ]
def str2vt(s):
    if s == 'c':
        return c,s
    elif s == 'd':
        return d,s
    else:
        return s,None

print ( "----------------------------------------" )
pprint(g.first_set)
print ( "----------------------------------------" )
pprint(g.follow_set)
print ( "----------------------------------------" )
lex = Lexical([" ","\n","\t"],{})
lr1 = LR1(g,lex)
print( "=> target" )
show( lr1.targets )
print ( "----------------------------------------" )
show( lr1.action_table )
print ( "----------------------------------------" )
show( lr1.goto_table )
print ( "----------------------------------------" )

inp = """
c d d
"""
ast = lr1.parse(inp,str2vt,node)
pprint( ast )

