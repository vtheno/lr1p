#coding=utf-8
from lib import *
from LR import *
E = New("E")
T = New("T")
ID = mkID(['+','*'])
G = [
    rule(E,[E,'+',T]),
    rule(E,[T]),
    rule(T,[ID]),
    ]
inp = ['a','+','b']
bt = BottomUp(G,inp,[],[])
