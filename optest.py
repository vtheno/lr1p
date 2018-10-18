#coding=utf-8
from lr1p.grammar import *
from lr1p.parsing import *
from lr1p.lex import *
from lr1p.util import *

from pprint import pprint
import time
"""
Prog -> Expr
Expr -> Expr + Term ;; Add
     |- Term
Term -> Term Term ;; App 
     |- Term `Term` Term ;; BinOp App
     |- Factor
Factor -> ident 
       |- if Expr then Expr else Expr
       |- let ident = Expr in Expr
       |- fn ident => Expr
       |- ( Expr )
"""
S,E,T,F = make(Vn,"S","E","T","F")
n,add,mul = make(Vt,"n","+","*")
lp,rp = make(Vt,'(',')')
lq,rq = make(Vt,'[',']')
IF,THEN,ELSE = make(Vt,"if","then","else")
LET,IN,assgin = make(Vt,"let","in","=")
FN,AS = make(Vt,"fn","=>")
quote = Vt("`")
spectab = {
    "=":[">"],
}
g = Grammar([
    rule(S,[E]),
    rule(E,[T]),
    rule(T,[T,T]),
    rule(T,[T,quote,T,quote,T]),
    rule(T,[F]),
    rule(F,[n]),
    rule(F,[IF,E,THEN,E,ELSE,E]),
    rule(F,[LET,n,assgin,E,IN,E]),
    rule(F,[FN,n,AS,E]),
    rule(F,[lp,E,rp]),
])
node = [
    lambda e:{'s_prog':e},
    lambda t : t,
    lambda t1,t2:{'app':[t1,t2]},
    lambda t1,t2,t3:{"app":[t2,t1,t3]},
    lambda f : f,
    lambda n:n,
    lambda e1,e2,e3:{'if':[e1,e2,e3]},
    lambda n,e1,e2:{'let':[n,e1,e2]},
    lambda n,e : {"fn":[n,e]},
    lambda e : e,
    ]
def str2vt(s):
    if isinstance(s,str):
        if s == 'if':
            return IF,None
        elif s == 'then':
            return THEN,None
        elif s == 'else':
            return ELSE,None
        elif s == '(':
            return lp,None
        elif s == ')':
            return rp,None
        elif s == "let":
            return LET,None
        elif s == "in":
            return IN,None
        elif s == "=":
            return assgin,None
        elif s == "fn":
            return FN,None
        elif s == "=>":
            return AS,None
        elif s == "`":
            return quote,None
        else:
            return n,s
    return s,None
print( "-------------------- fop --------------------" )
pprint( g.first_set )
print( "-------------------- lop --------------------") 
pprint( g.follow_set )
#print( "--------------------  atable   --------------------" )
#act,goto = lr1.table(lr1.items())
#show( act )
#print( "--------------------  gtable   --------------------" )
#show( goto )
print( "--------------------  parse   --------------------" )
skips = [" ","\n","\t"]
lex = Lexical(skips,spectab)
from cProfile import Profile
_t1 = time.perf_counter()
lr1 = LR1(g,lex) 
_t2 = time.perf_counter()
print( "started.",_t2 - _t1 )
prof = Profile()
prof.runcall( lambda : LR1(g,lex) )
prof.print_stats()

while 1:
    inp = input('>> ')
    if inp == ':q':
        break
    try:
        ast = lr1.parse(inp,str2vt,node)
        pprint( ast )
        pprint( lr1.lex.pos )
    except ParseError as e:
        print( f"!> SyntaxError: {e}" )
