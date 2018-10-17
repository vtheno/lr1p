from grammar import *
from parsing import *
from lex import *

S1 = Vn("S'")
S = Vn("S")
A = Vn("A")
E = Vn("E")
id = Vt("id")
add = Vt("+")
an = Vt(";")
assgin = Vt(":=")
g = Grammar([
    rule(S1,[S]), # lambda _ : _
    rule(S,[S,an,A]), # lambda s,_,a: s + [a]
    rule(S,[A]),#  lambda a : a
    rule(A,[E]),# lambda e : e
    rule(A,[id,assgin,E]), # lambda id,_,e:{'=':[id,e]}
    rule(E,[E,add,id]),# lambda e,_,id:{'+',:[e,id]}
    rule(E,[id]),# lambda id:id
])
node = [
    lambda s:{'prog':s},# S' -> S
    lambda s,a: {"s_SA":[s,a]},# S -> S ; A
    lambda a:{"s_A":a},# S -> A
    lambda e:{'a_A':e},# A -> E
    lambda id,e:{'a_assgin':[id,e]}, # A -> id := E 
    lambda e,id:{'e_add':[e,id]}, # E -> E + id 
    lambda id:{'e_id':id}, # E -> id
    ]
lr0 = LR1(g)
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
items = lr0.items()
pprint( items )
print( "--------------------  atable   --------------------" )
act,goto = lr0.table(items)
show( act )
print( "--------------------  gtable   --------------------" )
show( goto )
print( "--------------------  parse   --------------------" )
show( node )
print( "--------------------  parse   --------------------" )
skips = [" ","\n","\t"]
spectab = {
    ":" : ["="]
}
inp = """
b := 3 + 4;
a := 1 + 2;
b
"""
def str2vt(s:str) -> Vt:
    if isinstance(s,str):
        if s not in [":=","+",";"]:
            return id,s
        elif s == ":=":
            return assgin,None
        elif s == ";":
            return an,None
        else:
            return add,None
    return s,None
inp = Lexical(skips,spectab).lex(inp)
ast = lr0.parse( inp, str2vt,node )
pprint( ast )
show( ast )
## TODO SR table choice level
