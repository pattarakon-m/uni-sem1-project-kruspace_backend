import sqlite3
import random
import os
import re

if __name__ == "__main__":
    db = sqlite3.connect("database.db")
    db_cur = db.cursor()
    for query_name in os.listdir("./sql"):
        if not query_name.endswith(".sql"):
            continue
        if not re.match('[0-9]{2}-', query_name):
            continue
        f = open("./sql/" + query_name)
        query = f.read()
        db_cur.executescript(query)
    db.commit()

    teachers = [
        ["Misaka", "Mikoto"],
        ["Touma", "Kamijo"],
        ["Nanoha", "Takamachi"],
        ["Fate", "Testarossa"],
        ["Hayate", "Yagami"]
    ]
    for i in range(len(teachers)):
        teachers[i] += ["%s@example.com" % teachers[i][0].lower()]
    db_cur.executemany("INSERT INTO teacher (firstname, lastname, email) VALUES (?, ?, ?)", teachers)

    students = [
        [random.randint(1, len(teachers)), ''.join([hex(i)[2:] for i in random.randbytes(6)]), "Yuki", "Nagato"],
        [random.randint(1, len(teachers)), ''.join([hex(i)[2:] for i in random.randbytes(6)]), "Subaru", "Natsuki"],
        [random.randint(1, len(teachers)), ''.join([hex(i)[2:] for i in random.randbytes(6)]), "Tomoya", "Okazaki"],
        [random.randint(1, len(teachers)), ''.join([hex(i)[2:] for i in random.randbytes(6)]), "Youhei", "Sunohara"],
        [random.randint(1, len(teachers)), ''.join([hex(i)[2:] for i in random.randbytes(6)]), "Tsukasa", "Hiiragi"],
        [random.randint(1, len(teachers)), ''.join([hex(i)[2:] for i in random.randbytes(6)]), "Kagami", "Hiiragi"],
        [random.randint(1, len(teachers)), ''.join([hex(i)[2:] for i in random.randbytes(6)]), "Konata", "Izumi"],
        [random.randint(1, len(teachers)), ''.join([hex(i)[2:] for i in random.randbytes(6)]), "Izumi", "Sakurai"],
        [random.randint(1, len(teachers)), ''.join([hex(i)[2:] for i in random.randbytes(6)]), "Manabu", "Takasaki"],
        [random.randint(1, len(teachers)), ''.join([hex(i)[2:] for i in random.randbytes(6)]), "Kojiro", "Sasahara"],
        [random.randint(1, len(teachers)), ''.join([hex(i)[2:] for i in random.randbytes(6)]), "Makoto", "Sakurai"],
        [random.randint(1, len(teachers)), ''.join([hex(i)[2:] for i in random.randbytes(6)]), "Sakura", "Kinomoto"]
    ]

    db_cur.executemany("INSERT INTO student (teacher_id, student_id, firstname, lastname) VALUES (?, ?, ?, ?)", students)

    assignments =[
        [8, "Physics", "Force", "Newton's 1st Law"],
        [8, "Physics", "Force", "Newton's 2nd Law"],
        [3, "Math", "Operator", "Addition"],
        [3, "Math", "Operator", "Subtraction"],
        [3, "Math", "Operator", "Multiplication"],
        [3, "Math", "Operator", "Division"],
        [5, "Social", "Religion", "Buddhism"],
        [5, "Social", "Religion", "Chritianity"],
        [5, "Social", "Religion", "Islam"]
    ]
    for i in range(1,len(teachers)+1):
        assignment_index = random.randint(0, len(assignments)-1)
        db_cur.executemany(
            "INSERT INTO assignment (teacher_id, class, subject, topic, name) VALUES (?, ?, ?, ?, ?)",
            [[i] + assignments[(assignment_index + j) % len(assignments)] for j in range(3)]
        )

    db_cur.execute("""
        INSERT OR IGNORE INTO score (student_rowid, assignment_id)
            SELECT student.rowid AS student_rowid, assignment.id AS assignment_id 
                FROM (
                    student JOIN assignment 
                    ON student.teacher_id = assignment.teacher_id
                )
    """)

    db.commit()
    db.close()

