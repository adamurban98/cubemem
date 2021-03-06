from flask import Flask
from flask import request, render_template, url_for, session, redirect, jsonify
from datetime import timedelta
import random
from cube import Cube, DEFAULT_CUBECODE

app = Flask(__name__)
app.secret_key = 'adamka'
app.permanent_session_lifetime = timedelta(seconds=10)

@app.route('/')
def hello_world():
    return redirect(url_for('cube'))

@app.route('/cube')
def cube():
    cubecode = request.args.get('cubecode', DEFAULT_CUBECODE) 
    cubecode_userinput = request.args.get('cubecode-userinput', None)
    
    if cubecode_userinput is not None:
        cubecode = ''.join([c for c in cubecode_userinput if c in 'wbogry'])
        return redirect(url_for('cube', cubecode=cubecode))
    else:
        cube = Cube(cubecode)
        return render_template('cube.html', cubecode=cube.cubecode, cube_color=cube.colors, cube_label={})


@app.route('/move')
def move():    
    cubecode = request.args.get('cubecode', DEFAULT_CUBECODE)
    moves = request.args.get('moves', 'U')

    cube = Cube(cubecode).moves(moves)

    return redirect(url_for('cube', cubecode=cube.cubecode))
    print(cube.strickers)
    return render_template('cube.html', cube_color=cube.colors, cube_label=cube.strickers)


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
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
