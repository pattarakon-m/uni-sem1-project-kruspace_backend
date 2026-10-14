-- ATTENDANT
CREATE TABLE IF NOT EXISTS attendant_day (
    rowid INTEGER PRIMARY KEY,
    day TEXT NOT NULL, -- YYYY-MM-DD
    teacher_id INTEGER NOT NULL,

    UNIQUE(day, teacher_id),
    FOREIGN KEY (teacher_id) REFERENCES teacher(id) ON DELETE CASCADE
);

-- ATTENDANT + STUDENT
CREATE TABLE IF NOT EXISTS attendant_student (
    student_rowid INTEGER NOT NULL,
    attendant_day_rowid INTEGER NOT NULL,
    status INTEGER DEFAULT 0 CHECK (0 <= status <= 4) , -- NO_DATA, MISSING, ATTEND, LATE, LEAVE

    UNIQUE(student_rowid, attendant_day_rowid),
    FOREIGN KEY (student_rowid)       REFERENCES student(rowid)       ON DELETE CASCADE,
    FOREIGN KEY (attendant_day_rowid) REFERENCES attendant_day(rowid) ON DELETE CASCADE
);
