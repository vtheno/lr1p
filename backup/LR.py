#coding=utf-8
from lib import *
from pprint import pprint
def New(name):
    value = type(name,(object,),{"__repr__":lambda self:name})()
    return value
def News(*names):
    return [New(name) for name in names]
def mkID(keywords):
    return type("ID",(object,),{"__repr__":lambda self:"ID",
                                "__keywords__":keywords,
                                "__eq__":lambda self,other:other !=EOF and other not in self.__keywords__})()
IDK = type("IDK",(object,),{"__repr__":lambda self:"IDK"})()
RejectErr = type("RejectErr",(Exception,),{"__repr__":lambda self:"RejectErr"})
class rule(object):
    def __init__(self,L,R,cur=0):
        self.L = L
        self.R = R
        self.cur = cur
        self.max = len(R)
    def next(self):
        return rule(self.L,self.R,self.cur if self.max == self.cur else self.cur + 1)
    def end_of(self):
        return self.cur == self.max
    def __repr__(self):
        dot = type('dot',(object,),{'__repr__':lambda self:'.'})()
        tmp = self.R[0:self.cur] + [dot] + self.R[self.cur:]
        return "{} -> {}".format(self.L, ' '.join([repr(x) for x in tmp]))
class BottomUp(object):
    def __init__(self,
                 G : [(object,[object])],
                 I : InputStream,
                 action : [{object:object}],
                 goto : [{object:object}] ):
        tmp = G[0].L
        self.accept = rule(New(f"{tmp}'"),[tmp])
        self.Rules = [self.accept] + G
        self.Input = I
        self.Stack = Stack()
        self.Stack.push( SHIFT(0) )
        self.action = action
        self.goto = goto
        self.init()
        
    def Closure(self,item):
        items = [item]
        while 1:
            flag = 0
            for i in items:
                if i.end_of():
                    continue
                Y = i.R[0]
                for p in self.Rules:
                    if p.L != Y:
                        continue
                    if p not in items:
                        items += [ p ]
                        flag = 1
            if flag==0:
                break
        return items
    def init(self):
        self.notToken = list(set([ l.L for l in self.Rules ]))
        isToken = [EOF]
        for r in self.Rules:
            isToken += [i for i in  r.R if i not in self.notToken ]
        self.isToken = list(set(isToken))
        print( self.first( '+' ) )
    def first(self,symbol):
        if symbol in self.isToken:
            return [ symbol ]
        fail = [ ]
        for rule in self.Rules:
            if rule.L == symbol and rule.R[0] != symbol:
                if rule.L in self.isToken:
                    fail += [symbol]
        return fail
    def gt(self,Set,symbol):
        gotoSet = [ ];
        for i in range(len(self.Rules)):
            if Set[i].R[Set[i].cur] == symbol:
                gotoSet += [ {  } ]
    def get_action(self,state,token):
        tab = self.action[state]
        f = type('f',(object,),{})()
        val = tab.get(token,f)
        return val if val !=f else tab[IDK]
    def parse(self):
        while 1: # repeat
            token = self.Input.current
            state = (self.Stack.peek()).n
            action = self.action[state][token]
            print( "current:",token,action,self.Stack)
            if isinstance(action,SHIFT):
                si = action
                self.Stack.push(token)
                self.Stack.push(si)
                self.Input.next()
            elif isinstance(action,REDUCE):
                rule_index = action.n
                rul = self.Rules[rule_index + 1]
                print( 'reduce: ',rul )
                (A,body) = (rul.L,rul.R)
                length = len(body)
                popn = self.Stack.popn( length + length )
                state = self.Stack.peek()
                self.Stack.push( A )
                self.Stack.push( self.goto[state.n][A] )
            elif isinstance(action,ACCEPT):
                state,result = self.Stack.popn(2)
                return result
            elif isinstance(action,REJECT):
                raise RejectErr("{}".format(action))

__all__ = ["New","News",
           "mkID","IDK",
           "rule",
           "BottomUp"]
