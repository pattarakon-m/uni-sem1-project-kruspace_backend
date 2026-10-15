-- TEACHER_TABLE
CREATE TABLE IF NOT EXISTS teacher (
	id INTEGER PRIMARY KEY,
	firstname TEXT,
	lastname TEXT,
	prefix TEXT,
	email TEXT UNIQUE NOT NULL,
	sex TEXT,
	profile_img BLOB,

	-- internal things
	password_hash BLOB,
	password_salt BLOB,
	create_at TEXT,
	update_at TEXT
);
