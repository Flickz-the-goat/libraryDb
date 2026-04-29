
from flask import Flask, render_template, request, redirect, url_for, session, flash
from db_funcs import (
    getUser, getLibrary, getAllBooks, getBook,
    createCheckout, returnBook, getUserCheckouts,
)

app = Flask(__name__)
app.secret_key = "lis-demo-secret"


@app.route("/", methods=["GET", "POST"])
def home():
    """Used to sign in by email."""
    if request.method == "POST":
        email = (request.form.get("email") or "").strip()
        library_name = (request.form.get("library") or "").strip()
        try:
            user = getUser(email)
            library = getLibrary(library_name)
            session["user_id"] = user["UserID"]
            session["user_name"] = f"{user['FirstName']} {user['LastName']}"
            session["library_id"] = library["LibraryID"]
            session["library_name"] = library["LibraryName"]
            return redirect(url_for("books"))
        except Exception as e:
            flash(f"Sign-in failed — check the email and library name. ({e})")
    return render_template("index.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


@app.route("/books")
def books():
    """Used to search books at the current library."""
    if "library_id" not in session:
        return redirect(url_for("home"))
    every_books = getAllBooks(session["library_id"])
    q = (request.args.get("q") or "").strip().lower()
    if q:
        def matches(b):
            h = " ".join(str(b.get(k) or "") for k in
                                ("Title", "AuthorFirstName", "AuthorLastName", "Genre"))
            return q in h.lower()
        every_books = [b for b in every_books if matches(b)]
    return render_template("books.html", books=every_books, q=q)


@app.route("/book/<int:book_id>")
def book(book_id):
    """used to single book detail page."""
    if "library_id" not in session:
        return redirect(url_for("home"))
    b = getBook(session["library_id"], book_id)
    return render_template("book.html", book=b)


@app.route("/checkout/<int:book_id>", methods=["POST"])
def checkout(book_id):
    """used to check the book out for the signed-in user."""
    if "user_id" not in session:
        return redirect(url_for("home"))
    b = getBook(session["library_id"], book_id)
    if b.get("AvailabilityStatus") != "Available":
        flash(f"'{b.get('Title')}' is not available right now.")
        return redirect(url_for("book", book_id=book_id))
    createCheckout(book_id, session["user_id"])
    flash(f"Checked out: {b.get('Title')}")
    return redirect(url_for("my_checkouts"))


@app.route("/my")
def my_checkouts():
    """used to see user's checkout history."""
    if "user_id" not in session:
        return redirect(url_for("home"))
    checkouts = getUserCheckouts(session["user_id"])
    return render_template("my_checkouts.html", checkouts=checkouts)


@app.route("/return/<int:checkout_id>", methods=["POST"])
def ret(checkout_id):
    """used to return a checked-out book."""
    if "user_id" not in session:
        return redirect(url_for("home"))
    try:
        returnBook(checkout_id)
        flash("Book returned.")
    except Exception as e:
        flash(f"Return failed: {e}")
    return redirect(url_for("my_checkouts"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
