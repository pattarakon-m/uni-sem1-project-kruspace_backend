-- TEACHER_TABLE
CREATE TABLE IF NOT EXISTS teacher (
	id INTEGER PRIMARY KEY,
	firstname TEXT,
	lastname TEXT,
	prefix TEXT,
	email TEXT,
	profile_img BLOB,

	-- internal things
	password_hash TEXT,
	password_salt TEXT,
	create_at DATE,
	update_at DATE
);
