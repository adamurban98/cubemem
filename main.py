from flask import Flask
from flask import request, render_template, url_for, session, redirect, jsonify, g
from datetime import timedelta
import random
from cube import Cube, DEFAULT_CUBECODE
from solution import Solution
from moves import s_to_c, c_to_s
import yaml
import logging
from collections import defaultdict

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'adamka'
app.logger.setLevel(logging.INFO)

@app.errorhandler(404)
def error(e):
    return render_template('error.html')

@app.route('/')
def hello_world():
    return redirect(url_for('cube'))


@app.before_request
def register_get_pref():
    
    defaults = dict(
        pref_b_dimension = True,
        pref_s_showletter = 'hover',
        pref_i_shufflen = 10,
    )
    
    def get_pref(key):
        if key in session:
            return session[key]
        elif key in defaults:
            return defaults[key]
        else:
            KeyError(key)

    g.get_pref = get_pref
        

@app.route('/preferences', methods=['GET', 'POST'])
def preferences():
    if request.method == 'POST':
        for k, v in request.form.items():
            processed_v = v
            if k.startswith('pref_i_'):
                processed_v = int(v)
            elif k.startswith('pref_f_'):
                processed_v = float(v)
            elif k.startswith('pref_b_'):
                processed_v = v not in ['False', '0', 'false']
            session[k] = processed_v
            app.logger.info(f"Preference {k:30} set to {processed_v}")

    
    next_page = request.args.get('next', False)
    if next_page:
        return redirect(next_page)

    return render_template('preferences.html')

mnemonics_data = yaml.load(open('mnemonics.yaml').read(), Loader=yaml.Loader)

@app.route('/mnemonics')
def mnemonics():
    return render_template('mnemonics.html', mnemonics=mnemonics_data)

@app.route('/cube')
def cube():
    cubecode = request.args.get('cubecode', DEFAULT_CUBECODE) 
    cubecode_userinput = request.args.get('cubecode-userinput', None)
    
    show_3d = request.args.get('show3d', False)
 
    g.c_to_s=c_to_s
    g.random=random
    g.str=str

    if cubecode_userinput is not None:
        cubecode = ''.join([c for c in cubecode_userinput if c in 'wbogry'])
        return redirect(url_for('cube', cubecode=cubecode))
    else:
        shuffle = session.get('shuffle', '')
        cube = Cube.create(cubecode)
        return render_template(
            'cube.html',
            cube=cube,
            show_3d=True,
            shuffle= ' '.join(c_to_s(list(shuffle))) if cube.cubestate_equal(Cube.create().moves(shuffle)) else None
        )

@app.route('/shuffle')
def shuffle():
    n = g.get_pref('pref_i_shufflen')
    shuffle = ''.join([random.choice('RrLlUuDdBbFf') for i in range(random.choice([n,n+1]))])
    session['shuffle'] = shuffle

    return redirect(
        url_for(
            'cube',
            cubecode=Cube.create().moves(shuffle).cubecode
            )
        )
    
@app.route('/move')
def move():    
    cubecode = request.args.get('cubecode', DEFAULT_CUBECODE)
    moves = request.args.get('moves', 'U')

    cube = Cube.create(cubecode).moves(moves)

    return redirect(url_for('cube', cubecode=cube.cubecode))

@app.route('/solution')
def solution():    
    cubecode = request.args.get('cubecode', DEFAULT_CUBECODE)
    cube = Cube.create(cubecode)
    solution = Solution.solve(cube)

    def get_mnemonic(que):
        que_lower = que.lower()
        mnemonic = mnemonics_data.get(que_lower, [{'name': que}])

        if mnemonic == []:
            mnemonic = [{'name': que}]

        return mnemonic[0]['name'] 

    g.get_mnemonic = get_mnemonic
    g.random = random
    g.str = str
    
    shuffle=session.get('shuffle', 'XX')
    shuffle= ' '.join(c_to_s(list(shuffle))) if cube.cubestate_equal(Cube.create().moves(shuffle)) else None
    
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
