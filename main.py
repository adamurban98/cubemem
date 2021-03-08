from flask import Flask
from flask import request, render_template, url_for, session, redirect, jsonify
from datetime import timedelta
import random
from cube import Cube, DEFAULT_CUBECODE
from solution import Solution

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'adamka'

@app.route('/')
def hello_world():
    print(app.static_folder)
    print(app.static_url_path)
    return redirect(url_for('cube'))

@app.route('/cube')
def cube():
    cubecode = request.args.get('cubecode', DEFAULT_CUBECODE) 
    cubecode_userinput = request.args.get('cubecode-userinput', None)

    if cubecode_userinput:
        session['shuffle'] = None
    
    if cubecode_userinput is not None:
        cubecode = ''.join([c for c in cubecode_userinput if c in 'wbogry'])
        return redirect(url_for('cube', cubecode=cubecode))
    else:
        cube = Cube(cubecode)
        return render_template('cube.html', cube=cube)

@app.route('/shuffle')
def shuffle():
    shuffle = ''.join([random.choice('RrLlUuDdBbFf') for i in range(8)])
    session['shuffle'] = shuffle
    return render_template('cube.html', cube=Cube().moves(shuffle), shuffle=shuffle)



@app.route('/move')
def move():    
    cubecode = request.args.get('cubecode', DEFAULT_CUBECODE)
    moves = request.args.get('moves', 'U')

    session['shuffle'] = None

    cube = Cube(cubecode).moves(moves)

    return redirect(url_for('cube', cubecode=cube.cubecode))
    return render_template('cube.html', cube=cube)

@app.route('/solution')
def solution():    
    cubecode = request.args.get('cubecode', DEFAULT_CUBECODE)
    cube = Cube(cubecode)
    solution = Solution.solve(cube)
    
    return render_template('solution.html', solution=solution, zip=zip)


@app.route('/_parse-cubecode-userinput')
def _verify_userinput():
    cubecode_userinput = request.args.get('userinput', None)

    print(list(request.args.items()))
    print(list(request.form.items()))
    if cubecode_userinput is not None:
        cubecode = ''.join([c for c in cubecode_userinput if c in 'wbogry'])

        if len(cubecode) > 3*3*6:
            return jsonify(valid=False,message='Input too long.')
        elif len(cubecode) < 3*3*6:
            return jsonify(valid=False,message='Input too short.')
        else:
            return jsonify(valid=True, cubecode=cubecode, message='Input OK.')

    else:
        return jsonify(valid=False,message='No userinput provided.')




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
