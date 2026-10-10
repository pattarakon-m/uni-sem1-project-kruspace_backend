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
	res = cursor.execute("SELECT count(id), data FROM test GROUP BY data")
	for (id, data) in res.fetchall():
		print(id, data)
	dbcon.commit()
