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
        if self.end_of():
            if self.L == accept:
                return (EOF,Accept,self)
            else:
                return (EOF,REDUCE(-1),self)
        else:
            return ( self.R[self.cur] ,SHIFT(-1),self)
class BottomUp(object):
    def __init__(self,
                 G : [(object,[object])],
                 I : InputStream,
                 action : [{object:object}],
                 goto : [{object:object}] ):
        tmp = G[0].L
        self.accept = rule(New("{}'".format(tmp)),[tmp])
        self.Rules = [self.accept] + G
        self.Input = I
        self.Stack = Stack()
        self.Stack.push( SHIFT(0) )
        self.action = [None] # [{}] table
        self.goto = [None]     # [{}] table
        self.infos()
        self.GeneratorItem( self.Rules )
    def index(self,rul):
        n = 0
        for r in self.Rules:
            if r.L == rul.L and r.R == rul.R:
                return n
            else:
                n+=1
        else:
            return IndexError

    def infos(self):
        ls = [r.L for r in self.Rules]
        rs = set([EOF])
        for r in self.Rules:
            for x in r.R:
                if repr(x) == 'ID':
                    rs.add( IDK )
                elif x not in ls:
                    rs.add( x )
                else:
                    continue
        self.goto_header = list(set(ls))
        self.action_header = list(rs)
    def toTable(self,lst,n):
        print( "ToTable:",len(lst))
        for l in lst :
            target,state,rul = l
            target = IDK if repr(target) == 'ID' else target
            if isinstance(state,SHIFT):
                cur_state = SHIFT(n + 1)
            elif isinstance(state,REDUCE):
                cur_state = REDUCE( self.index( rul ) )
            else:
                cur_state = state
            if rul.end_of():
                self.action[n][EOF] = cur_state
                #print( "eof table:",n,target,cur_state,rul)
            else:
                if target in self.goto_header:
                    #print( "goto table:",n,target,cur_state,rul )
                    self.goto[n][target] = cur_state
                else:
                    #print( "action table:",n,target,cur_state,rul )
                    self.action[n][target] = cur_state
            
    def GeneratorItem(self,rules):
        tmp = rules[1:]
        n = 0
        while tmp:
            self.goto[n] = {k:v for k,v in zip(self.goto_header,[Reject] * len(self.goto_header))}
            self.action[n] = {k:v for k,v in zip(self.action_header,[Reject] * len(self.action_header))}
            targets = [i.inference(self.accept) for i in tmp]
            print( targets )
            #self.toTable(targets,n)
            tmp = [i.next() for i in tmp if not i.end_of()]
            n += 1
            self.goto += [None]
            self.action += [None]
            #self.append( )
        self.goto.pop()
        self.action.pop()
        pprint( self.goto )
        pprint( self.action )
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
                rul = self.Rules[rule_index]
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
