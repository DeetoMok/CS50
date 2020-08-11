from flask import Flask, render_template, request, session
from flask_session import Session

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("indexForm.html")


#allow request method of POST and GET
@app.route("/hello", methods=["GET", "POST"])
def hello():
    if request.method == "GET":
        return "Please submit the form instead."
    else:
        # "name" here is from the "name" of name="name" in indexForm.html 
        name = request.form.get("name")
        return render_template("hello.html", name=name)