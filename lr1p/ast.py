def general_init(self, **kws):
    items = kws.items ()
    count = len( items )
    if count != len(self._fields):
        raise TypeError
    for f,(k,v) in zip(self._fields, items):
        if f == k:
            setattr(self, f,v)
        else:
            raise TypeError
def general_repr(self):
    val = []
    for field in self._fields:
        value = getattr(self, field)
        val += [f"{field} = {value}"]
    val = ", ".join( val )
    return f"{{ {self._name} : {val} }}"
def general_equal(self,other):
    if hasattr(other,"_fields"):
        _fields = getattr(other,"_fields")
        if all([hasattr(other,i) for i in _fields]):
            val1 = [getattr(self, field) for field in self._fields]
            val2 = [getattr(other, field) for field in other._fields]
            return val1 == val2
        return False
    return False
class AST(type):
    def __new__(cls, name, bases, attrs):
        attrs["_name"] = name
        fields = attrs.get("_fields",[])
        attrs["__init__"] = general_init
        attrs["__repr__"] = general_repr
        attrs["__eq__"] = general_equal
        return type.__new__(cls, name, bases, attrs)
class Transfer(object):
    def match(self, ast):
        name = ast._name
        def add(fn):
            setattr (self,f"{name}_visit",fn)
            return self.visit
        return add
    def visit(self,node : {str:list}, ctx):
        name = node._name
        visit = getattr (self, f"{name}_visit", None)
        if visit:
            return visit (self, node, ctx)
        return self.general_visit (node, ctx)
    def general_visit (self, node, ctx):
        construct = type(node)
        name = node._name
        vals = [ ]
        for field in node._fields:
            val = getattr(node, field)
            if type(type(val)) is AST:
                val = self.visit(val, ctx)
            vals += [(field,val)]
        vals = dict(vals)
        return construct(**vals)

__all__ = ["AST","Transfer"]
