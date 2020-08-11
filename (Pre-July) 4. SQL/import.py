import csv
import os

from sqlalchemy import  create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open(flights.csv)
    render = csv.reader(f)
    # Where col 1 is origin, col 2 is destination, ...
    for o, dest, dur in reader:
        # :origin is a placeholder for origin, since the value is not yet known
        db.execute("INSERT INTO flights(origin, destination, duration) VALUES (:origin, :destination, :duration)",
            {"origin": o, "destination": dest, "duration": dur})
            #encased in {} is a python dict that tells the placeholder what to put in based on the reader
        print(f"Added flight from {o} to {dest} lasting {duration}")
    db.commit()

if __name__ == "__main__":
    main()