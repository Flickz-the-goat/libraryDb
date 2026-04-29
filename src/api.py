from flask import Flask
from flask import request 
from db_funcs import *

app = Flask(__name__)


# Set up routes 
@app.route("/user/<email>", methods=['GET'])
def get_user(email):
    return {"user": getUser(email)}

@app.route("/library/<libraryName>", methods=['GET'])
def get_library(libraryName):
    return {"library": getLibrary(libraryName)}

@app.route("/searchBooks/<int:libraryId>", methods=['GET'])
def get_all_books(libraryId):
    books = getAllBooks(libraryId)
    return {"books": books}

@app.route("/searchBooks/<int:libraryId>/<int:bookId>", methods=["GET"])
def get_book(libraryId, bookId):
    book = getBook(libraryId, bookId)

    return {"book": book}

# Checkout a specific book routes
@app.route("/checkout/<int:libraryId>/<int:bookId>/<int:userId>")
def create_checkout(libraryId, bookId, userId):
    # check availability
    book = getBook(libraryId, bookId)
    
    status = book.get("AvailabilityStatus") 
    print(status)
    if status != "Available":
        return {"error_msg": "Book checkout out", "book": book}

    checkout = createCheckout(bookId, userId) 
    
    return {"checkedOutBook": checkout}

# Return Book
@app.route("/checkout/return/<int:checkoutId>", methods=[GET])
def return_book(checkoutId):
    book = returnBook(checkoutId)
    
    return {"book": book}

#View User Checkouts: 
@app.route("/user/checkouts/<int:userId>", methods=["GET"])
def get_user_checkouts(userId):
    userCheckouts = getUserCheckouts(userId)
    
    return {"userCheckouts": userCheckouts}
if __name__ == "__main__":
    app.run()
