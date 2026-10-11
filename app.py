from flask import *
import sqlite3
import json
import os

app = Flask(__name__)
api_base = "/api/v0"
db_path = "./database.db"

@app.route("/")
def root():
    return "testttttttttttttttttttt"
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

@app.route("/")
@app.route(api_base + "/")
@app.route(api_base + "/students")
@app.route(api_base + "/teacher_info")
@app.route(api_base + "/attendent")
@app.route(api_base + "/assignment/<action>") # info, add, edit_score
@app.route(api_base + "/calendar/<action>")
@app.route(api_base + "/file/<action>") # info, upload, download
@app.route(api_base + "/search/<category_to_search>") # student, file, assignment, attendent
def dummyHandler(**kwargs):
    print(kwargs)
