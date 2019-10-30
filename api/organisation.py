import sqlite3 as sql
import json
from flask import Blueprint, abort, request, Response
import db.dbUtil as dbUtil

organisation = Blueprint("organisation",__name__)

# CRUD

@organisation.route('/api/org/')
def showAllOrg():
    with sql.connect(dbUtil.connectionString) as conn:
        conn.row_factory = dbUtil.dict_factory
        cursor = conn.execute("SELECT * FROM organisation")
        res = cursor.fetchall()
        # print(res)
        return Response(json.dumps(res),mimetype='application/json')

@organisation.route('/api/org/<id>')
def showIdOrg(id):
    with sql.connect(dbUtil.connectionString) as conn:
        conn.row_factory = dbUtil.dict_factory
        cursor = conn.execute(f"SELECT * FROM organisation WHERE id={id}")
        res = cursor.fetchone()
        if res == None:
            return abort(404)
        return dict(res)
    
@organisation.route('/api/org/create',methods=['POST','GET'])
def createOrg():
    if request.method =='POST':
        content = request.json
        if content['name']
        with sql.connect(dbUtil.connectionString) as conn:
            conn.row_factory = dbUtil.dict_factory
            cursor = conn.execute(f"SELECT * FROM organisation WHERE id={id}")
            res = cursor.fetchone()
            if res == None:
                return abort(404)
            return str(res)
    