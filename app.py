from flask import Flask
from api.organisation import organisation

app = Flask(__name__)
app.register_blueprint(organisation)

@app.route('/')
def helloo():
    return f'Hello,!'

@app.route('/test')
def hello():
    return f'test'

@app.route('/hello/<a>')
def s(a):
    return f'hello, {a}'