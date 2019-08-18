from flask import Blueprint

print(__name__)
test = Blueprint('test', __name__)

@test.route('/')
def hello_world():
    return 'Hello World'