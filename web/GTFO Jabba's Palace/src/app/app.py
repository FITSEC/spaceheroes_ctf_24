# This code was generated with Chat GPT using the prompt: "use this *Challenge Description* and give me a simple python
# flask app to show a welcome message and an image of Jabba


# Not sure what GTFO bin to use
from flask import Flask, render_template, request, make_response
import os

app = Flask(__name__)


# Landing page
@app.route('/')
def index():
    password = 'myfavoritedecoration'
    resp = make_response(render_template('index.html'))
    resp.set_cookie('jabba', password, samesite='None', secure=True)
    return resp


# A little trickery
@app.route('/robots.txt')
def nice_try():
    return render_template('nice-try.html')


# Login route
@app.route('/login', methods=['POST'])
def login():
    dest = request.form['destination']
    if dest == 'myfavoritedecoration':
        return render_template('myfavoritedecoration.html')
    else:
        return render_template('nice-try.html')


@app.route('/destination', methods=['POST'])
def check_password():
    password = request.form['password']
    if 'cat' in password or 'ls' in password:
        return render_template('no-read.html')
    elif 'jq -Rr . "flag.txt"' in password:
        try:
            command = 'ping -c 1 ' + password
            output = os.popen(command).read()
            print(command)
            return render_template('result.html', output=output)
        except Exception as e:
            error = "Ah, really close, have you tried anything with a J?"
            return render_template('result.html', error=error)
    else:
        return render_template('failure.html')


if __name__ == '__main__':
    app.run(debug=True)
