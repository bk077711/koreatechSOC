# file name : __init__.py
from flask import Flask, request, redirect, url_for
from flask import render_template
from project import db_connect
from project import apiCall
# 가나다라마바사
app = Flask(__name__, static_folder='static', static_url_path='/static')

@app.route("/")
def hello():
    return render_template("home.html")

@app.route("/home")
def home():
    return redirect("/")

@app.route("/introduction")
def introduction() :
    return render_template("introduction.html")

@app.route("/location")
def search_list():
    return render_template("index.html")

@app.route("/post", methods=['post'])
def post():
    value = request.form['input']
    return redirect("/location/" + value)

@app.route("/location/<value>")
def findFishing(value) :
    info = apiCall.apiCall()
    FFF = info.fishFind(value)
    fish_dict ={}
    for j in FFF:
        fish_dict[j['fname']] = [j['flatitude'], j['flongitude']]

    return render_template("index_list.html", data = FFF, location = value, fdic = fish_dict
                           #,temp=info.getData('temp'), fishList=info.getData('fishList')
                           )

if __name__ == "__main__":
    app.run()