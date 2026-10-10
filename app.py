from flask import *
import sqlite3
import json

app = Flask(__name__)
api_base = "/api/v0"

@app.route("/")
def root():
    return "testttttttttttttttttttt"

@app.route("/")
@app.route(api_base + "/")
@app.route(api_base + "/students")
@app.route(api_base + "/teacher_info")
@app.route(api_base + "/attendent")
@app.route(api_base + "/assignment/<action>") # info, add, edit_score
@app.route(api_base + "/calendar/<action>")
@app.route(api_base + "/file/<action>") # info, upload, download
@app.route(api_base + "/search/<category_to_search>") # TODO: Change "script" to something else (ex. to_be_search, search_type)
def dummyHandler(**kwargs):
    print(kwargs)
