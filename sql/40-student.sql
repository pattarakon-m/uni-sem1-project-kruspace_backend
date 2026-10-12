-- STUDENT TABLE
CREATE TABLE IF NOT EXISTS student (
	student_id TEXT UNIQUE ON CONFLICT REPLACE NOT NULL ON CONFLICT IGNORE,
	firstname TEXT,
	lastname TEXT,
	prefix TEXT,

	-- internal things
	create_at DATE,
	update_at DATE
);
