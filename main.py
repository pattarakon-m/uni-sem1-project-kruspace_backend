from flask import *
import sqlite3
import json
import os
import base64
import re
import time

app = Flask("KruSpace")
api_base = "/api/v0"
db_path = "./database.db"

# DB RELATED PART

def sql_opendb():
    db = getattr(g, "db", None)
    def dict_factory(cursor, row):
        return dict((cursor.description[i][0], value) for i, value in enumerate(row))
    if db is None:
        db = g.db = sqlite3.connect(db_path)
        db.row_factory = dict_factory
    return db

def sql_closedb():
    db = getattr(g, "db", None)
    if db:
        db.commit()
        db.close()
        g.db = None

def sql_prepare():
    db = sqlite3.connect(db_path)
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
    db.close()

sql_prepare()

# LOGIN / AUTH

def is_login_correct(email, password):
    return True # TODO

def is_logged_in(teacher_id, session_id):
    return True # TODO

def auto_abort_unauthorized(request):
    session_id = request.cookies.get("session_id")
    teacher_id = request.cookies.get("teacher_id")
    if session_id is None or teacher_id is None:
        abort(401)
    if not is_logged_in(teacher_id, session_id):
        abort(401)

# ACTUAL SERVER FUNC

## ADMIN

@app.route("/.admin/new_teacher")
def new_teacher():
    return

## API
# TODO: Proper error message/response

@app.route(api_base + "/")
@app.route(api_base + "/calendar/<action>")
@app.route(api_base + "/file/<action>") # info, upload, download
@app.route(api_base + "/search/<category_to_search>") # student, file, assignment, attendent
def dummyHandler(**kwargs):
    print(kwargs)
    res = make_response()
    res.headers["Content-Type"] = "application/json"
    return json.dumps(kwargs, indent="\t")

@app.route(api_base + "/teacher_info", methods=['GET', 'POST'])
def teacher_info():
    auto_abort_unauthorized(request)
    teacher_id = request.cookies.get("teacher_id")
    db = None
    # Don't worry about non exists teacher, is_logged_in already check it for us.
    if request.method == 'POST':
        req = request.get_json()
        # TODO: server should validate user input
        db = sql_opendb()
        db_cur = db.cursor()
        for field in ["prefix", "firstname", "lastname", "sex", "email"]:
            if field not in req:
                continue
            query = "UPDATE teacher SET %s = ? WHERE id = ?" % field # this is safe, user can't control `field`
            db_cur.execute(query, [req[field], teacher_id])
        if req.get("profile_img"):
            db_cur.execute("UPDATE teacher SET profile_img = ? WHERE id = ?",
                [base64.b64decode(req["profile_img"]), teacher_id]
            )
        db_cur.execute("UPDATE teacher SET update_at = datetime() WHERE id = ?", [teacher_id])
        db.commit()
    http_res = make_response()
    http_res.headers["Content-Type"] = "application/json"
    db = sql_opendb()
    # TODO: sent profile image on demand.
    exec_res = db.cursor().execute('''
        SELECT prefix, firstname, lastname, sex, email, profile_img
        FROM teacher WHERE id = ?''',
        [teacher_id]
    )
    db_data = exec_res.fetchall()
    sql_closedb()
    if len(db_data) > 0:
        teacher_data = db_data[0]
        if teacher_data["profile_img"]:
            teacher_data["profile_img"] = base64.b64encode(teacher_data["profile_img"]).decode()
        http_res.data = json.dumps(teacher_data) + "\n"
        return http_res
    abort(400)

### ASSIGNMENT
# TODO: Use flask's blueprint

def get_assignment_obj(assignment_id, teacher_id):
    '''
    Query assignment object by assignment_id and teacher_id
    It automatically open and close the databse
    '''
    if assignment_id is None or teacher_id is None:
        return None
    db = sql_opendb()
    assignments = db.cursor().execute(
            "SELECT id, name, subject, topic, class, room, max_score, due, create_at FROM assignment WHERE teacher_id = ? AND id = ?",
            [teacher_id, assignment_id]
        ).fetchall()
    sql_closedb()
    if len(assignments) == 1:
        return assignments[0]
    return None

@app.get(api_base + "/assignment/info")
def assignment_info():
    auto_abort_unauthorized(request)
    teacher_id = request.cookies.get("teacher_id")
    assignment_id = request.args.get("assignment_id")
    http_res = make_response()
    http_res.headers["Content-Type"] = "application/json"
    assignment = get_assignment_obj(assignment_id, teacher_id)
    if assignment:
        http_res.data = json.dumps(assignment) + "\n"
        return http_res
    abort(400)

