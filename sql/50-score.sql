-- SCORE
CREATE TABLE IF NOT EXISTS score (
    score INTEGER DEFAULT 0,
    assignment_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    UNIQUE(assignment_id, student_id) ON CONFLICT IGNORE,
    FOREIGN KEY (assignment_id) REFERENCES assignment(id) ON DELETE CASCADE,
    FOREIGN KEY (student_id)    REFERENCES student(id)    ON DELETE CASCADE
)
