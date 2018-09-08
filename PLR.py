#coding=utf-8
from util import *
class InputStream(object):
    slst : [str]
    def __init__(self,string):
        assert list(string) != [] ,"InputString Empty"
        self.slst = list(string) + [EOF]
        self.position = 0
        self.current = self.slst[self.position]
    def end_of(self):
        return self.current == EOF
    def next(self):
        self.position += 1
        self.current = self.slst[self.position]
I = InputStream
class Symbol(type):
    def __new__(cls,name,parents,attrs):
        attrs["__name__"] = name
        attrs["__repr__"] = lambda self:self.__name__
        return type.__new__(cls,name,parents,attrs)
def newSymbol(name):
    return Symbol(name,(),{})()
def newSymbols(*names):
    return tuple([newSymbol(name) for name in names])
class Rule(object):
    def __init__(self,L,R,pos=0):
        self.L = L
        self.R = R
        self.pos = pos
        self.max = len(self.R)
        self.cur = self.R[self.pos] if self.pos < self.max else EOF
    def __eq__(self,obj):
        #print( "eq_obj:",self,'==',obj )
        return self.L == obj.L and self.R == obj.R and self.pos == obj.pos and self.cur == obj.cur and self.max == obj.max
    def __repr__(self):
        rs = [ ]
        for ri in range(len(self.R)):
            if ri == self.pos:
                rs += ["."]
            rs += [repr(self.R[ri])]
        R = ''.join(rs)
        if self.end_of():
            R +='.'
        return f"{self.L} -> {R}"
    def __iter__(self):
        yield self.L
        yield self.R
    def next(self):
        if self.pos < self.max:
            return Rule(self.L,self.R,self.pos + 1)
        return Rule(self.L,self.R,self.pos)
    def end_of(self):
        return self.pos == self.max
    def prefixes(self,X):
        return self.cur == X
class Grammar(object):
    def __init__(self,*rule_tup):
        rule_tup = list(rule_tup)
        first = rule_tup[0][0]
        G = newSymbol(first.__name__ + "'")
        self.first = Rule(G,[first],0)
        #print( self.first.L )
        self.rules = [self.first] + [Rule(*r) for r in rule_tup]
        self.all_symbols = self.all_symbol()
        self.all_tokens = self.all_token()
        self.alls = self.all_symbols + self.all_tokens
        #self.alls = [i for i in self.alls if i!=self.first]
    def all_symbol(self):
        out = [ ]
        for rule in self.rules:
            L,R = rule
            out += [i for i in [L] + R if type(i).__class__ is Symbol]
        return list(set(out))
    def all_token(self):
        out = [ ]
        for rule in self.rules:
            L,R = rule
            out += [i for i in [L] + R if not type(i).__class__ is Symbol]
        return list(set(out))
    def __repr__(self):
        return repr(self.rules)
Id,E,T = newSymbols("Id","E","T")
G = Grammar( (E,[T,'+',E]),
             (E,[T]),
             (T,['id']),)
class ButtomUpParser(object):
    def __init__(self,grammar,inp):
        self.grammar = grammar
        self.inp = inp
        self.Stack = Stack(256 * 256)
        self.Stack.push( 0 )
    def parse(self):
        token = self.inp.current
        state = (self.stack.peek()).n
        action = self.action[state][token]
        if isinstance(action,SHIFT):
            si = action
            self.Stack.push(token)
            self.Stack.push(si)
            self.inp.next()
        elif isinstance(action,REDUCE):
            rule_index = action.n
            rule = self.rules.get(rule_index + 1)
            (A,body) = rule
            length = len(body)
            popn = self.Stack.popn( length + length )
            state = self.Stack.peek()
            self.Stack.push( A )
            self.Stack.push( self.goto[state.n][A] )
        elif action == ACCEPT:
            state,result = self.Stack.popn(2)
            return result
        else:
            #action == REJECT
            raise TypeError("{}".format(action))
    def Closure_LR0(self,I):
        I = list(I)
        while 1:
            new_item = False
            for item in I:
                if item.end_of():
                    continue
                Y = item.cur
                #print( Y )
                for prod in self.grammar.rules:
                    if prod.L != Y:
                        continue
                    if prod not in I:
                        I += [prod]
                        new_item = True
            if new_item == False:
                break
        return I
    def Goto_LR0(self,I,X):
        J = [ ]
        for i in I:
            if i.prefixes(X):
                next_i = i.next()
                if next_i not in J:
                    J += [ next_i ]
        out = self.Closure_LR0(J)
        return out
    def Items_LR0(self):
        C = self.Closure_LR0( [self.grammar.first] )
        Items = [ C ]
        Todo = [ C ]
        taginfos = [ ]
        while Todo:
            Si = Todo.pop()
            #print( self.grammar.alls )
            taginfo = [ ]
            for X in self.grammar.alls:
                t = self.Goto_LR0(Si,X)
                if t and t not in Items:
                    #print( {X:t},Si )
                    Items += [t]
                    Todo += [t]
                    taginfo.append( {X : [Items.index(Si),'to',Items.index(t)]} )
            if taginfo:
                taginfos +=[taginfo]
            #print( "s1:",x )
        return Items,taginfos
    def Construct_table(self):
        self.action = [ ]
        self.goto = [ ]
        items,taginfos = self.Items_LR0()
        infos = [ ]
        for item in items:
            temp = [ ]
            for c in item:
                t = {items.index(item) : c.cur}
                if t not in temp:
                    temp += [t]
            infos += [temp]
            print( temp )
        for taginfo in taginfos:
            print( taginfo )
b = ButtomUpParser(G,[])
print( "--------------------" )
print( G )
print( G.all_symbols )
print( G.all_tokens )
print( "--------------------" )
#i1 = b.Closure_LR0( [ G.first ] )
#print( i1 )
#print( b.Goto_LR0(i1,'id') )
items,_ =  b.Items_LR0()
for i in range(len(items)):
    print( f"S{i}:",items[i] )
print( "--------------------" )
b.Construct_table()
print( "--------------------" )
