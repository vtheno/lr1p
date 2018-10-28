#coding=utf-8
from lr1p.grammar import *
from lr1p.parsing import *
from lr1p.util import *
from types import FunctionType

class parser(object):
    def __init__(self):
        self.rules = [ ]
        self.node = [ ]
        self.maps = {}
        self.V = [ ]
    def general_str2vt(self,s):
        if isinstance(s,str):
            val = self.maps.get(s,self.get_V('id'))
            #print( "val =>",val)
            return val,s
        return s,None
    def add_rule(self,fn):
        name = fn.__name__.lower()
        annotations = {k.lower():v for k,v in fn.__annotations__.items()}
        length = len(annotations)
        argcount = fn.__code__.co_argcount
        varnames = fn.__code__.co_varnames[:]
        argnames = [varnames[i].lower() for i in range(argcount)]
        argnames = [k if k.split("_")== 1 else k.split("_")[0] for k in argnames]
        if length == argcount + 1:
            annotations[name] = annotations.pop("return")
            env = {k if k.split("_")== 1 else k.split("_")[0]:v for k,v in annotations.items()}
            self.maps.update( env )
            r = (name,argnames)
            self.rules += [r]
            self.node  += [fn]
            return fn
        else:
            raise TypeError("def type error")
    def compute_V(self):
        for k,v in self.maps.items():
            sym = k
            #val = sym.split("_")
            #if len(val) > 1:
            #    sym = val[0]
            if sym not in (i.sym for i in self.V):
                self.V.append(v(sym))
    def get_V(self,sym):
        for v in self.V:
            if v.sym == sym:
                return v
        else:
            raise ValueError(f"{sym} not in self.V")
    def compute_rules(self):
        rules = [ ]
        for lhs,rhs in self.rules:
            r = rule(self.get_V(lhs),[self.get_V(rh) for rh in rhs])
            rules += [r]
        self.rules = rules
    def compute_maps(self):
        for k,v in self.maps.items():
            val = self.get_V(k)
            if isinstance(val,v):
                self.maps[k] = val
    def build(self,lex):
        self.compute_V()
        #print( self.maps )
        self.compute_maps()
        #print(self.rules)
        self.compute_rules()
        #print(self.V)
        grammar = Grammar(self.rules)
        lr1 = LR1(grammar,lex)
        parse = lambda inp:lr1.parse(inp,self.general_str2vt,self.node)
        return parse

__all__ = ["parser"]
