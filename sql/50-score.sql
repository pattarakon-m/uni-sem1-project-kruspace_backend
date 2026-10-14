-- SCORE
CREATE TABLE IF NOT EXISTS score (
    score INTEGER DEFAULT 0,
    assignment_id INTEGER NOT NULL,
    student_rowid INTEGER NOT NULL,

    update_at TEXT,
    UNIQUE(assignment_id, student_rowid) ON CONFLICT IGNORE,
    FOREIGN KEY (assignment_id) REFERENCES assignment(id) ON DELETE CASCADE,
    FOREIGN KEY (student_rowid) REFERENCES student(rowid) ON DELETE CASCADE
);
