KEYWORDS = ["OR", "NOT", "AND"]


class SQLConditional:
    def __init__(self, expr):
        self.expr = expr

    def AND(self, other):
        if type(self) != type(other):
            raise TypeError("Not an SQLCondition")
        if other._is_compound:
            expr = self.expr + f" AND ({other.expr})"
        else:
            expr = self.expr + f" AND {other.expr}"
        return type(self)(expr)

    def OR(self, other):
        if type(self) != type(other):
            raise TypeError("Not an SQLCondition")
        if other._is_compound:
            expr = self.expr + f" OR ({other.expr})"
        else:
            expr = self.expr + f" OR {other.expr}"
        return type(self)(expr)

    def NOT(self):
        return type(self)("NOT " + self.expr)

    @property
    def _is_compound(self):
        for x in self.expr.split():
            if x in KEYWORDS:
                return True
        return False

    def __str__(self):
        return self.expr

    def __invert__(self):  # Not
        return self.NOT()

    def __and__(self, other):  # And
        return self.AND(other)

    def __or__(self, other):  # Or
        return self.OR(other)

    __repr__ = __str__
