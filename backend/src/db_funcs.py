import mysql.connector

cnx = mysql.connector.connect(user='flickz', password='animanlevel7',
                              host='127.0.0.1', database='library_db')

"""
Capabilities list: 
    Search Books, 
    Checkout Book, 
    View User Checkouts

App Logic: 
    Check what use u are logged in as (getUser) 
    Check what Library you are in (getLibrary) 
    Get all the books from that library (getAllBooks(libraryID)) 
    Get a specific book from the books (getBook(libraryID, bookID))

    Checkout a specific book: 
    getBook(libraryId, bookId) -> check availability 
    createCheckout(bookId, userId) -> create a checkout for the book, and update book availability 

    View User Checkouts: 
    getUserCheckouts(userId) -> get checkouts for that user
    getUserBooks(bookId) -> get all the books that the user has checked out

Functions: 
    *getUser(email)
    *getLibrary(libraryName)
    *getAllBooks(libraryId)
    *getBook(LibraryId, bookId)
    *createCheckout(bookId, userId)
    *updateBookStatus(bookId, availabilityStatus)
    *getUserCheckouts(userId)
"""
book_keys = ("BookID", "LibraryID", "Title", "ISBN", "Genre", "LanguageUsed", "PublicationYear", "Publisher", "NumPages", "Summary", "AvailabilityStatus", "AuthorFirstName", "AuthorLastName")

user_keys = ("UserID", "FirstName", "LastName", "Email", "AccountCreationDate", "AccountStatus", "WarningCount")

library_keys = ("LibraryID", "LibraryName", "Address", "City", "State", "ContactInfo")

checkout_keys = ("CheckoutID", "UserID", "BookID", "CheckoutDate", "RenewalCount", "CheckoutID", "Status", "FineAmount", "DueDate", "ReturnDate", "BookID", "LibraryID", "Title", "ISBN", "Genre", "LanguageUsed", "PublicationYear", "Publisher", "NumPages", "Summary", "AvailabilityStatus", "AuthorFirstName", "AuthorLastName")

def getUser(email):
    cnx = mysql.connector.connect(user='flickz', password='animanlevel7',
                              host='127.0.0.1', database='library_db')

    with cnx.cursor() as cursor: 
        query = f"select * from AUser where Email = \'{email}\' limit 1" 
        res = cursor.execute(query)
        user = dict(zip(user_keys, cursor.fetchone()))     
        return user

def getLibrary(libraryName): 
    cnx = mysql.connector.connect(user='flickz', password='animanlevel7',
                              host='127.0.0.1', database='library_db')

    with cnx.cursor() as cursor: 
        query = f"select * from Library where LibraryName = \'{libraryName}\' limit 1"
        res = cursor.execute(query)
        library = dict(zip(library_keys, cursor.fetchone()))
        return library

def getAllBooks(libraryId):
    cnx = mysql.connector.connect(user='flickz', password='animanlevel7',
                              host='127.0.0.1', database='library_db')

    with cnx.cursor() as cursor:
        query = f"select * from Book where LibraryId = {libraryId}"
        res = cursor.execute(query)
        books = cursor.fetchall() 

        return [dict(zip(book_keys, book)) for book in books]

def getBook(libraryId, bookId):
    cnx = mysql.connector.connect(user='flickz', password='animanlevel7',
                              host='127.0.0.1', database='library_db')

    with cnx.cursor() as cursor: 
        query = f"select * from Book where LibraryId = {libraryId} and BookID = {bookId} limit 1" 
        res = cursor.execute(query) 
        book = cursor.fetchone()
        book = dict(zip(book_keys, book))
        
        return book

def getUserCheckouts(userId):
    cnx = mysql.connector.connect(user='flickz', password='animanlevel7',
                              host='127.0.0.1', database='library_db')

    query = f"select * from Checkout c join CheckoutStatus s on c.CheckoutID = s.CheckoutID join Book b on c.BookID = b.BookID where userId = {userId}"
    with cnx.cursor() as cursor: 
        res = cursor.execute(query)
        
        checkouts = cursor.fetchall()
        return [dict(zip(checkout_keys, checkout)) for checkout in checkouts]

def updateBookStatus(bookId, status):
    cnx = mysql.connector.connect(user='flickz', password='animanlevel7',
                              host='127.0.0.1', database='library_db')

    query = f"update Book set AvailabilityStatus = %s where BookID = {bookId}"
    vals = status
    with cnx.cursor() as cursor:
        cursor.execute(query, (vals,))
        cnx.commit()

def createCheckout(bookId, userId):
    cnx = mysql.connector.connect(user='flickz', password='animanlevel7',
                              host='127.0.0.1', database='library_db')

    query = """insert into Checkout (UserID, BookID, RenewalCount) values (%s, %s, %s)"""
    vals = (userId, bookId, 0)

    with cnx.cursor() as cursor: 
        cursor.execute(query, vals)
        checkoutId = cursor.lastrowid

        query = "insert into CheckoutStatus (CheckoutID, Status, DueDate) values (%s, %s, DATE_ADD(CURRENT_DATE, INTERVAL 30 DAY))"
        vals = (checkoutId, 'Active')

        cursor.execute(query, vals)
        cnx.commit() 
        
        updateBookStatus(bookId, "CheckedOut")

        res = cursor.execute(f"select * from Checkout c join CheckoutStatus s on c.CheckoutID = s.CheckoutID join Book b on c.BookID = b.BookID where c.CheckoutID = {checkoutId}")
        book = cursor.fetchone() 
        book = dict(zip(checkout_keys, book))
        return book

def returnBook(checkoutId):
    cnx = mysql.connector.connect(user='flickz', password='animanlevel7',
                              host='127.0.0.1', database='library_db')

    #Reference: query = f"update Book set AvailabilityStatus = %s where BookID = {bookId}"
    query = f"select * from Checkout where CheckoutID == {checkoutId}"

    with cnx.cursor() as cursor: 
        res = cursor.execute(query)
        checkout = cursor.fetchone()
        checkoutId = checkout[0]
        bookId = checkout[2]

        query = f"update CheckoutStatus set Status = %s, ReturnedDate = %s where CheckoutID = {checkoutId}"
        vals = ("Returned", "CURRENT_DATE")
        cursor.execute(query, vals)
        cnx.commit() 
        
        updateBookStatus(bookId, "Available")

        res = cursor.execute(f"select * from Book where BookID = {bookId}")
        book = cursor.fetchone() 
        book = dict(zip(book_keys, book))
        return book


def main():
    user = getUser("jdoe@email.com")
    lib = getLibrary("East Broad Library")

    print("User:", user)
    print("Library: ", lib)
    

if __name__ == "__main__":
    main()



