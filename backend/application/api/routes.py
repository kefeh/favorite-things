from application import app

print(__name__)

@app.route('/')
def hello_world():
    return 'Hello World'