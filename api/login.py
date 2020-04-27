import sqlite3 as sql
import json
from flask import Blueprint, abort, request, Response
import db.dbUtil as dbUtil

login = Blueprint("login", __name__)

module = login


# CRUD
baseUrl = "/api/login/"