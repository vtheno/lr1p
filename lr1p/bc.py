from types import CodeType
from opcode import opmap
LOAD_ATTR = opmap["LOAD_ATTR"]
# attr is in names
# load find attrr call get
LOAD_CONST = opmap["LOAD_CONST"]
STORE_FAST = opmap["STORE_FAST"]
LOAD_FAST = opmap["LOAD_FAST"]
MAKE_FUNCTION = opmap["MAKE_FUNCTION"]
CALL_FUNCTION = opmap["CALL_FUNCTION"]
class ByteCode(object):
    def __init__(self):
        self.opec = []
        self.consts = []
        self.varnames = []
        self.names =[]
    def load_attr(self, name):
        if name not in self.names:
            self.names.append(name)
        self.opec +=  [LOAD_ATTR,self.names.index(name) ]
    def make_function(self, argc):
        self.opec += [MAKE_FUNCTION, argc]
    def call_function(self, argcount : int):
        self.opec += [CALL_FUNCTION, argcount]
    def load_const(self, val : object):
        if val not in self.consts:
            self.consts.append(val)
        self.opec += [LOAD_CONST,self.consts.index(val)]
    def store_fast (self, name : str):
        if name not in self.varnames:
            self.varnames.append(name)
        self.opec +=  [STORE_FAST,self.varnames.index(name) ]
    def load_fast (self, name : str):
        if name not in self.varnames:
            self.varnames.append(name)
        self.opec +=  [LOAD_FAST,self.varnames.index(name) ]
    def build (self):
        code = CodeType(0,
                        # argcount
                        0,
                        # kwonlyargcount
                        len(self.varnames),
                        # nlocals
                        2,
                        # stacksize
                        67,
                        # flags
                        bytes(self.opec),
                        # codestring
                        tuple(self.consts),
                        # consts
                        tuple(self.names),
                        # names
                        tuple(self.varnames),
                        # varnames
                        '<unknow>',
                        # filename
                        "<unknow>",
                        # name
                        1,
                        # firstlineno
                        b'',
                        # lnotab
                        tuple (),
                        # freevars
                        tuple (),
                        # cellvars
                    )
        return code
