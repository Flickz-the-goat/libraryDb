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
    createCheckout(bookId, userId) -> create a checkout for the book 
    createCheckoutStatus(checkoutId) -> create a checkout status entry for the checkout
    updateBookStatus(bookId, availabilityStatus) -> update the availability (CheckedOut) 

    View User Checkouts: 
    getUserCheckouts(userId) -> get checkouts for that user
    getUserCheckoutStatus(checkoutId) -> get the status of the checkouts for that user 
    getUserBooks(bookId) -> get all the books that the user has checked out

Functions: 
    *getUser(email)
    *getLibrary(libraryName)
    *getAllBooks(libraryId)
    *getBook(LibraryId, bookId)
    createCheckout(bookId, userId)
    createCheckoutStatus(checkoutId)
    updateBookStatus(bookId, availabilityStatus)
    *getUserCheckouts(userId)
    getUserBooks(userId)
"""

def getUser(email):
    with cnx.cursor() as cursor: 
        query = f"select * from AUser where Email = \'{email}\' limit 1" 
        res = cursor.execute(query)
        
        return cursor.fetchone() 

def getLibrary(libraryName): 
    with cnx.cursor() as cursor: 
        query = f"select * from Library where LibraryName = \'{libraryName}\' limit 1"
        res = cursor.execute(query)

        return cursor.fetchone() 

def getAllBooks(libraryId):
    with cnx.cursor() as cursor:
        query = f"select * from Book where LibraryId = {libraryId}"
        res = cursor.execute(query)

        return cursor.fetchall() 

def getBook(libraryId, bookId):
    with cnx.cursor() as cursor: 
        query = f"select * from Book where LibraryId = {libraryId} and BookID = {bookId} limit 1" 
        res = cursor.execute(query) 
        
        return cursor.fetchone() 

def getUserCheckouts(userId):
    query = f"select * from Checkout c join CheckoutStatus s on c.CheckoutID = s.CheckoutID join Book b on c.BookID = b.BookID where userId = {userId}"
    with cnx.cursor() as cursor: 
        res = cursor.execute(query)

        return cursor.fetchall()

def main():
    user = getUser("jdoe@email.com")
    lib = getLibrary("East Broad Library")
    books = getAllBooks(lib[0])
    book = getBook(lib[0], books[0][0])
    print(user[0])
    userBooks = getUserCheckouts(user[0])

    print("User:", user)
    print("Library: ", lib)
    print("Books: \n", books)
    print("Singular book: ", book)
    print("User checked out Books: \n", userBooks)

if __name__ == "__main__":
    main()

cnx.close() 


