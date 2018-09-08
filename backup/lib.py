#coding=utf-8
class ACTION(type):
    def __new__(cls,name,parents,attrs):
        attrs["__name__"] = name
        attrs["__init__"] = lambda self,n:setattr(self,'n',n)
        attrs["__repr__"] = lambda self:"{}{}".format(self.__name__,getattr(self,"n"))
        return type.__new__(cls,name,parents,attrs)
class SHIFT(metaclass=ACTION): pass
class REDUCE(metaclass=ACTION): pass
class ACCEPT(metaclass=ACTION): pass
class REJECT(metaclass=ACTION): pass
Accept = ACCEPT(0)
Reject = REJECT(0)
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
        return len(self.items) == 0
    def __repr__(self):
        return repr(self.items[0:self.top])
EOF = type("EOF",(object,),{"__repr__":lambda self:"EOF"})()
EmptyStream = type("EmptyStream",(Exception,),{"__repr__":lambda self:"EmptyStream"})
class InputStream(object):
    def __init__(self, stream):
        if stream == [ ]:
            raise EmptyStream
        self.stream = stream
        self.stream.append( EOF )
        self.stream_point = 0
        self.current = self.stream[self.stream_point]
    def next(self):
        self.stream_point += 1
        self.current = self.stream[self.stream_point]
        return self.stream[self.stream_point]
    def stream_end(self):
        if self.stream[self.stream_point] == EOF:
            return True
        else:
            return False

__all__ = ["Accept","Reject","SHIFT","REDUCE","ACCEPT","REJECT",
           "ACTION",
           "Stack",
           "EOF",
           "InputStream"]
