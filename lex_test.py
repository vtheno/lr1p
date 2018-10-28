#coding=utf-8
from lr1p.lex import *
from lr1p.parser import parser
from lr1p.grammar import Vn,Vt
lex = Lexical([" ","\r","\t","\n"])
g = parser()
@g.add_rule
def S(Expr:Vn)->Vn:
    return Expr
@g.add_rule
def expr(id:Vt) -> Vn:
    if id.isdigit():
        return {"num":int(id)}
    return {"var":id}
@g.add_rule
def expr(IF:Vt,expr_1:Vn,then:Vt,expr_2:Vn,Else:Vt,expr_3:Vn)->Vn:
    return {"if":[expr_1,expr_2,expr_3]}
g1 = g.build(lex)
print( g1(input(">> ")) )
