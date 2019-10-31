from flask import Flask
from api.organisation import organisation
from api.department import department

app = Flask(__name__)
app.register_blueprint(organisation)
app.register_blueprint(department)

@app.route('/')
def helloo():
    return f'Hello,!'

@app.route('/test')
def hello():
    return f'test'

@app.route('/hello/<a>')
def s(a):
    return f'hello, {a}'