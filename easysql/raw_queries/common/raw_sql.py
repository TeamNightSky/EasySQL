from ...util import check_has_not_type, join


class _RawSQL:
    @property
    def query(self):
        return "<query string>"

    def __str__(self):
        return self.query


class _RawSQLSelect(_RawSQL):
    def __init__(self, column_names, table_name, constraints=None):
        if constraints is None:
            constraints = []

        check_has_not_type([table_name, column_names], str)

        self.columns = column_names
        self.table = table_name
        self.constraints = constraints

    @property
    def _select(self):
        return "SELECT {}".format(", ".join(self.columns))

    @property
    def _from(self):
        return "FROM {}".format(self.table)

    @property
    def _constraints(self):
        return "\n".join([where.query for where in self.constraints])

    @property
    def query(self):
        return join([self._select, self._from, self._constraints]) + ";"


class _RawSQLSelectDistinct(_RawSQLSelect):
    @property
    def _select(self):
        return "SELECT DISTINCT {}".format(", ".join(self.columns))


class _RawSQLSelectTop(_RawSQLSelect):
    def __init__(self, row_count, columns, table_name, constraints=[]):
        self.rows = row_count
        super().__init__(columns, table_name, constraints)

    def _select(self):
        return "SELECT TOP {} {}".format(self.rows, self.columns)


class _RawSQLInsert(_RawSQL):
    def __init__(self, table_name, values, column_names=""):
        check_has_not_type([values, table_name, column_names])

        self.values = values
        self.table = table_name
        self.columns = column_names

    @property
    def _insert(self):
        insert = "INSERT INTO {}".format(self.table)
        if self.columns:
            insert += " ({})".format(", ".join(self.columns))
        return insert

    @property
    def _values(self):
        return "VALUES ({})".format(", ".join(self.values))

    @property
    def query(self):
        return join([self._insert, self._values]) + ";"


class _RawSQLInsertIntoSelect(_RawSQLInsert):
    def __init__(self, table_name, select_query):
        self.table = table_name
        self.select_query = select_query

    @property
    def _insert(self):
        return "INSERT INTO {}".format(self.table)

    @property
    def _select(self):
        return self.select_query

    @property
    def query(self):
        return join([self._insert, self._select])


class _RawSQLUpdate(_RawSQL):
    def __init__(self, table_name, column_value_map: dict, constraints=None):
        if constraints is None:
            constraints = []

        check_has_not_type([column_value_map.items(), table_name], str)

        self.column_value_map = column_value_map
        self.table = table_name
        self.constraints = constraints

    @property
    def _update(self):
        return "UPDATE {}".format(self.table)

    @property
    def _set(self):
        return "SET {}".format(
            ", ".join([" = ".join(item) for item in self.column_value_map.items()])
        )

    @property
    def _constraints(self):
        return join([where.query for where in self.constraints], "\n")

    @property
    def query(self):
        return join([self._update, self._set, self._constraints]) + ";"


class _RawSQLDelete(_RawSQL):
    def __init__(self, table_name, constraints=None):
        if constraints is None:
            constraints = []

        check_has_not_type([table_name])
        self.table = table_name
        self.constraints = constraints

    @property
    def _delete(self):
        return "DELETE FROM {}".format(self.table)

    @property
    def _constraints(self):
        return join([where.query for where in self.constraints], "\n")

    @property
    def query(self):
        return (
            join(
                [self._delete] + [self._constraints]
                if self._constraints != ""
                else [self._delete]
            ) + ";"
        )


class _RawSQLWhere(_RawSQL):
    def __init__(self, condition, extra=""):
        check_has_not_type([condition], str)
        self.condition = condition
        self.extra = extra

    @property
    def _extra(self):
        return str(self.extra)

    @property
    def _where(self):
        return "WHERE {}".format(str(self.condition))

    @property
    def query(self):
        return join([self._where, self._extra])


class _RawSQLLike(_RawSQL):
    def __init__(self, pattern):
        check_has_not_type([pattern])
        self.pattern = pattern

    @property
    def _like(self):
        return "LIKE {}".format(self.pattern)

    @property
    def query(self):
        return self._like


class _RawSQLBetween(_RawSQL):
    def __init__(self, num1: str, num2: str):
        check_has_not_type([num1, num2])
        self.nums = num1, num2

    @property
    def _between(self):
        return "BETWEEN {} AND {}".format(*self.nums)

    @property
    def query(self):
        return self._between


class _RawConditionsInput(_RawSQL):
    def __init__(self, *conditions, keyword=None):
        check_has_not_type([[str(cond) for cond in conditions], keyword], str)
        self._kw = keyword
        self.conditions = [
            str(cond) if type(cond) != list else cond for cond in conditions
        ]

    @property
    def query(self):
        return (" " + self._kw + " ").upper().join(self.conditions)


class _RawSQLIn(_RawConditionsInput):
    def __init__(self, values):
        super().__init__(values, keyword="in")

    @property
    def query(self):
        return "{} ({})".format(self._kw.upper(), ", ".join(*self.conditions))


class _RawSQLOrder(_RawSQL):
    def __init__(self, value, asc):
        self.asc = asc
        self.value = value

    @property
    def _order(self):
        return "ORDER"

    @property
    def _by(self):
        return "BY {}".format(self.value)

    @property
    def _asc(self):
        return "ASC" if self.asc else "DESC"

    @property
    def query(self):
        return join([self._order, self._by, self._asc])
