from flask import Flask, redirect, url_for
app = Flask(__name__)

@app.route('/')
def main() :
    return 'hello world'

@app.route('/user')

@app.route('/user/<name>')
def user(name) :
    if name == 'admin' :
        return redirect(url_for('hello_admin'))
    else :
        return redirect(url_for('hello_guest', guset = name))
#http://127.0.0.1:5000/