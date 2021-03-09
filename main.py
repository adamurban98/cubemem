from flask import Flask
from flask import request, render_template, url_for, session, redirect, jsonify, g
from datetime import timedelta
import random
from cube import Cube, DEFAULT_CUBECODE
from solution import Solution
from moves import s_to_c, c_to_s
import yaml

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'adamka'

@app.route('/')
def hello_world():
    return redirect(url_for('cube'))

@app.route('/mnemonics')
def mnemonics():
    return render_template('mnemonics.html', mnemonics=yaml.load(open('mnemonics.yaml').read()))

@app.route('/cube')
def cube():
    cubecode = request.args.get('cubecode', DEFAULT_CUBECODE) 
    cubecode_userinput = request.args.get('cubecode-userinput', None)
 
    g.c_to_s=c_to_s
    if cubecode_userinput is not None:
        cubecode = ''.join([c for c in cubecode_userinput if c in 'wbogry'])
        return redirect(url_for('cube', cubecode=cubecode))
    else:
        shuffle = session.get('shuffle', '')
        cube = Cube(cubecode)
        return render_template(
            'cube.html',
            cube=cube,
            shuffle= ' '.join(c_to_s(list(shuffle))) if cube==Cube().moves(shuffle) else None
        )

@app.route('/shuffle')
def shuffle():
    n = request.args.get('n', random.choice([6,7]), type=int)
    shuffle = ''.join([random.choice('RrLlUuDdBbFf') for i in range(n)])
    session['shuffle'] = shuffle

    return redirect(
        url_for(
            'cube',
            cubecode=Cube().moves(shuffle).cubecode
            )
        )
    
@app.route('/move')
def move():    
    cubecode = request.args.get('cubecode', DEFAULT_CUBECODE)
    moves = request.args.get('moves', 'U')

    cube = Cube(cubecode).moves(moves)

    return redirect(url_for('cube', cubecode=cube.cubecode))

@app.route('/solution')
def solution():    
    cubecode = request.args.get('cubecode', DEFAULT_CUBECODE)
    cube = Cube(cubecode)
    solution = Solution.solve(cube)

    shuffle=session.get('shuffle', 'XX')
    shuffle= ' '.join(c_to_s(list(shuffle))) if cube==Cube().moves(shuffle) else None
    
    g.zip = zip
    return render_template('solution.html', solution=solution, shuffle=shuffle)


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
