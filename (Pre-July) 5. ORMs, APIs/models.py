# Create classes that interacts with SQL database
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Flight is inheriting from the model of db. Allows Flight class to interact
# with the db database
class Flight(db.Model):
    # class Flight corresponds to the "flights" table name
    __tablename__ = "flights"
    id = db.Column(db.Integer, primary_key=True)
    # nullable=False means not null
    origin = db.Column(db.String, nullable=False)
    destination = db.Column(db.String, nullable=False)
    duration = db.Column(db.Integer, nullable=False)


class Passenger(db.Model):
    __tablename__ = "passengers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    # this foreign key is a col of this table that is referencing a column
    # of another table. Particularly, the id col of flights table (flights.id)
    flight_id = db.Column(db.Integer, db.ForeignKey("flights.id"), nullable=False)
