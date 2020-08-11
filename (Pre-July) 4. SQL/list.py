import os

#sqlalchemy is library to interact with databses
from sqlalchemy import  create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Object created by sqlalchemy to manage db using python
engine = create_engine(os.getenv("DATABASE_URL"))
# Creating a session
db = scoped_session(sessionmaker(bind=engine))

def main():
    # flights is a list of all the rows of the dataset
    flights = db.execute("SELECT origin, destination, duration FROM flights").fetchall()
    for flight in flights:
        print(f"{flight.origin} to {flight.destination}, {flight.duration} minutes.")

if __name__ == "__main__":
    main()

