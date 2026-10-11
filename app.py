from flask import *
import sqlite3
import json
import os
import base64

app = Flask(__name__)
api_base = "/api/v0"
db_path = "./database.db"

# DB RELATED PART

def sql_opendb():
    db = getattr(g, "_database", None)
    def dict_factory(cursor, row):
        return dict((cursor.description[i][0], value) for i, value in enumerate(row))
    if db is None:
        db = g._database = sqlite3.connect(db_path)
        db.row_factory = dict_factory
    return db

def sql_closedb():
    db = getattr(g, "_database", None)
    if db:
        db.commit()
        db.close()

def sql_prepare():
    db = sqlite3.connect(db_path)
    db_cur = db.cursor()
    for query_name in os.listdir("./sql"):
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

# ACTUAL SERVER FUNC

## ADMIN

@app.route("/.admin/new_teacher")
def new_teacher():
    return

## API

@app.route(api_base + "/")
@app.route(api_base + "/students")
@app.route(api_base + "/attendent")
@app.route(api_base + "/assignment/<action>") # info, add, edit_score
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
    session_id = request.cookies.get("session_id")
    teacher_id = request.cookies.get("teacher_id")
    if not is_logged_in(teacher_id, session_id):
        abort(401)
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