@app.get(api_base + "/assignment/list")
def assignment_list():
    auto_abort_unauthorized(request)
    teacher_id = request.cookies.get("teacher_id")
    http_res = make_response()
    http_res.headers["Content-Type"] = "application/json"
    assignments = sql_opendb().cursor().execute(
            "SELECT id, name, subject, topic, class, room, max_score, due, create_at FROM assignment WHERE teacher_id = ?",
            [teacher_id]
        ).fetchall()
    sql_closedb()
    if len(assignments) > 0:
        http_res.data = json.dumps(assignments) + "\n"
        return http_res
    abort(400)

@app.post(api_base + "/assignment/add")
def assignment_add():
    auto_abort_unauthorized(request)
    teacher_id = request.cookies.get("teacher_id")
    http_res = make_response()
    http_res.headers["Content-Type"] = "application/json"
    req = request.get_json()
    db = sql_opendb()
    db_cur = db.cursor()
    for field in ["name", "subject", "topic", "class"]:
        if field not in req:
            abort(400)
    assignment_id = db_cur.execute("""
        INSERT INTO assignment (
            name,
            subject,
            topic,
            class,
            teacher_id,
            create_at
        ) VALUES (?, ?, ?, ?, ?, datetime())
        RETURNING id""",
        [req["name"], req["subject"], req["topic"], req["class"], teacher_id]
    ).fetchall()[0]["id"]
    db.commit()
    for field in ["room", "max_score", "due"]:
        if field not in req:
            continue
        query = "UPDATE assignment SET %s = ? WHERE id = ?" % field # this is safe, user can't control `field`
        db_cur.execute(query, [req[field], assignment_id])
    db_cur.execute("UPDATE assignment SET update_at = datetime() WHERE id = ?", [assignment_id])
    db_cur.execute("""
        INSERT OR IGNORE INTO score (student_rowid, assignment_id, update_at)
        SELECT student.rowid AS student_rowid, ? AS assignment_id, datetime() AS update_at
          FROM student WHERE teacher_id = ?
    """, [assignment_id, teacher_id])
    db.commit()
    sql_closedb()
    assignment = get_assignment_obj(assignment_id, teacher_id)
    if assignment:
        http_res.data = json.dumps(assignment) + "\n"
        return http_res
    abort(400)

@app.post(api_base + "/assignment/edit")
def assignment_edit():
    auto_abort_unauthorized(request)
    teacher_id = request.cookies.get("teacher_id")
    assignment_id = request.args.get("assignment_id")
    http_res = make_response()
    http_res.headers["Content-Type"] = "application/json"

    req = request.get_json()
    db = sql_opendb()
    db_cur = db.cursor()
    for field in ["name", "subject", "topic", "class", "room", "max_score", "due"]:
        if field not in req:
            continue
        query = "UPDATE assignment SET %s = ? WHERE id = ?" % field # this is safe, user can't control `field`
        db_cur.execute(query, [req[field], assignment_id])
    db_cur.execute("UPDATE assignment SET update_at = datetime() WHERE id = ?", [assignment_id])
    db.commit()
    sql_closedb()
    assignment = get_assignment_obj(assignment_id, teacher_id)
    if assignment:
        http_res.data = json.dumps(assignment) + "\n"
        return http_res
    abort(400)

@app.get(api_base + "/student/list")
def student_list():
    auto_abort_unauthorized(request)
    teacher_id = request.cookies.get("teacher_id")
    # assume single student -> single teacher
    # pros: easy to deal with
    # cons: duplicate data
    db = sql_opendb()
    db_cur = db.cursor()
    students_data = db_cur.execute(
        "SELECT student_id, prefix, firstname, lastname, sex FROM student WHERE teacher_id = ?",
        [teacher_id]
    ).fetchall()
    sql_closedb()
    http_res = make_response()
    http_res.headers["Content-Type"] = "application/json"
    http_res.data = json.dumps(students_data) + "\n"
    return http_res

@app.post(api_base + "/student/add")
def student_add():
    auto_abort_unauthorized(request)
    teacher_id = request.cookies.get("teacher_id")
    # assume single student -> single teacher
    # pros: easy to deal with
    # cons: duplicate data
    req = request.get_json()
    for field in ["student_id", "firstname", "lastname"]:
        if field not in req:
            abort(400)
    student_id = req["student_id"]
    db = sql_opendb()
    db_cur = db.cursor()
    try:
        db_cur.execute(
            "INSERT INTO student (student_id, firstname, lastname, teacher_id, create_at) VALUES (?, ?, ?, ?, datetime())",
            [req["student_id"], req["firstname"], req["lastname"], teacher_id]
        )
        for field in ["firstname", "lastname", "sex", "prefix"]:
            if field not in req:
                continue
            query = "UPDATE student SET %s = ? WHERE student_id = ?" % field # this is safe, user can't control `field`
            db_cur.execute(query, [req[field], student_id])
    except Exception as e:
        sql_closedb()
        print(e)
        return "student id '%s' already exists in the database, consider using `edit` instead.\n" % student_id, 400
    db_cur.execute("UPDATE student SET update_at = datetime() WHERE student_id = ?", [student_id])
    db.commit()
    students_data = db_cur.execute(
        "SELECT student_id, prefix, firstname, lastname, sex FROM student WHERE student_id = ?",
        [student_id]
    ).fetchall()[0]
    sql_closedb()
    http_res = make_response()
    http_res.headers["Content-Type"] = "application/json"
    http_res.data = json.dumps(students_data) + "\n"
    return http_res

