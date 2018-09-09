#coding=utf-8
from util import *
from collections import namedtuple
rule = namedtuple('rule',['name','body'])
item = namedtuple('item',['name','left','rest'])
def item_repr(self):
    name = repr(self.name) + ' -> '
    left = ''.join([repr(i) for i in self.left]) + '.' 
    right = ''.join([repr(i) for i in self.rest])
    return  name + left + right 
item.__repr__ = item_repr
def add(a,b):
    a.extend([x for x in b if x not in a])
    return a
class Symbol(type):
    def __new__(cls,name,parents,attrs):
        attrs["__name__"] = name
        attrs["__repr__"] = lambda self:self.__name__
        return type.__new__(cls,name,parents,attrs)
def newSymbol(name):
    return Symbol(name,(),{})()
def newSymbols(*names):
    return tuple([newSymbol(name) for name in names])
class Grammar(object):
    def __init__(self,*rules):
        rules = list(rules)
        first = rules[0].name
        G = newSymbol(first.__name__ + "'")
        self.first_rule = rule(G,[first])
        self.rules = [self.first_rule] + rules
        self.all_symbols = self.all_symbol()
        self.all_tokens = self.all_token()
        self.alls = self.all_symbols + self.all_tokens
        self.alls = [i for i in self.alls if i!=self.first_rule.name]
        print(self.alls )
    def all_symbol(self):
        out = [ ]
        for rule in self.rules:
            L,R = rule
            out += [i for i in [L] + R if type(i).__class__ is Symbol]
        return list(set(out))
    def all_token(self):
        out = [ EOF ]
        for rule in self.rules:
            L,R = rule
            out += [i for i in [L] + R if not type(i).__class__ is Symbol]
        return list(set(out))
    def __repr__(self):
        return repr(self.rules)

class LR(object):
    def __init__(self,G):
        self.Stack = Stack(256 * 256)
        self.Stack.push( 0 )
        self.G = G
    def Closure(self,I : [item] ) -> [item] :
        assert type(I) is list,"Closure : [item] -> [item]"
        assert all([type(i) is item for i in I]),"Closure : [item] -> [item]"
        i = 0
        I = list(I)
        while 1:
            new_item = False
            for _item in I:
                X =  _item.rest[0] if _item.rest else EOF
                for name,body in self.G.rules:
                    if name == X:
                        x = item(name,[],body)
                        if x not in I:
                            I += [x]
                            new_item = True
            if new_item is False:
                break
        return I
    def Goto(self,I,X):
        J = [ ]
        for i in I:
            if i.rest and i.rest[0] == X:
                next_i = item(i.name,i.left + i.rest[:1],i.rest[1:])
                J += [ next_i ]
        return self.Closure(J)
    def Items(self):
        all_len = len(self.G.alls)
        init = {k:v for k,v in zip(self.G.alls,[None]*all_len)}
        table = [
            init,
        ]
        I0 = [item(self.G.first_rule.name,[],self.G.first_rule.body)]
        C = self.Closure( I0 )
        items = [ C ]
        todo = [ C ]
        i = 0
        while i < len(todo):
            Si = todo[i]
            for X in self.G.alls:
                J = self.Goto(Si,X)
                if J and J not in items:
                    items += [ J ]
                    todo += [ J ]
                    table += [
                        {k:v for k,v in zip(self.G.alls,[None]*all_len)}
                        ]
                table[i][X] = SHIFT(items.index(J)) if J in items else REJECT
            i += 1
        for index,its in enumerate(items):
            #print( index,its )
            for it in its:
                #print( it )
                if not it.rest:
                    if it.name == self.G.first_rule.name:
                        table[index][EOF] = ACCEPT
                    elif it.name in [rule.name for rule in self.G.rules]:
                        inp = it.left[:1][0]
                        i = self.G.rules.index( rule(it.name,
                                                     it.left + it.rest))
                        #print( "it:",inp, it , i)
                        table[index][EOF] = REDUCE(i)
        for i in items:
            print( 'i',i )
        for t in table:
            print( 't:',t )
        return items
E,T = newSymbols("E","T")

g = Grammar(
    rule(E,[T,'+',E]),
    rule(E,[T]),
    rule(T,['id']),
    )
print( g.alls )
lr = LR(g)
#print( lr.Closure( [ item(g.first_rule.name,[],g.first_rule.body) ] ) )
lr.Items()
