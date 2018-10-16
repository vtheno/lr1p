#coding=utf-8
class Lexical(object):
    def __init__(self,skips,spectab):
        self.skips = skips
        self.spectab = spectab
    def num(self,inp):
        temp = ''
        while inp and ('0' <= inp[0] <= '9'):
            temp += inp[0]
            inp = inp[1:]
        if temp:
            return temp,inp
    def alpha(self,inp):
        temp = ''
        while inp and ('a' <= inp[0] <= 'z' or 'A' <= inp[0] <= 'Z' or '0' <= inp[0] <= '9'):
            temp += inp[0]
            inp = inp[1:]
        if temp:
            return temp,inp
    def ops(self,inp):
        temp = '' + inp[0]
        inp = inp[1:]
        symbols = self.spectab.get(temp)
        while inp and symbols:
            if inp[0] == symbols[0]:
                temp += inp[0]
                symbols = symbols[1:]
                inp = inp[1:]
            else:
                break
        if temp:
            return temp,inp
    def lex(self,inp): # todo add position
        while inp:
            # print( f"inp => {inp!r}" )
            if inp[0] in self.skips:
                inp = inp[1:]
            elif '0' <= inp[0] <= '9':
                value = self.num(inp)
                if value:
                    out,inp = value
                    yield out
            elif 'a' <= inp[0] <= 'z' or 'A' <= inp[0] <= 'Z':
                value = self.alpha(inp)
                if value:
                    out,inp = value
                    yield out
            elif inp[0] in self.spectab.keys():
                value = self.ops(inp)
                if value:
                    out,inp = value
                    yield out
            else:
                out,inp = inp[0],inp[1:]
                yield out
__all__ = ["Lexical"]
"""
skips = [" ","\n","\t"]
spectab = {
    ":":[":"],
    "-":[">"],
}
lex = Lexical(skips,spectab)
print( list( lex.lex("(a::b) : int * int -> int") ) )
"""