@app.post(api_base + "/student/edit")
def student_edit():
    auto_abort_unauthorized(request)
    teacher_id = request.cookies.get("teacher_id")
    student_id = request.args.get("student_id")
    # assume single student -> single teacher
    # pros: easy to deal with
    # cons: duplicate data
    req = request.get_json()
    db = sql_opendb()
    db_cur = db.cursor()
    for field in ["firstname", "lastname", "sex", "prefix"]:
        if field not in req:
            continue
        query = "UPDATE student SET %s = ? WHERE student_id = ?" % field # this is safe, user can't control `field`
        db_cur.execute(query, [req[field], student_id])
    db_cur.execute("UPDATE student SET update_at = datetime() WHERE student_id = ?", [student_id])
    db.commit()
    students_data = db_cur.execute(
        "SELECT student_id, prefix, firstname, lastname, sex FROM student WHERE student_id = ? AND teacher_id = ?",
        [student_id, teacher_id]
    ).fetchall()
    sql_closedb()
    http_res = make_response()
    http_res.headers["Content-Type"] = "application/json"
    if len(students_data) > 0:
        http_res.data = json.dumps(students_data[0]) + "\n"
        return http_res
    return "student id '%s' is not in the database\n" % student_id, 400

@app.post(api_base + "/student/remove")
def student_remove():
    auto_abort_unauthorized(request)
    teacher_id = request.cookies.get("teacher_id")
    student_id = request.args.get("student_id")
    if student_id is None:
        return "server expected `student_id` parameter\n", 400
    # assume single student -> single teacher
    # pros: easy to deal with
    # cons: duplicate data
    db = sql_opendb()
    db_cur = db.cursor()
    if db_cur.execute("SELECT COUNT(student_id) AS count FROM student WHERE student_id = ? AND teacher_id = ?", [student_id, teacher_id]).fetchall()[0]["count"] < 1:
        sql_closedb()
        return "student id '%s' is not in the database\n" % student_id, 400
    db_cur.execute("DELETE FROM student WHERE student_id = ? AND teacher_id = ?", [student_id, teacher_id])
    db.commit()
    sql_closedb()
    http_res = make_response()
    http_res.headers["Content-Type"] = "application/json"
    http_res.data = "{}\n"
    return http_res

@app.get(api_base + "/score")
def score_list():
    auto_abort_unauthorized(request)
    teacher_id = request.cookies.get("teacher_id")
    assignment_id = request.args.get("assignment_id")
    db = sql_opendb()
    db_cur = db.cursor()
    assignment_info = db_cur.execute(
        "SELECT id, name, topic, subject, due, max_score, create_at FROM assignment WHERE id = ? AND teacher_id = ?",
        [assignment_id, teacher_id]
    ).fetchone()
    if assignment_info is None:
        return "assignment id '%s' not found\n" % assigment_id, 400
    student_scores = db_cur.execute("""
        SELECT student_id, prefix, firstname, lastname, score
          FROM (
            student JOIN score
            ON student.rowid = score.student_rowid
        ) WHERE assignment_id = ? AND teacher_id = ?""",
        [assignment_id, teacher_id]
    ).fetchall()
    sql_closedb()
    http_res = make_response()
    http_res.headers["Content-Type"] = "application/json"
    http_res.data = json.dumps({"assignment_info": assignment_info, "scores": student_scores}) + "\n"
    return http_res

