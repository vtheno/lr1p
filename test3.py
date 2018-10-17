#coding=utf-8
from grammar import *
from parsing import *
from lex import *
from util import make

S,E,T,F = make(Vn,"S","E","T","F")
id,lp,rp,add,mul = make(Vt,"id","(",")","+","*")

g = Grammar([
    rule(S,[E]),
    rule(E,[E,add,T]),
    rule(E,[T]),
    rule(T,[T,mul,F]),
    rule(T,[F]),
    rule(F,[id]),
    rule(F,[lp,E,rp]),
])
node = [
    lambda e:{"S":e},
    lambda e,t:{'e_add':[e,t]},
    lambda t:{"E":t},
    lambda t,f:{'t_mul':[t,f]},
    lambda f:{"T":f},
    lambda id:{"f_id":id},
    lambda e:{"(e)":e},
    ]
def str2vt(s):
    if s == 'id':
        return e,s
    elif s == '+':
        return add,None
    elif s == '*':
        return mul,None
    elif s == '(':
        return lp,None
    elif s == ')':
        return rp,None
    elif isinstance(s,str):
        return id,s
    else:
        return s,None
lr1 = LR1(g)
def show(x):
    for i,v in enumerate(x):
        print( f"{i} => {v}" )
from pprint import pprint
items = lr1.items()
pprint( items[0] )
print ( "----------------------------------------" )
act,goto = lr1.table(items)
show( act )
print ( "----------------------------------------" )
show( goto )
print ( "----------------------------------------" )
lex = Lexical([" ","\n","\t"],{}).lex
inp = """
1 * (2 + 3)
"""
inp = lex(inp)
ast = lr1.parse(inp,str2vt,node)
pprint( ast )
