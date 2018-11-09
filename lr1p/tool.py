#coding=utf-8
def inf(stop=None,step=1,start=0):
    n = start
    while stop is None or n < stop:
        yield n
        n += step
def alpha(stop=None,step=1,start=0,Format=lambda n:f'alpha{n}'):
    n = start
    while stop is None or n < stop:
        yield Format(n)
        n += step

def inf_map (func,inf):
    """
    fun map func (x::xs) = [func(x)] :: map func xs
      | map func nil     = nil
    """
    for val in inf:
        yield func(val)
def inf_filter (func,inf):
    """
    fun filter func (x::xs) = if func(x) then [x] :: filter func xs else filter func xs
      | filter func nil     = nil
    """
    for val in inf:
        if func(val):
            yield val
def inf_zip (inf1,inf2):
    """
    fun zip (x::xs) (y::ys) = [(x,y)] :: zip ys xs
      | zip (x::xs) nil     = nil
      | zip nil     (y::ys) = nil
      | zip nil     nil     = nil
    """
    while 1:
        try:
            yield next(inf1),next(inf2)
        except StopIteration:
            break
def inf_take(inf,n:int):
    while n:
        yield next(inf)
        n-=1

def vzip( lst1 , lst2 ):
    """
    fun zip (x::xs) (y::ys) = [(x,y)] :: zip ys xs
      | zip (x::xs) nil     = nil
      | zip nil     (y::ys) = nil
      | zip nil     nil     = nil
    """
    l1 = iter(lst1)
    l2 = iter(lst2)
    while 1:
        try:
            yield next(l1),next(l2)
        except StopIteration:
            break
def enum ( l : list ) -> zip:
    return zip(inf(step=1),l)

def chunks (l:list,n:int) -> list:
    return [l[i:i+n] for i,_ in zip(inf(step=n),l) if l[i:i+n] != [] ]

def unchunks (l:[list]) -> list:
    return [i for j in l for i in j]

__all__ = ["inf","alpha","inf_map","inf_filter","inf_zip","inf_take",
           "vzip","enum",
           "chunks","unchunks"]
