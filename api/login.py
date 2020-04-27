import sqlite3 as sql
import json
from flask import Blueprint, abort, request, Response
import db.dbUtil as dbUtil

login = Blueprint("login", __name__)

module = login


# CRUD
baseUrl = "/api/login/"

@module.route(baseUrl, methods = ['POST','GET'])
def dologin():
    if request.method == 'POST':
        return Response(status=200)
    return Response(status=200)