import os
import requests

from flask import Flask, session, render_template, request, redirect, url_for, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.secret_key = "b'\\xfe\\xb2\\x1f\\xa1V\\x9d\\x89\\x9f6\\xa6\\x88<k(\\xd7\\xcf\\xd1\\xbc\\xc0\\xc5\\xd0\\xf5\\xf9b'"

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    if "user" in session:
        user = session["user"]
        return render_template("aboutPage.html", name=user)
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return redirect(url_for("index"))
    else:
        name = request.form.get("name")
        password = request.form.get("password")
        if db.execute("SELECT * FROM users WHERE username = :username", {"username": name}).rowcount == 0:
            return render_template("error.html", message="Incorrect username")
        result = db.execute("SELECT * FROM users WHERE username = :username", {"username": name}).fetchone()
        
        password_check = check_password_hash(result.password, password)
        # if db.execute("SELECT * FROM users WHERE password = :password", {"password": password}).rowcount == 0:
        #     return render_template("error.html", message="Incorrect password")
        if password_check:
            session['user'] = name
            return render_template("aboutPage.html", name=name)
        else:
            return render_template("error.html", message="Incorrect password")

@app.route("/aboutPage", methods=["GET", "POST"])
def aboutPage():
    if "user" in session:
        user = session["user"]
        return render_template("aboutPage.html", name=user)
    else:
        return redirect(url_for("login"))

@app.route("/create-account", methods=["GET", "POST"])
def create():
    return render_template("create-account.html")

@app.route("/confirm", methods=["GET", "POST"])
def confirm():
    if request.method == "GET":
        return "Please submit the form instead."
    else:
        firstName = request.form.get("first-name")
        lastName = request.form.get("last-name")
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        confirmPassword = request.form.get("confirm-password")
        if password != confirmPassword:
            errorMessage = "Passwords do not match"
            return render_template("create-account.html", errorMessage=errorMessage)
        if db.execute("SELECT * FROM users WHERE email = :email", {"email": email}).rowcount == 1:
            errorMessage = "The email has already been used, please use another email address"
            return render_template("create-account.html", errorMessage=errorMessage)
        if db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).rowcount == 1:
            errorMessage = "This username is unavailable, please try another"
            return render_template("create-account.html", errorMessage=errorMessage)

        hash_password = generate_password_hash(password)

        db.execute("INSERT INTO users (firstName, lastName, email, username, password) VALUES (:firstName, :lastName, :email, :username, :password)",
            {"firstName": firstName, "lastName": lastName, "email": email, "username": username, "password": hash_password})
        db.commit()
        return render_template("confirm.html", firstName=firstName, lastName=lastName, email=email, username=username, password=password)

@app.route("/search", methods=["GET", "POST"])
def search():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "GET":
        return render_template("search.html")

    search = request.form.get("search")
    search = '%' + search + '%'
    if db.execute("SELECT * FROM books WHERE UPPER(isbn) LIKE UPPER(:search) OR UPPER(title) LIKE UPPER(:search) OR UPPER(author) LIKE UPPER(:search) OR CAST(year AS VARCHAR) LIKE :search", 
                    {"search": search}).rowcount > 0:
        books = db.execute("SELECT * FROM books WHERE UPPER(isbn) LIKE UPPER(:search) OR UPPER(title) LIKE UPPER(:search) OR UPPER(author) LIKE UPPER(:search) OR CAST(year AS VARCHAR) LIKE :search",
                             {"search": search}).fetchall()
        return render_template("found.html", books = books) 
    return render_template("error.html", message="Unable to find search key-word")

@app.route("/<string:isbn_no>")
def book(isbn_no):
    if "user" not in session:
        return redirect(url_for("login"))
    user = session["user"]
    search = isbn_no
    book = db.execute("SELECT * FROM books WHERE isbn = :search", {"search": search}).fetchone()
    if book is None:
        return render_template("error.html", message="No such book exists.")

    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "xGXcpQuOtYENInyZGLXuQ", "isbns": search})
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")
    data = res.json()
    ratingCounts = data["books"][0]["ratings_count"]
    reviewCounts = data["books"][0]["reviews_count"]
    rating = data["books"][0]["average_rating"]

    bookId = book.id
    # Retrieve review info
    reviewInfo = db.execute("SELECT * FROM reviews JOIN books ON reviews.books_id=books.id JOIN users ON reviews.users_id=users.id WHERE reviews.books_id=:bookId", {"bookId": bookId}).fetchall()
    reviewed_book = db.execute("SELECT * FROM reviews JOIN books ON reviews.books_id=books.id JOIN users ON reviews.users_id=users.id WHERE reviews.books_id=:bookId AND users.username=:user", {"bookId": bookId, "user":user}).rowcount > 0
    return render_template("book.html", book=book, rating=rating, ratingCounts=ratingCounts, reviewCounts=reviewCounts, reviewInfo=reviewInfo, reviewed_book=reviewed_book)

@app.route("/review/<book_id>", methods=["GET", "POST"])
def review(book_id):
    if "user" not in session:
        return redirect(url_for("login"))
    review_text = request.form.get("review")
    review_score = request.form.get("rating")
    user = session['user']
    isbn_no_tuple = db.execute("SELECT isbn FROM books WHERE id=:book_id", {"book_id": book_id}).fetchone()
    isbn_no = isbn_no_tuple[0]
    user_id_tuple = db.execute("SELECT users.id FROM users WHERE users.username = :user", {"user": user}).fetchone()
    user_id_value = user_id_tuple[0]
    db.execute("INSERT INTO reviews (review_text, review_score, books_id, users_id) VALUES (:review_text, :review_score, :book_id, :user_id)",
        {"review_text": review_text, "review_score": review_score, "book_id": book_id, "user_id": user_id_value})
    db.commit() 
    # return render_template("error.html", message=isbn_no)
    return redirect(url_for("book", isbn_no=isbn_no))

@app.route("/logout")
def logout():
    # Remove "user" from session
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/api_access")
def api_access():
    if "user" not in session:
        return redirect(url_for("login"))    
    return render_template("api.html")

@app.route("/api/<isbn>")
def api(isbn):

    result = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()

    if result is None:
        return jsonify({
            "message": "error 404 - This book isbn No. is not in the database."
        })

    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "xGXcpQuOtYENInyZGLXuQ", "isbns": isbn})
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")
    data = res.json()
    ratingCounts = data["books"][0]["ratings_count"]
    reviewCounts = data["books"][0]["reviews_count"]
    rating = data["books"][0]["average_rating"]
    # res = requests.get("https://www.goodreads.com/book/review_counts.json",
    #                    params={"key": "xGXcpQuOtYENInyZGLXuQ", "isbns": isbn})

    return jsonify({
        "title": result.title,
        "author": result.author,
        "year": result.year,
        "isbn": result.isbn,
        "review_count": reviewCounts,
        "average_score": rating
    })

