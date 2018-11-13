#coding=utf-8
from lr1p.parser import parser
from lr1p.grammar import Vt,Vn
from lr1p.lex import Lexical
skips = [" ","\n","\t"]
lex = Lexical(skips,{})
def sym2sym(s):
    if s == "lparent":
        return "("
    elif s == "rparent":
        return ")"
    elif s == "add":
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
def expr(term:Vn,add:Vt,expr:Vn)->Vn:
    """
    expr -> term + expr
    """
    return {"add":[term,expr]}
@parse.add_rule
def expr(term:Vn,sub:Vt,expr:Vn)->Vn:
    """
    expr -> term - expr
    """
    return {"sub":[term,expr]}
@parse.add_rule
def expr(term:Vn)->Vn:
    """
    expr -> term
    """
    return term
@parse.add_rule
def term(factor:Vn,mul:Vt,term:Vn)->Vn:
    """
    term -> factor * term
    """
    return {"mul":[factor,term]}
@parse.add_rule
def term(factor:Vn,div:Vt,term:Vn)->Vn:
    """
    term -> factor / term
    """
    return {"div":[factor,term]}
@parse.add_rule
def term(factor:Vn)->Vn:
    """
    temr -> factor
    """
    return factor
@parse.add_rule
def factor(ident:Vt) -> Vn:
    """
    factor -> ident
    ident -> num
    ident -> var
    """
    if ident.isdigit():
        return {"num":int(ident)}
    return {"var":ident}
@parse.add_rule
def factor(lparent:Vt,expr:Vn,rparent:Vt)->Vn:
    """
    factor -> ( expr )
    """
    return expr
@parse.add_rule
def factor(IF:Vt,expr_1:Vn,then:Vt,expr_2:Vn,Else:Vt,expr_3:Vn)->Vn:
    """
    factor -> if expr then expr else expr
    """
    return {"if":[expr_1,expr_2,expr_3]}
parse = parse.build(lex)
print(parse("2 * (1 + 3) / 2"))
print(parse("2 * 1 + 3 / 2"))
print(parse("b + if a then 1 else 2"))
# output: 
# {'program': {'mul': [{'num': 2}, {'div': [{'add': [{'num': 1}, {'num': 3}]}, {'num': 2}]}]}}
# {'program': {'add': [{'mul': [{'num': 2}, {'num': 1}]}, {'div': [{'num': 3}, {'num': 2}]}]}}
