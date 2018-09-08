#coding=utf-8
from LR import *
from lib import SHIFT,REDUCE,Reject,Accept,EOF,InputStream
E,Int = News("E","Int")
G = [
    rule(E,[E,'+',E]),
    rule(E,[Int])
]
action = [ 
    {Int : SHIFT(3) , '+' : Reject , EOF : Reject , },
    {Int : Reject , '+' : SHIFT(2) , EOF : Accept , },
    {Int : SHIFT(4) , '+' : Reject , EOF : Reject , },
    {Int : Reject , '+' : REDUCE(1)  , EOF : REDUCE(1) },
    {Int : Reject , '+' : REDUCE(1) , EOF : REDUCE(1) },
    {Int : Reject , '+' : REDUCE(0) , EOF : REDUCE(0) },
]
goto = [
    {E : SHIFT(1) },
    {E : Reject },
    {E : SHIFT(5) },
    {E : Reject },
    {E : Reject },
    {E : Reject },
]
inp = InputStream( [Int,'+',Int,'+',Int,'+',Int] )
bt = BottomUp(G,inp,action,goto)
print( bt.parse() )
