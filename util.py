#coding=utf-8
StackOverflow = type("StackOverflow",(Exception,),{"__repr__":lambda self:"StackOverflow"})
class Stack(object):
    def __init__(self,size=256):
        self.items = [None] * size
        self.top = 0
        self.stack_size = size
    def push(self, item):
        if self.stack_size >= self.top:
            self.items[self.top] = item
            self.top += 1
            return self.top
        else:
            raise StackOverflow
    def pop(self):
        self.top -= 1
        val = self.items[self.top]
        self.items[self.top] = None
        return val
    def popn(self, n):
        return [self.pop() for i in range(n)]
    def peek(self):
        return self.items[self.top - 1]
    def empty(self):
        return self.top is 0
    def __repr__(self):
        return repr(self.items[0:self.top])
EOF = type("EOF",(object,),{"__repr__":lambda self:"EOF"})()
class ACTION(type):
    def __new__(cls,name,parents,attrs):
        attrs["__name__"] = name
        attrs["__init__"] = lambda self,n:setattr(self,'n',n)
        if "__repr__" not in attrs.keys():
            attrs["__repr__"] = lambda self:"{}{}".format(self.__name__[0],getattr(self,"n"))
        return type.__new__(cls,name,parents,attrs)
class SHIFT(metaclass=ACTION): pass
class REDUCE(metaclass=ACTION): pass
class ACCEPT(metaclass=ACTION): pass
class REJECT(metaclass=ACTION):
    def __repr__(self):
        return "--"
ACCEPT = ACCEPT(0)
REJECT = REJECT(0)
class InputStream(object):
    slst : [str]
    def __init__(self,string):
        assert list(string) != [] ,"InputString Empty"
        self.slst = list(string) + [EOF]
        self.position = 0
        self.current = self.slst[self.position]
    def end_of(self):
        return self.current == EOF
    def next(self):
        self.position += 1
        self.current = self.slst[self.position]
__all__ = ["Stack","StackOverflow","InputStream",
           "EOF",
           "ACTION",
           "ACCEPT","SHIFT","REDUCE","REJECT"]
           
