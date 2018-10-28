#coding=utf-8
from lr1p.parser import parser
from lr1p.grammar import Vt,Vn
from lr1p.lex import Lexical
skips = [" ","\n","\t"]
lex = Lexical(skips)
def sym2sym(s):
    if s == "add":
        return "+"
    elif s == "sub":
        return "-"
    elif s == "mul":
        return "*"
    elif s == "div":
        return "/"
    else:
        val = s.split("_")
        if len(val) == 1:
            return s
        return val[0]
parse = parser(sym2sym,"ident")
@parse.add_rule
def program(expr:Vn) -> Vn:
    return {'program':expr}
@parse.add_rule
def expr(ident:Vt) -> Vn:
    if ident.isdigit():
        return {"num":int(ident)}
    return {"var":ident}
@parse.add_rule
def expr(expr_1:Vn,add:Vt,expr_2:Vn)->Vn:
    return {"add":[expr_1,expr_2]}

parse = parse.build()
