from flask import Flask
from flask_cors import CORS
from api.organisation import organisation
from api.department import department
from api.activity import activity
from api.activityScore import activityScore

app = Flask(__name__)
CORS(app)
app.register_blueprint(organisation)
app.register_blueprint(department)
app.register_blueprint(activity)
app.register_blueprint(activityScore)

@app.route('/')
def helloo():
    return f'Hello,!'

@app.route('/test')
def hello():
    return f'test'

@app.route('/hello/<a>')
def s(a):
    return f'hello, {a}'