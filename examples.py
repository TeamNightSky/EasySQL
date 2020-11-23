from easysql import DBType, SQLConditional as sqc

"""
examples.py does NOT use
the best SQL syntax, and
that is intentional and
for demonstrational purposes
"""

print("-> SQL Expressions")

con = sqc("age > 5")
con2 = sqc("age < 10")

print(con & con2)   # Use AND to combine conditionals (&)
print(con | con2)   # Use OR to combine conditionals (|)
print(~con & con2 | con)   # Use NOT to invert a conditional (~)

print("\n-> SQL Queries:")

db = DBType("MySQL")

Q_select = db.query("select", "*", "people")   # SQL SELECT method
Q_delete = db.query("delete", "people")   # SQL DELETE method
Q_insert = db.query("insert", "people", ["fox", "-1"])   # SQL INSERT method
Q_update = db.query("update", "people", {"name": "fox", "age": "-1"})   # SQL UPDATE method

Q_select << ~con2   # add NOT con2 to Q_select
Q_select << con   # add con to Q_select (Query uses AND to join unjoined conditionals)
Q_select.Like("%b")   # add LIKE to Q_select

Q_delete << (~con2 & con)   # add NOT con2 AND con to Q_delete
Q_delete.Between(5, 10)   # add BETWEEN to Q_delete

Q_update << ~con2   # you know this by now
Q_update << con   # you also know this by now
Q_update.In([5, 6, 7])   # add IN (5, 6, 7) to Q_update

print(Q_select, Q_delete, Q_insert, Q_update, sep="\n")

"""
SELECT * FROM people WHERE NOT age < 10 AND age > 5 LIKE %b;
DELETE FROM people WHERE NOT age < 10 AND age > 5 BETWEEN 5 AND 10;
INSERT INTO people VALUES (fox, -1);
UPDATE people SET name = fox, age = -1 WHERE NOT age < 10 AND age > 5 IN (5, 6, 7);
"""
