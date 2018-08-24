#coding=utf-8
from LR import *
from lib import SHIFT,REDUCE,Reject,Accept,EOF,InputStream

A,B = News("A","B")
#keywords = ['+',]
#ID = mkID(keywords)
G = [
    (A,['0',A,'1']),
    (A,[B]),
    (B,['#']),
]
action = [ ]
goto = [ ]
inp = [ ]
bt = BottomUp(G,inp,action,goto)
print( bt.search_action() )

