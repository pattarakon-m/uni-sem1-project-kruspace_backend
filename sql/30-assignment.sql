-- ASSIGNMENT
CREATE TABLE IF NOT EXISTS assignment (
    id INTEGER PRIMARY KEY,
    name TEXT,
    subject TEXT,   -- SHOULD IT BE ANOTHER TABLE?
    topic TEXT,     -- SHOULD IT BE ANOTHER TABLE?
    class INTEGER CHECK (1 <= class AND class <= 12) NOT NULL,
    room INTEGER DEFAULT 1,
    max_score INTEGER DEFAULT 0,
    teacher_id INTEGER NOT NULL,

    create_at TEXT,
    update_at TEXT,
    FOREIGN KEY (teacher_id) REFERENCES teacher(id) ON DELETE CASCADE
);
