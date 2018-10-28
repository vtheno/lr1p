#coding=utf-8
class Lexical(object):
    def __init__(self,skips):
        self.skips = skips
        self.inp = None
        self.pos = 0
    def move(self):
        self.pos += 1
    def num(self,inp):
        temp = ''
        while inp and ('0' <= inp[0] <= '9'):
            temp += inp[0]
            inp = inp[1:]
            self.move()
        if temp:
            return temp,inp
    def alpha(self,inp):
        temp = ''
        while inp and ('a' <= inp[0] <= 'z' or 'A' <= inp[0] <= 'Z' or '0' <= inp[0] <= '9'):
            temp += inp[0]
            inp = inp[1:]
            self.move()
        if temp:
            return temp,inp
    def ops(self,inp):
        temp = ''
        while inp and inp[0] in """`!@#$%^&?{}[]_"'~<>+-*/|\,.:;()=""":
            temp += inp[0]
            inp = inp[1:]
            self.move()
        if temp:
            return temp,inp
    def lex(self,inp): # todo add position
        self.inp = inp
        self.pos = 0
        while inp:
            # print( f"inp => {inp!r}" )
            if inp[0] in self.skips:
                inp = inp[1:]
                self.move()
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
            elif inp[0] in """`!@#$%^&?{}[]_"'~<>+-*/|\,.:;()=""":
                value = self.ops(inp)
                if value:
                    out,inp = value
                    yield out
            else:
                out,inp = inp[0],inp[1:]
                self.move()
                yield out
__all__ = ["Lexical"]
