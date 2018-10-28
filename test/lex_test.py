#coding=utf-8
from lr1p.lex import *
from lr1p.parser import parser
from lr1p.grammar import Vn,Vt
lex = Lexical([" ","\r","\t","\n"])
def sym2sym(s):
    """
    process python argname to string
    """
    if s == "sub":
        return "-"
    val = s.split("_")
    if len(val) == 1:
        return s
    return val[0]
g = parser(sym2sym,"id")
@g.add_rule
def S(Expr:Vn)->Vn:
    """
    ;; infact
    s : Vn
    expr : Vn
    
    s -> expr
    """
    return Expr
@g.add_rule
def expr(expr_1:Vn,sub:Vt,expr_2:Vn)->Vn:
    return {"sub":[expr_1,expr_2]}
@g.add_rule
def expr(id:Vt) -> Vn:
    """
    expr -> id
    ;; id is build-in vt symbol
    """
    if id.isdigit():
        return {"num":int(id)}
    return {"var":id}
@g.add_rule
def expr(IF:Vt,expr_1:Vn,then:Vt,expr_2:Vn,Else:Vt,expr_3:Vn)->Vn:
    """
    expr_1 is expr
    expr_2 is expr
    expr_n is expr,process by "<xxx>_<n>"
    """
    return {"if":[expr_1,expr_2,expr_3]}
g1 = g.build(lex)
print( g1(input(">> ")) )
