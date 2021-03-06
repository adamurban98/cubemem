from flask import Flask
from flask import request
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
    args = request.args
    return '<pre>'+'<br>'.join(['Hello, Adam!'] + [f'{k:50}: {v}' for k,v in args.items()])


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))