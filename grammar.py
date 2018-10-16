#coding=utf-8
from collections import namedtuple
from util import *

class Vn(metaclass=Symbol): pass 
class Vt(metaclass=Symbol): pass 
@call('..')
class bottom(metaclass=Symbol): pass
@call('$')
class eof(metaclass=Symbol): pass

rule = namedtuple('rule',['lhs','rhs'])
rule.__repr__ = lambda self :f"{self.lhs} -> {' '.join([repr(i) for i in self.rhs])}"

class Grammar(object):
    def __init__(self,g):
        self.R = g
        self.Vn = [ ] # V non-terminator
        self.Vt = [ ] # E terminator
        self.S = self.R[0][0]
        self.calc()
        self.first_set = {}
        self.follow_set = {}
        self.nullable_set = {}
        self.init_set()
        self.compute_nullable()
        self.compute_first() 
        self.compute_follow()

    def calc(self):
        for left,right in self.R:
            value = [i for i in [left] if isinstance(i,Vn) and i not in self.Vn]
            if value:
                self.Vn += value
            value = [i for i in right if isinstance(i,Vn) and i not in self.Vn]
            if value:
                self.Vn += value
            value = [i for i in [left] if isinstance(i,Vt) and i not in self.Vt]
            if value:
                self.Vt += value
            value = [i for i in right if isinstance(i,Vt) and i not in self.Vt]
            if value:
                self.Vt += value

    def init_set(self):
        self.nullable_set[bottom] = True
        self.nullable_set[eof] = True
        self.first_set[bottom] = [bottom]
        self.first_set[eof] = [eof]
        V = self.Vn + self.Vt
        for x in V:
            self.nullable_set[x] = False
            if isinstance(x,Vt):
                self.first_set[x] = [x]
            elif isinstance(x,Vn):
                self.first_set[x] = [ ]
                self.follow_set[x] = [ ]
        self.follow_set[self.S] = [eof]
 
    def sum(self,lst:[[...]]):
        out = [ ]
        for i in lst:
            value = [x for x in i if x not in out]
            if value:
                out += value
        return out

    def null_point(self,lst:[...]):
        flag = True if self.nullable_set[lst[0]] else False
        for i in lst[1:]:
            if flag:
                flag = self.nullable_set[i]
            else:
                break
        return flag

    def compute_nullable(self):
        changed = True
        while changed:
            changed = False
            for x in self.Vn:
                for lhs,rhs in self.R:
                    if lhs == x:
                        value = self.null_point(rhs)
                        if value and value != self.nullable_set[lhs]:
                            self.nullable_set[lhs] = value
                            changed = True
        
    def first_point(self,lst:[...]):
        i,l = 0,len(lst)
        current = lst[i]
        first_x = [i for i in self.first_set[current]]
        changed = True
        while changed and i < l - 1 and self.nullable_set[current]:
            changed = False
            i += 1
            current = lst[i]
            value = [i for i in self.first_set[current] if i not in first_x]
            if value:
                first_x += value
                changed = True
        return first_x

    def compute_first(self):
        changed = True
        while changed:
            changed = False
            for x in self.Vn:
                value = self.sum([self.first_point(y) for X,y in self.R if X == x])
                #print( x,"=>",value )
                if value and value!= self.first_set[x]:
                    self.first_set[x] = value
                    changed = True

    def follow_point(self,x,name,lst:[...]):
        idx,l = lst.index(x),len(lst)
        if idx + 1 < l:
            lst = lst[idx+1:]
        else:
            return [i for i in self.follow_set[name]]
        i,l = 0,len(lst)
        current = lst[i]
        follow_x = [i for i in self.first_set[current] if i!= bottom]
        changed = True
        while changed and i < l - 1 and self.nullable_set[current] :
            changed = False
            i += 1
            current = lst[i]
            value = [i for i in self.first_set[current] if i not in first_x]
            if value:
                follow_x += value
                changed = True
        else:
            value = [i for i in self.follow_set[name] if i not in follow_x]
            if value:
                follow_x += value
                changed = True
        return follow_x

    def compute_follow(self):
        changed = True
        while changed:
            changed = False
            for x in self.Vn:
                value = self.sum([self.follow_point(x,lhs,rhs) for lhs,rhs in self.R if x in rhs])
                if value and value != self.follow_set[x]:
                    self.follow_set[x] = value
                    changed = True

__all__ = ["Vn","Vt","bottom","eof","Grammar","rule"]