@app.post(api_base + "/score")
def score_edit():
    auto_abort_unauthorized(request)
    teacher_id = request.cookies.get("teacher_id")
    assignment_id = request.args.get("assignment_id")

    # validate body
    req = request.get_json()
    for record in req:
        for field in ["score", "student_id"]:
            if field not in record:
                abort(400)


    db = sql_opendb()
    db_cur = db.cursor()

    # validate assignment_id
    if db_cur.execute("SELECT id FROM assignment WHERE id = ? AND teacher_id = ?", [assignment_id, teacher_id]).fetchone() is None:
        return "assignment id '%s' not found\n" % assigment_id, 400

    # TODO: make sure `score` <= `max_score`
    records = [ [record["score"], assignment_id, record["student_id"], teacher_id] for record in req ]
    db_cur.executemany("""
        UPDATE score SET update_at = datetime(), score = ?
        WHERE score.assignment_id = ?
          AND score.student_rowid = (
            SELECT rowid FROM student WHERE student_id = ? AND teacher_id = ?
          )
        """,
        records
    )
    sql_closedb()
    http_res = make_response()
    http_res.headers["Content-Type"] = "application/json"
    http_res.data = json.dumps({}) + "\n"
    return http_res

@app.get(api_base + "/attendant")
def attendent_list():
    # status (0-4) meaning:  NO_DATA, MISSING, ATTEND, LATE, LEAVE
    auto_abort_unauthorized(request)
    teacher_id = request.cookies.get("teacher_id")
    date = request.args.get("date")
    try:
        time.strptime(date, "%Y-%m-%d")
    except:
        return "invalid date '%s'\n" % date, 400

    db = sql_opendb()
    db_cur = db.cursor()

    if db_cur.execute("SELECT day FROM attendant_day WHERE day = ? AND teacher_id = ?", [date, teacher_id]).fetchone() is None:
        row_id = db_cur.execute("INSERT INTO attendant_day (teacher_id, day) VALUES (?, date()) RETURNING rowid", [teacher_id]).fetchone()["rowid"]
        db_cur.execute("""
            INSERT INTO attendant_student (student_rowid, attendant_day_rowid)
            SELECT student.rowid AS student_rowid, ? AS attendant_day_rowid
            FROM student WHERE teacher_id = ?
            """, [row_id, teacher_id])
        db.commit()

    student_attendants =  db_cur.execute("""
        SELECT student_id, prefix, firstname, lastname, status
          FROM (
               student
          JOIN attendant_day
          JOIN attendant_student
            ON student.rowid = attendant_student.student_rowid
           AND attendant_day.rowid = attendant_student.attendant_day_rowid
        ) WHERE day = ? AND attendant_day.teacher_id = ?""",
        [date, teacher_id]
    ).fetchall()

    sql_closedb()
    http_res = make_response()
    http_res.headers["Content-Type"] = "application/json"
    http_res.data = json.dumps({"date": date, "attendants": student_attendants}) + "\n"
    return http_res

@app.post(api_base + "/attendant")
def attendent_edit():
    auto_abort_unauthorized(request)
    teacher_id = request.cookies.get("teacher_id")
    date = request.args.get("date")
    try:
        time.strptime(date, "%Y-%m-%d")
    except:
        return "invalid date '%s'\n" % date, 400

    # validate body
    req = request.get_json()
    for record in req:
        if "student_id" not in record:
            abort(400)
        if "status" not in record:
            abort(400)
        if (not 0 <= record["status"]) or (not record["status"] <= 4):
            return "invalid status range, expect (0-4) but got '%s'\n" % record["status"], 400

    db = sql_opendb()
    db_cur = db.cursor()
    # make sure attendant data is exists
    if db_cur.execute("SELECT day FROM attendant_day WHERE day = ? AND teacher_id = ?", [date, teacher_id]).fetchone() is None:
        row_id = db_cur.execute("INSERT INTO attendant_day (teacher_id, day) VALUES (?, date()) RETURNING rowid", [teacher_id]).fetchone()["rowid"]
        db_cur.execute("""
            INSERT INTO attendant_student (student_rowid, attendant_day_rowid)
            SELECT student.rowid AS student_rowid, ? AS attendant_day_rowid
            FROM student WHERE teacher_id = ?
            """, [row_id, teacher_id])
        db.commit()

    records = [ [record["status"], date, teacher_id, record["student_id"], teacher_id] for record in req ]
    # SELECT rowid FROM attendant_day WHERE day = ? AND techer_id = ?
    # SELECT rowid FROM student WHERE student_id = ? AND teacher_id = ?
    db_cur.executemany("""
        UPDATE attendant_student SET status = ?
         WHERE attendant_student.attendant_day_rowid = (SELECT rowid FROM attendant_day WHERE day        = ? AND teacher_id = ?)
           AND attendant_student.student_rowid       = (SELECT rowid FROM student       WHERE student_id = ? AND teacher_id = ?)
        """,
        records
    )
    db.commit()
    sql_closedb()
    http_res = make_response()
    http_res.headers["Content-Type"] = "application/json"
    http_res.data = json.dumps({}) + "\n"
    return http_res

if __name__ == "__main__":
    app.run(host="localhost", port=5000)
