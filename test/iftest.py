#coding=utf-8
from grammar import *
from parsing import *
from lex import *
from util import *

from pprint import pprint

S,S1 = make(Vn,"S","S1")
i,c,e,t = make(Vt,"i","c","e","t")
# i -> if 
# c -> <cond>
# e -> else
# t -> then
g = Grammar([
    rule(S1,[S]),
    rule(S,[i,c,t,S]),
    rule(S,[i,c,t,S,e,S]),
    rule(S,[c]),
])
node = [
    lambda s:{"prog":[s]},
    lambda c,S:{"when":[c,S]},
    lambda c,S1,S2:{"if":[c,S1,S2]},
    lambda c :{"S":c},
    ]
def str2vt(s):
    if s == 'if':
        return i,None
    elif s == 'then':
        return t,None
    elif s == 'else':
        return e,None
    elif isinstance(s,str):
        return c,s
    else:
        return s,None 
lr1 = LR1(g)
print( "-------------------- --------------------" )
pprint( g.first_set )
print( "-------------------- --------------------" )
pprint( g.follow_set )
print( "-------------------- --------------------" )
act,goto =  lr1.table(lr1.items())
show( act )
print( "-------------------- --------------------" )
show( goto )
print( "-------------------- --------------------" )
lex = Lexical([" ","\n","\t"],{}).lex
inp = """
if abc 
then if b then b else c
else if a then b
"""
inp = lex(inp)
pprint( lr1.parse( inp,str2vt,node) )
