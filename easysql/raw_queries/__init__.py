import easysql.raw_queries.common as common
from easysql.queries import Query


def wrap(raw_class):
    def construct(*args, **kwargs):
        return raw_class(*args, **kwargs)

    return construct


_METHODS = {
    "postgres": {
        "select": wrap(common._RawSQLSelect),
        "selectdistinct": wrap(common._RawSQLSelectDistinct),
        "insert": wrap(common._RawSQLInsert),
        "update": wrap(common._RawSQLUpdate),
        "delete": wrap(common._RawSQLDelete),
        "where": wrap(common._RawSQLWhere),
        "like": wrap(common._RawSQLLike),
        "between": wrap(common._RawSQLBetween),
        "in": wrap(common._RawSQLIn),
        "order": wrap(common._RawSQLOrder),
        "table": wrap(common._RawSQLTable),
    },
    "mysql": {
        "select": wrap(common._RawSQLSelect),
        "selectdistinct": wrap(common._RawSQLSelectDistinct),
        "insert": wrap(common._RawSQLInsert),
        "update": wrap(common._RawSQLUpdate),
        "delete": wrap(common._RawSQLDelete),
        "where": wrap(common._RawSQLWhere),
        "like": wrap(common._RawSQLLike),
        "between": wrap(common._RawSQLBetween),
        "in": wrap(common._RawSQLIn),
        "order": wrap(common._RawSQLOrder),
        "table": wrap(common._RawSQLTable),
    },
}


class DBType:
    def __init__(self, name):
        if name.lower() not in _METHODS.keys():
            raise ValueError(f"{name} is not a valid DB name")
        self._name = name.lower()

    def __getattr__(self, attr):
        if attr in _METHODS[self._name].keys():
            return _METHODS[self._name][attr]
        else:
            return super().__getattribute__(attr)

    def query(self, *args, **kwargs):
        return Query(*args, **kwargs, db=self)
