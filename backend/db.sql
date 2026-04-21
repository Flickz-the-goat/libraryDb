USE library_db;

DROP TABLE CheckoutStatus;
DROP TABLE Checkout;
DROP TABLE Book;
DROP TABLE StudentUser;
DROP TABLE GeneralUser;
DROP TABLE Library;
DROP TABLE AUser;

CREATE TABLE AUser(
    UserID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Email VARCHAR(100) UNIQUE,
    AccountCreationDate DATE,
    AccountStatus VARCHAR(30),
    WarningCount INT,
    CHECK (AccountStatus IN ('Active', 'Suspended', 'Terminated'))
);

CREATE TABLE StudentUser(
    UserID INT PRIMARY KEY, 
    UniversityID VARCHAR(50) NOT NULL, 
    Major VARCHAR(100), 
    FOREIGN KEY (UserID) REFERENCES AUser(UserID)
);

CREATE TABLE GeneralUser(
    UserID INT PRIMARY KEY,
    MembershipType VARCHAR(100),
    ExpirationDate DATE,
    FOREIGN KEY (UserID) REFERENCES AUser(UserID)
);

CREATE TABLE Library (
    LibraryID INT PRIMARY KEY,
    LibraryName VARCHAR(100),
    Address VARCHAR(100),
    City VARCHAR(50),
    State VARCHAR(30),
    ContactInfo VARCHAR(100)
);

CREATE TABLE Book (
    BookID INT PRIMARY KEY,
    LibraryID INT, 
    Title VARCHAR(100),
    ISBN VARCHAR(200) UNIQUE,
    Genre VARCHAR(30),
    LanguageUsed VARCHAR(20),
    PublicationYear INT, 
    Publisher VARCHAR(100),
    NumPages INT,
    Summary VARCHAR(1000),
    AvailabilityStatus VARCHAR(100),
    AuthorFirstName VARCHAR(50),
    AuthorLastName VARCHAR(50), 
    FOREIGN KEY (LibraryID) REFERENCES Library(LibraryID),
    CHECK (NumPages > 0),
    CHECK (AvailabilityStatus IN ('Available', 'CheckedOut', 'OnHold'))
);

CREATE TABLE Checkout (
    CheckoutID INT PRIMARY KEY,
    UserID INT NOT NULL,
    BookID INT NOT NULL,
    CheckoutDate DATE NOT NULL,
    RenewalCount INT DEFAULT 0,
    FOREIGN KEY (UserID) REFERENCES AUser(UserID),
    FOREIGN KEY (BookID) REFERENCES Book(BookID),
    CHECK (RenewalCount >= 0)
);

CREATE TABLE CheckoutStatus (
    CheckoutID INT PRIMARY KEY,
    Status VARCHAR(40),
    FineAmount DECIMAL(10,2) DEFAULT 0.00,
    DueDate DATE NOT NULL,
    ReturnDate DATE,
    FOREIGN KEY (CheckoutID) REFERENCES Checkout(CheckoutID),
    CHECK (Status IN ('Active', 'Returned', 'Overdue')),
    CHECK (FineAmount >= 0)
);

INSERT INTO AUser VALUES 
(379, 'Bob', 'Stookey', 'bstookey@email.com', '2016-11-11', 'Active', 1),
(473, 'John', 'Doe', 'jdoe@email.com', '2013-07-21', 'Active', 0),
(247, 'Clam', 'Don', 'cdon@email.com', '1999-04-18', 'Terminated', 4);

INSERT INTO StudentUser VALUES (379, 'GMU', 'Computer Science'); 

INSERT INTO GeneralUser VALUES (473, 'Engineer', '2023-12-31');

INSERT INTO Library VALUES
(3734, 'East Broad Library', '637 East Broad Street', 'Arlington', 'VA', '513-996-3792'),
(5984, 'Hawksworth Baltimore Library', '556 MLK Driveway', 'Baltimore', 'MD', '467-927-8394');

INSERT INTO Book VALUES
(27, 3734, 'How to Row a Boat', '978-0-452-28423-4', 'Tutorial', 'English', 1998, 'RowBoaters INC.', 187, '', 'Available', 'Francis', 'Belview'),
(37, 5984, 'The Avalanche', '978-1-4028-9462-6', 'Fiction', 'English', 2003, 'ABCBookProductions.', 244, '', 'CheckedOut', 'Chris', 'Johnson');

INSERT INTO Checkout VALUES
(676, 379, 27, '2018-05-05', 0),
(449, 473, 37, '2018-03-27', 2),
(567, 247, 27, '2018-08-12', 0);

INSERT INTO CheckoutStatus VALUES
(449, 'Overdue', 10.00, '2018-04-27', '2018-05-27');
