import datetime

from flask import Flask, render_template

# Im making a new web application with this file's name 
# representing the application
app = Flask(__name__)

# Flask is desgned in terms of routes. "/" is to access the default route
# immediately below it
@app.route("/")
def index():
    now = datetime.datetime.now()
    new_year = now.month == 1 and now.day == 1
    return render_template("index.html", new_year=new_year)

#takes any string after / and associate it to variable "name"
@app.route("/<string:name>")
def hello(name):
    name = name.capitalize()
    return f"<h1>Hello, {name}!</h1>"

@app.route("/david")
def david():
    return "David is here tooo!??!!"

@app.route("/bye")
def bye():
    headline = "Goodbye!"
    return render_template("index.html", headline=headline)

@app.route("/loop")
def loop():
    names = ["Alice", "Bob", "Charlie"]
    return render_template("index.html", names=names)

@app.route("/more")
def more():
    return render_template("more.html")