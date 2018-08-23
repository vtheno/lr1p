#coding=utf-8
from lib import *
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
    def __init__(self,rule):
        self.L = rule[0]
        self.R = rule[1]
        self.cur = 0
        self.max = len(self.R)
    def __repr__(self):
        return "{} -> {}".format(repr(self.L),repr(self.R[0]) if len(self.R) == 1 else ''.join(map(lambda x:repr(x),self.R)))
    def reset(self):
        self.cur = 0
    def end_of(self):
        if self.cur == self.max:
            return True
        else:
            return False
class Process (object):
    def __init__(self,rules):
        self.rules = rules
    def first_find(self):
        first = self.rules[1]
        non_end = set([self.rules[0],first])
        for r in self.rules[2:]:
            if first.R.index(r.L) is 0:
                non_end.add(r)
        is_end = set(self.rules) - non_end
        return (is_end , non_end)
    def second_find(self):
        Rs = set([])
        Ls = set([l.L for l in self.rules[1:]])
        for r in self.rules:
            for t in r.R:
                Rs.add( t ) if repr(t) != 'ID' and t not in Ls else Rs.add(IDK)
        return (Ls,Rs)
class BottomUp(object):
    def __init__(self,G,I,action,goto):
        tmp = G[0][0]
        self.Rules = [(New(repr(tmp) + "'"),[tmp])] + G # Grammar
        self.rules = [rule(r) for r in self.Rules]
        self.process = Process(self.rules)
        self.Input = I # InputSteam
        self.Stack = Stack()
        self.Stack.push( SHIFT(0) )
        self.action = action # [{}] table
        self.goto = goto     # [{}] table
    def search_action(self):
        # from the rule generate action table ???
        for rule in self.rules:
            print( rule )
        is_end,non_end = self.process.first_find ()
        goto,action = self.process.second_find ()
        print( is_end,non_end , goto,action )
        # wait
    def search_goto(self):
        pass
    def get_action(self,state,token):
        tab = self.action[state]
        f = type('f',(object,),{})()
        val = tab.get(token,f)
        return val if val !=f else tab[IDK]
    def parse(self):
        while 1: # repeat
            token = self.Input.current
            state = (self.Stack.peek()).n
            action = self.get_action(state,token)
            print( "current:",action,token,self.Stack.peek(),self.Stack)
            if isinstance(action,SHIFT):
                si = action
                self.Stack.push(token)
                self.Stack.push(si)
                self.Input.next()
            elif isinstance(action,REDUCE):
                rule_index = action.n
                (A,body) = self.Rules[rule_index]
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
           "BottomUp"]
