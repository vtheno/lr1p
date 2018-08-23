#coding=utf-8
from LR import *
from lib import SHIFT,REDUCE,Reject,Accept,EOF,InputStream
keywords = [ ]
A,B,S = News("A","B","S")
G = [
    (S,[A,B]),
    (A,['a']),
    (B,['b']),
    ]
"""
Grammar:
    S -> AB
    A -> a
    B -> b
"""
ID = mkID(keywords)
action = [ 
    { # 0
        'a':SHIFT(3),
        'b':Reject,
        EOF:Reject,
    },
    { # 1
        'a':Reject,
        'b':Reject,
        EOF:Accept,
    },
    { # 2
        'a':Reject,
        'b':SHIFT(5),
        EOF:Reject,
    },
    { # 3
        'a':REDUCE(1),
        'b':REDUCE(1),
        EOF:REDUCE(1),
    },
    { # 4
        'a':REDUCE(0),
        'b':REDUCE(0),
        EOF:REDUCE(0),
    },
    { # 5
        'a':REDUCE(2),
        'b':REDUCE(2),
        EOF:REDUCE(2),
    },
]
goto = [
    { #0
        S:SHIFT(1),
        A:SHIFT(2),
        B:Reject,
    },
    { #1
        S:Reject,
        A:Reject,
        B:Reject,
    },
    { #2
        S:Reject,
        A:Reject,
        B:SHIFT(4),
    },
    { #3
        S:Reject,
        A:Reject,
        B:Reject,
    },
    { #4
        S:Reject,
        A:Reject,
        B:Reject,
    },
    { #5
        S:Reject,
        A:Reject,
        B:Reject,
    },

]
inp = InputStream(["a","b"])
BT = BottomUp(G,inp,action,goto)
BT.search_action()
#print( BT.parse() )
