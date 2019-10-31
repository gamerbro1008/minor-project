import sqlite3 as sql
import json
from flask import Blueprint, abort, request, Response
import db.dbUtil as dbUtil

activity = Blueprint("activity", __name__)

module = activity


# CRUD
baseUrl = "/api/org/<orgId>/dept/<deptId>/act/"

@module.route(baseUrl)
def showAll(orgId,deptId):
    with sql.connect(dbUtil.connectionString) as conn:
        conn.row_factory = dbUtil.dict_factory
        cursor = conn.execute(f"SELECT * FROM activity WHERE orgId={orgId} AND deptId={deptId}")
        res = cursor.fetchall()
        return Response(json.dumps(res), mimetype='application/json')


@module.route(baseUrl+'<id>')
def showId(orgId,deptId,id):
    with sql.connect(dbUtil.connectionString) as conn:
        conn.row_factory = dbUtil.dict_factory
        cursor = conn.execute(f"SELECT * FROM activity WHERE id={id} AND orgId={orgId} AND deptId={deptId}")
        res = cursor.fetchone()
        if res == None:
            return abort(404)
        return dict(res)


@module.route(baseUrl+'create', methods=['POST', 'GET'])
def create(orgId, deptId):
    if request.method == 'POST':
        content = request.json
        if content != None and "name" in content.keys() and 'description' in content.keys():
            with sql.connect(dbUtil.connectionString) as conn:
                try:
                    conn.execute(
                        f"INSERT INTO activity (name,orgId,deptId,description) VALUES ('{content['name']}',{orgId},{deptId},'{content['description']}')")
                    conn.commit()
                    return Response(status=201)
                except Exception:
                    return Exception
    return abort(400)


@module.route(baseUrl+'update/<id>', methods=['POST', 'GET'])
def update(orgId,deptId,id):
    if request.method == 'POST':
        content = request.json
        if content != None and 'name' in content.keys() and 'description' in content.keys():
            with sql.connect(dbUtil.connectionString) as conn:
                try:
                    conn.execute(
                        f"UPDATE activity SET name='{content['name']}',description='{content['description']}' WHERE id={id} AND orgId={orgId} AND deptId={deptId}")
                    conn.commit()
                    return Response(status=202)
                except Exception:
                    return Exception
    return abort(400)


@module.route(baseUrl+'delete/<id>')
def delete(orgId,deptId,id):
    with sql.connect(dbUtil.connectionString) as conn:
        try:
            conn.execute(
                f"DELETE FROM activity WHERE id={id} AND orgId={orgId} AND deptId={deptId}")
            conn.commit()
            return Response(status=200) # OK
        except Exception:
            return Exception