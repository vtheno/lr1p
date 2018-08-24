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
    def __init__(self,L,R,cur=0):
        self.L = L
        self.R = R
        self.cur = cur
        self.max = len(R)
    def next(self):
        if self.cur < self.max :
            return rule(self.L,self.R,self.cur + 1)
        else:
            raise EOFError
    def end_of(self):
        return self.cur == self.max
    def __repr__(self):
        dot = type('dot',(object,),{'__repr__':lambda self:'.'})()
        tmp = self.R[0:self.cur] + [dot] + self.R[self.cur:]
        return "{} -> {}".format(self.L, ' '.join([repr(x) for x in tmp]))
    def inference(self,accept):
        #tmp = self.next()
        if self.end_of():
            if self.L == accept:
                return ('A',self.L)
            return ('R',self.L)
        else:
            return ('S',self.R[self.cur])
class BottomUp(object):
    def __init__(self,
                 G : [(object,[object])],
                 I : InputStream,
                 action : [{object:object}],
                 goto : [{object:object}] ):
        tmp = G[0].L
        r1 = rule(New("{}'".format(tmp)),[tmp])
        self.Rules = [r1] + G
        self.GeneratorItem( self.Rules, r1.L )
        self.Input = I
        self.Stack = Stack()
        self.Stack.push( SHIFT(0) )
        self.action = action # [{}] table
        self.goto = goto     # [{}] table
    def infos(self):
        ls = [r.L for r in self.Rules]
        rs = set([EOF])
        for r in self.Rules:
            for x in r.R:
                if repr(x) == 'ID':
                    rs.add( IDK )
                elif x not in ls:
                    rs.add( x )
        goto_header = set(ls)
        action_header = rs
        return action_header,goto_header
    def GeneratorItem(self,rules,accept):
        items = [rules]
        tmp = rules
        while tmp:
            ttt = [i.inference(accept) for i in tmp]
            print( "In :",tmp )
            print( "Out:",ttt )
            tmp = [i.next() for i in tmp if not i.end_of()]

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
           "rule",
           "BottomUp"]
