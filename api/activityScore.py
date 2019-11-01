import sqlite3 as sql
import json
from flask import Blueprint, abort, request, Response
import db.dbUtil as dbUtil

activityScore = Blueprint("activityScore", __name__)

module = activityScore


# CRUD
baseUrl = "/api/org/<orgId>/dept/<deptId>/activityScore/<prevActId>/"


@module.route(baseUrl)
def showSuggested(orgId, deptId, prevActId):
    with sql.connect(dbUtil.connectionString) as conn:
        conn.row_factory = dbUtil.dict_factory

        if prevActId == "0":
            res = []
            cursor = conn.execute(
                f'SELECT activity.id AS suggestedActId FROM activity WHERE deptId={deptId} AND isStart=1')
            data = cursor.fetchone()
            data['score'] = '0'
            res.append(data)
            return Response(json.dumps(res), mimetype='application/json')

        else:
            cursor = conn.execute(
                f"SELECT suggestedActId,score FROM activityScore WHERE prevActId={prevActId} ORDER BY score desc LIMIT 5")
            res = cursor.fetchall()
            return Response(json.dumps(res), mimetype='application/json')


@module.route(baseUrl+'<searchActName>')
def showAll(orgId, deptId, prevActId, searchActName):
    with sql.connect(dbUtil.connectionString) as conn:
        conn.row_factory = dbUtil.dict_factory
        cursor = conn.execute(
            f"SELECT id FROM activity WHERE ( name like '%{searchActName}%' OR description like '%{searchActName}%' ) and deptId={deptId}")
        allActId = cursor.fetchall()
        print(allActId)
        result = []
        for actId in allActId:
            id = actId['id']
            default = {
                "id": 0,
                "prevActId": int(prevActId),
                "suggestedActId": id,
                "score": 0
            }
            cursor = conn.execute(
                f"SELECT * FROM activityScore WHERE prevActId={prevActId} AND suggestedActId={id}")
            res = cursor.fetchone()
            if res != None:
                result.append(res)
            else:
                result.append(default)

        result = sorted(result, key=lambda x: x['score'], reverse=True)

        return Response(json.dumps(result), mimetype='application/json')


# @module.route(baseUrl+'create/<suggestedActId>')
def create(dbConnection, prevActId, suggestedActId):
    try:
        conn = dbConnection
        conn.execute(
            f"INSERT INTO activityScore (prevActId,suggestedActId,score) VALUES ({prevActId},{suggestedActId},1)")
        conn.commit()
        return Response(status=201)
    except Exception:
        return Exception


@module.route(baseUrl+'increment/<suggestedActId>')
def update(orgId, deptId, prevActId, suggestedActId):
    with sql.connect(dbUtil.connectionString) as conn:
        try:
            conn.row_factory = dbUtil.dict_factory
            cursor = conn.execute(
                f"SELECT * FROM activityScore WHERE prevActId={prevActId} AND suggestedActId={suggestedActId}")
            res = cursor.fetchone()
            print(res)
            if res == None:
                create(conn, prevActId, suggestedActId)
                print('yoo')
                return Response(status=201)
            res['score'] += 1
            conn.execute(
                f"UPDATE activityScore SET score={res['score']} WHERE prevActId={prevActId} AND suggestedActId={suggestedActId}")
            conn.commit()
            return Response(status=201)
        except Exception:
            return Exception


@module.route(baseUrl+'decrement/<suggestedActId>')
def updateD(orgId, deptId, prevActId, suggestedActId):
    with sql.connect(dbUtil.connectionString) as conn:
        try:
            conn.row_factory = dbUtil.dict_factory
            cursor = conn.execute(
                f"SELECT * FROM activityScore WHERE prevActId={prevActId} AND suggestedActId={suggestedActId}")
            res = cursor.fetchone()
            if res == None:
                return Response(status=201)
            res['score'] -= 1
            conn.execute(
                f"UPDATE activityScore SET score={res['score']} WHERE prevActId={prevActId} AND suggestedActId={suggestedActId}")
            conn.commit()
            return Response(status=201)
        except Exception:
            return Exception
