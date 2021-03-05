from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/')
def hello_world():
    args = request.args
    return '<pre>'+'<br>'.join(['Hello, World!'] + [f'{k:50}: {v}' for k,v in args.items()])



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

