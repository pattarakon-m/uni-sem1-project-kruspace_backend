import sqlite3
import random

if __name__ == "__main__":
	dbcon = sqlite3.connect("database.db")
	cursor = dbcon.cursor()
	res = cursor.execute("CREATE TABLE IF NOT EXISTS test (id INTERGER PRIMARY KEY, data TEXT);")
	res = cursor.execute("SELECT * FROM test;")
	data = [
		(random.uniform(0,1)*1000 // 1, random.choice(["hello", "world", "foo", "bar"])) for _ in range(100)
	]
	res = cursor.executemany("INSERT OR IGNORE INTO test VALUES (?, ?)", data)
	dbcon.commit()

	res = cursor.execute("SELECT count(id), data FROM test GROUP BY data")
	query_res = res.fetchall()
	print(dir(query_res))
	for (id, data) in query_res:
		print(id, data)
	res = cursor.execute("SELECT count(id) FROM test WHERE data = ?", (random.choice(["hello", "world", "foo", "bar"]),))
	for (count,) in res.fetchall():
		print(count)
	dbcon.commit()
