#coding=utf-8
from LR import *
from lib import SHIFT,REDUCE,Reject,Accept,EOF,InputStream

E = New("E")
keywords = ['+',]
ID = mkID(keywords)
G = [
    (E,[E,'+',E]),
    (E,[E,'*',E]),
    (E,[ID]),
]
action = [ ]
goto = [ ]
inp = ["a",'+','b']
bt = BottomUp(G,inp,action,goto)
print( bt.search_action() )
