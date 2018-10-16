#coding=utf-8
from util import *
from lex import Lexical
from grammar import *

from collections import namedtuple

item = namedtuple('item',['lhs','rhs_l','rhs_r','la'])
item.__repr__ = lambda self:f"{self.lhs} -> {' '.join([repr(i) for i in self.rhs_l])} . {' '.join([repr(i) for i in self.rhs_r])}  , {self.la}"

class LR1(object):
    def __init__(self,g:Grammar) -> 'LR1':
        self.g = g
        self.start = [ item(self.g.S,[],self.g.R[0].rhs,eof) ]

    def closure(self, I : [item] ) -> [item]:
        I = I[:]
        changed = True
        while changed:
            changed = False
            for it in I:
                X = it.rhs_r[0] if it.rhs_r else [ ]
                tail = it.rhs_r[1:]
                head = self.g.first_point(tail + [it.la])
                #print("=>",head )
                for lhs,rhs in self.g.R:
                    if X == lhs:
                        for b in head:
                            value = item(lhs,[],rhs,b)
                            if value not in I:
                                I += [value]
                                changed = True
        return I

    def goto(self, I:[item], X : Vt and  Vn):
        J = [ ]
        for it in I:
            if it.rhs_r:
                if it.rhs_r[0] == X:
                    _it = item(it.lhs,it.rhs_l + [it.rhs_r[0]],it.rhs_r[1:],it.la)
                    J += [_it]
        return self.closure(J)

    def items (self) -> [item] :
        I0 = self.closure( self.start )
        C = [I0]
        changed = True
        while changed:
            changed = False
            for I in C:
                for x in self.g.Vt + self.g.Vn:
                    In = self.goto(I,x)
                    if In and In not in C:
                        C += [In]
                        changed = True
        return C

    def table (self, I : [item] ):
        action = [{} for i in I]
        goto   = [{} for i in I]
        for i in range(len(I)):
            for A in I[i]:
                if A.rhs_r:
                    j = self.goto(I[i],A.rhs_r[0])
                    if j:
                        idx = I.index(j)
                        if A.rhs_r[0] in self.g.Vt:
                            action[i][A.rhs_r[0]] = ('shift',idx)
                        else:
                            goto[i][A.rhs_r[0]] = ('shift',idx)
                elif A.rhs_l and A.rhs_r == [ ]:
                    if A.lhs != self.g.S:
                        action[i][A.la] = ('reduce',rule(A.lhs,A.rhs_l) )
                    else:
                        action[i][eof] = ('accept',rule(A.lhs,A.rhs_l) )
        return action,goto

    def next (self,g : ... ):
        try:
            val = next(g)
        except StopIteration:
            val = eof
        return val
        
    def parse (self, inp : ...,str2vt:'str -> Vt',node:['node'])->'ast':
        stack = Stack()
        action,goto = self.table(self.items())
        stack.push( 0 )
        current = self.next(inp)
        ast =  []
        while 1:
            token = current
            token,out = str2vt(token)
            if out:
                ast += [out]
            print( "ast stack =>",ast )
            state = stack.peek()
            (act,n) = action[state][token]
            #print( "act,n,stack =>",token,act,n,stack )
            if act == 'shift':
                stack.push(token)
                stack.push(n)
                current = self.next(inp)
            elif act == 'reduce':
                (lhs,rhs) = n
                length = len(rhs)
                drop = list(reversed([stack.pop() for n in range(length * 2)]))
                state = stack.peek()
                stack.push( lhs )
                act,val = goto[state][lhs]
                stack.push( val )
                # ast 
                idx = self.g.R.index(n)
                func = node[idx]
                count = func.__code__.co_argcount
                offset = len(ast)-count
                ast,args = ast[0:offset],ast[offset:]
                print( "args =>",idx,args,func(*args) )
                ast += [func(*args)]
            elif act == 'accept':
                state = stack.pop ()
                result = stack.pop ()
                idx = 0
                return node[idx](*ast)
            else:
                raise ValueError(f"{act}")

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
    lambda s,a: s + [a],# S -> S ; A
    lambda a:[a],# S -> A
    lambda e:e,# A -> E
    lambda id,e:{'assgin':[id,e]}, # A -> id := E 
    lambda e,id:{'add':[e,id]}, # E -> E + id 
    lambda id:id, # E -> id
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
a := 1 + 2;
b := a + 3;
c := b + 4;
d := a + b + c;
e
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
