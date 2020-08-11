# Creating Flask app that creates SQL db
import os

from flask import Flask, render_template, request
# from models.oy file, import everything
from models import *

app = Flask(__name__)
# Tells the app what database to use (I think right now the database URL not set?????)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Tie this database with this application
db.init_app(app)

def main():
    # create all SQL tables as written in python code
    db.create_all()

if __name__ == "__main__":
    with app.app_context():
        main()
