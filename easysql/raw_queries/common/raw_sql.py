from easysql.util import enforce_types, join


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

        enforce_types([table_name, column_names], str)

        self.columns = column_names
        self.table = table_name
        self.constraints = constraints

    @property
    def _select(self):
        sql_columns = ", ".join(self.columns)
        return f"SELECT {sql_columns}"

    @property
    def _from(self):
        return f"FROM {self.table}"

    @property
    def _constraints(self):
        return "\n".join(where.query for where in self.constraints)

    @property
    def query(self):
        return join([self._select, self._from, self._constraints]) + ";"


class _RawSQLSelectDistinct(_RawSQLSelect):
    @property
    def _select(self):
        sql_columns = ", ".join(self.columns)
        return f"SELECT DISTINCT {sql_columns}"


class _RawSQLSelectTop(_RawSQLSelect):
    def __init__(self, row_count, columns, table_name, constraints=None):
        if not constraints:
            constraints = []
        self.rows = row_count
        super().__init__(columns, table_name, constraints)

    def _select(self):
        return f"SELECT TOP {self.rows} {self.columns}"


class _RawSQLInsert(_RawSQL):
    def __init__(self, table_name, values, column_names=""):
        enforce_types([values, table_name, column_names])

        self.values = values
        self.table = table_name
        self.columns = column_names

    @property
    def _insert(self):
        insert = f"INSERT INTO {self.table}"
        if self.columns:
            insert += f" ({', '.join(self.columns)})"
        return insert

    @property
    def _values(self):
        sql_values = ", ".join(self.values)
        return f"VALUES ({sql_values})"

    @property
    def query(self):
        return join([self._insert, self._values]) + ";"


class _RawSQLInsertIntoSelect(_RawSQLInsert):
    def __init__(self, table_name, select_query):
        self.table = table_name
        self.select_query = select_query

    @property
    def _insert(self):
        return f"INSERT INTO {self.table}"

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

        enforce_types([column_value_map.items(), table_name], str)

        self.column_value_map = column_value_map
        self.table = table_name
        self.constraints = constraints

    @property
    def _update(self):
        return f"UPDATE {self.table}"

    @property
    def _set(self):
        sql_col_val_map = ", ".join(" = ".join(item) for item in self.column_value_map.items())
        return f"SET {sql_col_val_map}"

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

        enforce_types([table_name])
        self.table = table_name
        self.constraints = constraints

    @property
    def _delete(self):
        return f"DELETE FROM {self.table}"

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
        enforce_types([condition], str)
        self.condition = condition
        self.extra = extra

    @property
    def _extra(self):
        return str(self.extra)

    @property
    def _where(self):
        return f"WHERE {self.condition}"

    @property
    def query(self):
        return join([self._where, self._extra])


class _RawSQLLike(_RawSQL):
    def __init__(self, pattern):
        enforce_types([pattern])
        self.pattern = pattern

    @property
    def _like(self):
        return f"LIKE {self.pattern}"

    @property
    def query(self):
        return self._like


class _RawSQLBetween(_RawSQL):
    def __init__(self, num1: str, num2: str):
        enforce_types([num1, num2])
        self.num1 = num1
        self.num2 = num2

    @property
    def _between(self):
        return f"BETWEEN {self.num1} AND {self.num2}"

    @property
    def query(self):
        return self._between


class _RawConditionsInput(_RawSQL):
    def __init__(self, *conditions, keyword=None):
        enforce_types([[str(cond) for cond in conditions], keyword], str)
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
        sql_conditions = ", ".join(*self.conditions)
        return f"{self._kw.upper()} ({sql_conditions})"


class _RawSQLOrder(_RawSQL):
    def __init__(self, value, asc):
        self.asc = asc
        self.value = value

    @property
    def _order(self):
        return "ORDER"

    @property
    def _by(self):
        return f"BY {self.value}"

    @property
    def _asc(self):
        return "ASC" if self.asc else "DESC"

    @property
    def query(self):
        return join([self._order, self._by, self._asc])


class _RawSQLTable(_RawSQL):
    def __init__(self, name, column_value_map: dict, if_not_exists=True):
        self.name = name
        self.map = column_value_map
        self.if_not_exists = if_not_exists

    @property
    def _create(self):
        return f"CREATE TABLE {'IF NOT EXISTS ' if self.if_not_exists else ''}{self.name}"

    @property
    def _values(self):
        return f"({', '.join([' '.join(items) for items in self.map.items()])})"

    @property
    def query(self):
        return join([self._create, self._values]) + ";"
