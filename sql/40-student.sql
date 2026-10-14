-- STUDENT TABLE
CREATE TABLE IF NOT EXISTS student (
	rowid INTEGER PRIMARY KEY,
	student_id TEXT NOT NULL,
	teacher_id INTEGER NOT NULL,
	firstname TEXT NOT NULL,
	lastname TEXT NOT NULL,
	prefix TEXT,
	sex TEXT,
	-- CLASS INFO -- TODO: nice to have but not require

	-- internal things
	create_at DATE,
	update_at DATE,
	UNIQUE(student_id, teacher_id),
	FOREIGN KEY (teacher_id) REFERENCES teacher(id)
);
