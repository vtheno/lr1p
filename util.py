#coding=utf-8
class StackError(Exception): pass
class Stack(object):
    def __init__(self,size=256):
        self.size = size
        self.items = [None] * size
        self.top = 0

    def push(self,val):
        if self.top < self.size:
            self.items[self.top] = val
            self.top += 1
            return self.top
        else:
            raise StackError(f"push {self.top} greate stack size {self.size}")

    def pop(self):
        if self.top > 0:
            self.top -= 1
            val = self.items[self.top]
            self.items[self.top] = None
            return val
        else:
            raise StackError(f"pop Empty")

    def peek (self):
        return self.items[self.top - 1]

    def __repr__(self):
        return f"{[i for i in self.items if i!=None]}"

def call(*args,**kws):
    def warp(fn):
        return fn(*args,**kws)
    return warp

def define(obj):
    """
    define => rewrite to <name> = obj_warp
    obj_warp => rewrite def <name> or class <name> delcare to <name> = warp
    warp => rewrite to obj(*args,**kws)
    """
    def obj_warp(fn):
        def warp(*args,**kws):
            return obj(*args,**kws)
        return warp
    return obj_warp

class Symbol(type):
    def __new__(cls,name,bases,attrs):
        attrs["__name__"] = name
        attrs["__init__"] = lambda self,sym:setattr(self,"sym",sym)
        attrs["__repr__"] = lambda self:f"{self.sym!r}({self.__name__})"
        return type.__new__(cls,name,bases,attrs)

__all__ = ["call","define","Symbol","Stack"]
