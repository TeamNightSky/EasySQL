# EasySQL

## Overview

**EasySQL is a dependency-free, pythonic module to make your SQL projects easy and fast**
To install EasySQL, simply use `pip install easysql`.
To view examples, look in `examples.py`, or continue reading for a more extensive description.

## Conditionals

Conditionals can be imported directly from `easysql`.

```python
from easysql import SQLConditional
```

Conditionals are initiated with a string representation of a condition.

```python
from easysql import SQLConditional as sqc
condition = sqc("age > 17")
```

To join conditionals, use `&, |, ~` for `AND, OR, NOT`, respectively. When compared, a new conditional is returned.

```python
from easysql import SQLConditional as sqc

condition = sqc("age > 17")
condition2 = sqc("age < 100")

condition3 = condition & condition2  # AND
condition4 = condition | condition2  # OR
condition5 = ~condition  # NOT
```

## Queries

Queries are inititated with the query type of the Query, the args for the type, and inititated from a DBType or with a DBType as a param.

```python
from easysql import DBType, Query

db = DBType("<db name>")

Q_param = Query("<type>", <args>, db=db) #  With DBType as a parameter
Q_method = db.query("<type>", <args>) #  From DBType method
```

Queries currently have the following types:

WIP

```
select         -- SQL SELECT method.           Params: column_names, table_name, constraints=None
delete         -- SQL DELETE method.           Params: table_name, constraints=None
update         -- SQL UPDATE method.           Params: 
insert         -- SQL INSERT method.           Params:
table          -- SQL CREATE TABLE method.     Params:
selectdistinct -- SQL SELECT DISTINCT method.  Params:
```
