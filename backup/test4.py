#coding=utf-8
from LR import *
from lib import SHIFT,REDUCE,Reject,Accept,EOF,InputStream

S,A,B = News("S","A","B")
#keywords = ['+',]
#ID = mkID(keywords)
G = [
    (S,[A,'c',B]),
    (A,['a',A]),
    (A,['a']),
    (B,['b',B]),
    (B,['b']),
]
"""
S -> AcB
A -> aA | a
B -> bB | b
"""
action = [ ]
goto = [ ]
inp = [ ]
bt = BottomUp(G,inp,action,goto)
print( bt.search_action() )
