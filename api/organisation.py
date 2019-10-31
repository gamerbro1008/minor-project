import sqlite3 as sql
import json
from flask import Blueprint, abort, request, Response
import db.dbUtil as dbUtil

organisation = Blueprint("organisation", __name__)

module = organisation


# CRUD
baseUrl = "/api/org/"

@module.route(baseUrl)
def showAllOrg():
    with sql.connect(dbUtil.connectionString) as conn:
        conn.row_factory = dbUtil.dict_factory
        cursor = conn.execute("SELECT * FROM organisation")
        res = cursor.fetchall()
        return Response(json.dumps(res), mimetype='application/json')


@module.route(baseUrl+'<id>')
def showIdOrg(id):
    with sql.connect(dbUtil.connectionString) as conn:
        conn.row_factory = dbUtil.dict_factory
        cursor = conn.execute(f"SELECT * FROM organisation WHERE id={id}")
        res = cursor.fetchone()
        if res == None:
            return abort(404)
        return dict(res)


@module.route(baseUrl+'create', methods=['POST', 'GET'])
def createOrg():
    if request.method == 'POST':
        content = request.json
        if content != None and content['name'] != None:
            with sql.connect(dbUtil.connectionString) as conn:
                try:
                    conn.execute(
                        f"INSERT INTO organisation (name) VALUES ('{content['name']}')")
                    conn.commit()
                    return Response(status=201)
                except Exception:
                    return Exception


@module.route(baseUrl+'update/<id>', methods=['POST', 'GET'])
def updateOrg(id):
    if request.method == 'POST':
        content = request.json
        if content != None and content['name'] != None:
            with sql.connect(dbUtil.connectionString) as conn:
                try:
                    conn.execute(
                        f"UPDATE organisation SET name='{content['name']}' WHERE id={id}")
                    conn.commit()
                    return Response(status=202)
                except Exception:
                    return Exception


@module.route(baseUrl+'delete/<id>')
def deleteOrg(id):
    with sql.connect(dbUtil.connectionString) as conn:
        try:
            conn.execute(
                f"DELETE FROM organisation WHERE id={id}")
            conn.commit()
            return Response(status=200) # OK
        except Exception:
            return Exception