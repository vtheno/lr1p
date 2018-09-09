#coding=utf-8
from util import *
from collections import namedtuple
# non-terminal is all_symbols
# terminal is all_tokens
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
    def First(self,x):
        #if x in self.all_tokens:
        #    return [x]
        #first =  [ ]
        #lst = [body[0] for name,body in self.rules if name == x and name!=body[0]]
        #for x in lst:
        #    first.extend( self.First(x) )
        #return list(set(first))
        if x in self.all_tokens:
            return [x]
        f = []
        for name,body in self.rules:
            if name == x and body[0] != x:
                fn = self.First(body[0])
                f.extend(fn)
        return list(set(f))
    def __repr__(self):
        return repr(self.rules)

class LR(object):
    def __init__(self,G):
        self.Stack = Stack(256 * 256)
        self.Stack.push( SHIFT(0) )
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
                        #print( self.G.all_tokens )
                        for e in self.G.all_tokens:
                            if table[index][e] == REJECT:
                                table[index][e] = REDUCE(i)
                            #table[index][EOF] = REDUCE(i)
        for index,i in enumerate(items):
            print( f'i{index}',i )
        for index,t in enumerate(table):
            print( f't{index}:',t )
        return table#items
    def parse(self,inp):
        self.table = self.Items()
        self.inp = inp
        while 1:
            token = self.inp.current
            state = (self.Stack.peek()).n
            action = self.table[state][token]
            print( token,action,self.Stack )
            if isinstance(action,SHIFT):
                si = action
                self.Stack.push(token)
                self.Stack.push(si)
                self.inp.next()
            elif isinstance(action,REDUCE):
                rule_index = action.n
                rule = self.G.rules[rule_index]
                (A,body) = rule
                length = len(body)
                popn = self.Stack.popn( length + length )
                state = self.Stack.peek()
                self.Stack.push( A )
                self.Stack.push( self.table[state.n][A] )
            elif action == ACCEPT:
                state,result = self.Stack.popn(2)
                return result
            else:
                raise TypeError("{}".format(action))
E,T,F = newSymbols("E","T","F")
"""
----------------------------------------
E = T + E # this is right assoc
  | T
T = id
----------------------------------------
E = E + T # this is left assoc
  | T
T = id 
----------------------------------------
"""
g = Grammar(
    rule(E,[E,'+',T]),
    rule(E,[T]),
    rule(T,['id']),
    )
g1 = Grammar(
    rule(E,[T,'+',E]),
    rule(E,[T]),
    rule(T,['id']),
    )
g2 = Grammar(
    rule(E,[E,'+',E]),
    rule(E,['id']),
    )
lr = LR(g)
#print( g.alls )
#print( lr.Closure( [ item(g.first_rule.name,[],g.first_rule.body) ] ) )
#print( g.First(g.first_rule.name) , g.Follow(g.first_rule.name) )
#print( g.First(E) , g.Follow(E) )
#print( g.First(T) , g.Follow(T) )
inp = InputStream( ['id','+','id','+','id'] )
out = lr.parse(inp)
print( out )
inp1 = InputStream( ['id','+','id','+','id'] )
print( LR(g1).parse(inp1) )
inp2 = InputStream( ['id','+','id','+','id'] )
print( LR(g2).parse(inp2) )
