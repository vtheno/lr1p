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
        self.first_op = {}
        self.last_op = {}
        self.init_op_set()
        self.compute_first_op()
        self.compute_last_op()
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

    def init_op_set(self):
        for lhs in self.Vn:
            self.first_op[lhs] = [ ]
            self.last_op[lhs] = [ ]

    def first_op_point(self,lhs,rhs):
        i,l,out = 0,len(rhs),[]
        start = rhs[i]
        if isinstance(start,Vt):
            value = [i for i in [start] if i not in self.first_op[lhs]]
            if value:
                out += value
        elif isinstance(start,Vn):
            value = [i for i in [start] if i not in self.first_op[lhs]]
            if value:
                out += value
            if i + 1 < l:
                i += 1
                start = rhs[i]
                value = [i for i in [start] if i not in self.first_op[lhs]]
                if value:
                    out += value
        return out

    def compute_first_op(self):
        changed = True
        while changed:
            changed = False
            for lhs,rhs in self.R:
                value = [i for i in self.first_op_point(lhs,rhs) if i not in self.first_op[lhs]]
                if value:
                    self.first_op[lhs] += value
                    changed = True
        changed = True
        while changed:
            changed = False
            for lhs,ops in self.first_op.items():
                for op in ops:
                    if isinstance(op,Vn):
                        value = [i for i in self.first_op[op] if i not in self.first_op[lhs] and i!=op]
                        if value:
                            value = [i for i in self.first_op[lhs] + value if i!=op]
                            if value:
                                self.first_op[lhs] = value
                                changed = True
        for lhs,ops in self.first_op.items():
            self.first_op[lhs] = [i for i in self.first_op[lhs] if not isinstance(i,Vn)]

    def last_op_point(self,lhs,rhs):
        l,out = len(rhs),[]
        i = l - 1
        start = rhs[i]
        if isinstance(start,Vt):
            value = [i for i in [start] if i not in self.last_op[lhs]]
            if value:
                out += value
        elif isinstance(start,Vn):
            value = [i for i in [start] if i not in self.last_op[lhs]]
            if value:
                out += value
            if i > 1:
                i -= 1
                start = rhs[i]
                value = [i for i in [start] if i not in self.last_op[lhs]]
                if value:
                    out += value
        return out

    def compute_last_op(self):
        changed = True
        while changed:
            changed = False
            for lhs,rhs in self.R:
                value = [i for i in self.last_op_point(lhs,rhs) if i not in self.last_op[lhs]]
                if value:
                    self.last_op[lhs] += value
                    changed = True
        changed = True
        while changed:
            changed = False
            for lhs,ops in self.last_op.items():
                for op in ops:
                    if isinstance(op,Vn):
                        value = [i for i in self.last_op[op] if i not in self.last_op[lhs] and i!=op]
                        if value:
                            value = [i for i in self.last_op[lhs] + value if i!=op]
                            if value:
                                self.last_op[lhs] = value
                                changed = True
        for lhs,ops in self.last_op.items():
            self.last_op[lhs] = [i for i in self.last_op[lhs] if not isinstance(i,Vn)]        

__all__ = ["Vn","Vt","bottom","eof","Grammar","rule"]
