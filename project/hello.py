from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello() :
    return 'hello world'

#http://127.0.0.1:5000/