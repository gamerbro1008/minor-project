import sqlite3 as sql
import json
from flask import Blueprint, abort, request, Response
import db.dbUtil as dbUtil

department = Blueprint("department", __name__)

module = department


# CRUD
baseUrl = "/api/org/<orgId>/dept/"


@module.route(baseUrl)
def showAll(orgId):
    with sql.connect(dbUtil.connectionString) as conn:
        conn.row_factory = dbUtil.dict_factory
        cursor = conn.execute(f"SELECT * FROM department WHERE orgId={orgId}")
        res = cursor.fetchall()
        return Response(json.dumps(res), mimetype='application/json')


@module.route(baseUrl+'<id>')
def showId(orgId, id):
    with sql.connect(dbUtil.connectionString) as conn:
        conn.row_factory = dbUtil.dict_factory
        cursor = conn.execute(
            f"SELECT * FROM department WHERE id={id} AND orgId={orgId}")
        res = cursor.fetchone()
        if res == None:
            return abort(404)
        return dict(res)


@module.route(baseUrl+'create', methods=['POST', 'GET'])
def create(orgId):
    if request.method == 'POST':
        content = request.json
        if content != None and "name" in content.keys() and 'description' in content.keys():
            with sql.connect(dbUtil.connectionString) as conn:
                try:
                    cursor = conn.execute(
                        f"INSERT INTO department (name,orgId,description) VALUES ('{content['name']}',{orgId},'{content['description']}')")
                    conn.commit()

                    deptId = cursor.lastrowid
                    print(deptId)
                    conn.execute(
                        f"INSERT INTO activity (name,orgId,deptId,description,isStart) VALUES ('Start',{orgId},{deptId},'Start of model',1)")
                    conn.commit()
                    return Response(status=201)
                except Exception:
                    return str(Exception)
    return abort(400)


@module.route(baseUrl+'update/<id>', methods=['POST', 'GET'])
def update(orgId, id):
    if request.method == 'POST':
        content = request.json
        if content != None and 'name' in content.keys() and 'description' in content.keys():
            with sql.connect(dbUtil.connectionString) as conn:
                try:
                    conn.execute(
                        f"UPDATE department SET name='{content['name']}',description='{content['description']}' WHERE id={id} AND orgId={orgId}")
                    conn.commit()
                    return Response(status=202)
                except Exception:
                    return Exception
    return abort(400)


@module.route(baseUrl+'delete/<id>')
def delete(orgId, id):
    with sql.connect(dbUtil.connectionString) as conn:
        try:
            conn.execute(
                f"DELETE FROM department WHERE id={id} AND orgId={orgId}")
            conn.commit()
            return Response(status=200)  # OK
        except Exception:
            return Exception
