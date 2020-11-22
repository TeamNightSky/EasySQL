from easysql.errors import SQLError
from .conditions import SQLConditional as sqc


class Query:
    def __init__(self, method, *args, _filter=None, db=None):
        self._args = args
        self._method = method
        self._filter = _filter
        self.db = db
    
    def __repr__(self):
        return "<SQLQuery object '{}'>".format(self._method.upper().strip('_'))
    
    def __str__(self):
        return self.string
    
    
    def __lshift__(self, other):
        if type(other).__name__ != 'SQLConditional':
            raise TypeError('Cannot add condition to Query with type {}'.format(type(other)))
        if not self._filter:
            self._filter = self.Where(other)._filter
            return
        self._filter = self.Where(sqc(self._filter.condition).AND(other))._filter
    
    @property
    def string(self):
        _class = getattr(self.db, self._method)
        if _class.__name__ != '_insert' and self._filter is not None:
            raw = _class(*self._args, [self._filter])
        else:
            raw = _class(*self._args)
        return str(raw)

    def OrderBy(self, value, asc=True):
        order = self.db.order(value, asc)
        return Query(self._method, db=self.db, *self._args, _filter=order)
    
    # Filters
    def Where(self, condition=''):
        where = self.db.where(str(condition))
        where.extra = ''
        return Query(self._method[1:], self.db, *self._args, _filter=where)

    def Between(self, bottom, top):
        self._filter.extra += str(self.db.between(str(bottom), str(top)))
        return self

    def Like(self, pattern):
        self._filter.extra += str(self.db.like(pattern))
        return self
    
    def In(self, values):
        self._filter.extra += str(getattr(self.db, 'in')([str(value) for value in values]))
        return self

