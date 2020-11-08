from flask import Flask, redirect, url_for
app = Flask(__name__)

@app.route('/')
def main() :
    return 'welcome'

@app.route('/admin')
def hello_admin() :
    return 'hello Admin'

@app.route('/guest/<name>')
def hello_guest(name) :
    return 'hello %s as Guset' % name
@app.route('/user/<name>')
def user(name) :
    if name == 'admin' :
        return redirect(url_for('hello_admin'))
    else :
        return redirect(url_for('hello_guest', name = name))

if __name__== '__main__' :
    app.run(debug=True)
#http://127.0.0.1:5000/