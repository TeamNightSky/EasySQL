# EasySQL
## Overview
#### EasySQL is a dependency-free, pythonic module to make your SQL projects easy and fast.
To install EasySQL, simply use `pip install easysql`.
To view examples, look in `examples.py`, or continue reading for a more extensive description.

## Conditionals
Conditionals can be imported directly from easysql.
```python
from easysql import SQLConditional
```
Conditionals are initiated with a string representation of a condition.
```python
from easysql import SQLConditional as sqc
condition = sqc("age > 17")
```
To join conditionals, use `&, |, ~` for `AND, OR, NOT`, respecitvely. When compared, a new conditional is returned.
```python
from easysql import SQLConditional as sqc

condition = sqc("age > 17")
condition2 = sqc("age < 100")

condition3 = condition & condition2 # AND
condition4 = condition | condition2 # OR
condition5 = ~condition # NOT
```
## Queries
pass
