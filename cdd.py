#coding=utf-8
from grammar import *
from parsing import *
from lex import *
from util import make,show

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
lr1 = LR1(g)

items = lr1.items()
act,goto = lr1.table(items)
show( act )
print ( "----------------------------------------" )
show( goto )
print ( "----------------------------------------" )
lex = Lexical([" ","\n","\t"],{}).lex

inp = """
c d d
"""
inp = lex(inp)
ast = lr1.parse(inp,str2vt,node)
pprint( ast )
