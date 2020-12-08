# file name : __init__.py
from flask import Flask, request
from flask import render_template
from project import db_connect
# 가나다라마바사
app = Flask(__name__)

@app.route("/")
def hello():
    info = "KKH"
    return render_template("index.html", data=info, uiui = "KDY")

@app.route("/list")
def search_list():
    return render_template("index_list.html")

@app.route("/post",methods=['post'])
def post():
    value = request.form['input']
    return render_template("index_list.html", data = value)

@app.route("/abc")
def hello2():
    a="{1:aa,2:bb}"
    return a

@app.route("/univ/<aaa>")
def hello3(aaa):
    a=aaa
    return a

@app.route("/message/<string:message_id>")
def get_message(message_id):
    print(type(message_id))
    return "message id: %s" % message_id

@app.route("/first/<int:messageid>")
def get_first(messageid):
    print(type(messageid))
    return "<h1>%d</h1>" % messageid + 5

@app.route("/<user>")
def test(user):
    return user

@app.route("/test")
def get_html():
    return render_template("view.html",aa='전달데이터',bb="1234", cc=[1,2,3])

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/hello/<user>")
def hello_name(user):
    return render_template("view.html",data=user, list=[1,2,3,4])

@app.route("/db")
def showDB() :
    db_class = db_connect.Database()

    sql = "select * from model"
    row = db_class.execute(sql)
    print(row)

    return render_template('index.html', resultData=row[0])

if __name__ == "__main__":
    app.run(debug=True)