USE library_db;

DROP TABLE IF EXISTS CheckoutStatus;
DROP TABLE IF EXISTS Checkout;
DROP TABLE IF EXISTS Book;
DROP TABLE IF EXISTS StudentUser;
DROP TABLE IF EXISTS GeneralUser;
DROP TABLE IF EXISTS Library;
DROP TABLE IF EXISTS AUser;

CREATE TABLE AUser(
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Email VARCHAR(100) UNIQUE,
    AccountCreationDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    AccountStatus VARCHAR(30),
    WarningCount INT DEFAULT 0,
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
    LibraryID INT AUTO_INCREMENT PRIMARY KEY,
    LibraryName VARCHAR(100),
    Address VARCHAR(100),
    City VARCHAR(50),
    State VARCHAR(30),
    ContactInfo VARCHAR(100)
);

CREATE TABLE Book (
    BookID INT AUTO_INCREMENT PRIMARY KEY,
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
    CheckoutID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    BookID INT NOT NULL,
    CheckoutDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    RenewalCount INT DEFAULT 0,
    FOREIGN KEY (UserID) REFERENCES AUser(UserID),
    FOREIGN KEY (BookID) REFERENCES Book(BookID),
    CHECK (RenewalCount >= 0)
);

CREATE TABLE CheckoutStatus (
    CheckoutID INT PRIMARY KEY,
    Status VARCHAR(40),
    FineAmount DECIMAL(10,2) DEFAULT 0.00,
    DueDate DATE,
    ReturnDate DATE,
    FOREIGN KEY (CheckoutID) REFERENCES Checkout(CheckoutID),
    CHECK (Status IN ('Active', 'Returned', 'Overdue')),
    CHECK (FineAmount >= 0)
);

-- USERS
INSERT INTO AUser (FirstName, LastName, Email, AccountStatus, WarningCount) VALUES
('Bob', 'Stookey', 'bstookey@email.com', 'Active', 1),
('John', 'Doe', 'jdoe@email.com', 'Active', 0),
('Clam', 'Don', 'cdon@email.com', 'Terminated', 4),
('Alice', 'Smith', 'asmith@email.com', 'Active', 0),
('Mark', 'Brown', 'mbrown@email.com', 'Suspended', 2);

INSERT INTO StudentUser VALUES 
(1, 'GMU001', 'Computer Science'),
(4, 'GMU002', 'Physics');

INSERT INTO GeneralUser VALUES 
(2, 'Premium', '2026-12-31'),
(3, 'Basic', '2025-06-30'),
(5, 'Standard', '2026-01-01');

-- LIBRARIES
INSERT INTO Library (LibraryName, Address, City, State, ContactInfo) VALUES
('East Broad Library', '637 East Broad Street', 'Arlington', 'VA', '513-996-3792'),
('Hawksworth Baltimore Library', '556 MLK Driveway', 'Baltimore', 'MD', '467-927-8394');

-- BOOKS (20+)
INSERT INTO Book (LibraryID, Title, ISBN, Genre, LanguageUsed, PublicationYear, Publisher, NumPages, Summary, AvailabilityStatus, AuthorFirstName, AuthorLastName) VALUES
(1,'How to Row a Boat','978-0-452-28423-4','Tutorial','English',1998,'RowBoaters INC.',187,'','Available','Francis','Belview'),
(2,'The Avalanche','978-1-4028-9462-6','Fiction','English',2003,'ABCBookProductions.',244,'','CheckedOut','Chris','Johnson'),
(1,'Database Systems','978-0-111-11111-1','Education','English',2015,'TechPress',500,'','Available','Alan','Smith'),
(1,'Graph Theory Basics','978-0-222-22222-2','Education','English',2018,'MathWorld',320,'','Available','Lisa','Ray'),
(2,'Modern Physics','978-0-333-33333-3','Science','English',2020,'SciPub',410,'','Available','Neil','Tyson'),
(2,'Linear Algebra','978-0-444-44444-4','Math','English',2012,'MathPub',280,'','Available','David','Lay'),
(1,'AI Fundamentals','978-0-555-55555-5','Technology','English',2021,'FutureTech',390,'','Available','Andrew','Ng'),
(2,'Operating Systems','978-0-666-66666-6','Technology','English',2017,'CompSciPub',600,'','Available','Andrew','Tanenbaum'),
(1,'Networking Basics','978-0-777-77777-7','Technology','English',2016,'NetPub',350,'','Available','James','Kurose'),
(2,'Data Mining','978-0-888-88888-8','Technology','English',2019,'DataPub',420,'','Available','Jiawei','Han'),
(1,'Cybersecurity 101','978-0-999-99999-9','Security','English',2022,'SecurePub',310,'','Available','Kevin','Mitnick'),
(2,'Cloud Computing','978-1-000-00000-0','Technology','English',2023,'CloudPub',330,'','Available','AWS','Amazon'),
(1,'Big Data Analytics','978-1-111-11111-1','Technology','English',2020,'DataPub',450,'','Available','Tom','White'),
(2,'Machine Learning','978-1-222-22222-2','Technology','English',2019,'MLPub',470,'','Available','Ian','Goodfellow'),
(1,'Deep Learning','978-1-333-33333-3','Technology','English',2021,'MLPub',550,'','Available','Yoshua','Bengio'),
(2,'Discrete Math','978-1-444-44444-4','Math','English',2014,'MathPub',300,'','Available','Kenneth','Rosen'),
(1,'Algorithms','978-1-555-55555-5','Technology','English',2013,'MITPress',700,'','Available','CLRS','Team'),
(2,'Computer Graphics','978-1-666-66666-6','Technology','English',2018,'GraphicsPub',380,'','Available','James','Foley'),
(1,'Game Development','978-1-777-77777-7','Technology','English',2020,'GamePub',290,'','Available','John','Doe'),
(2,'Software Engineering','978-1-888-88888-8','Technology','English',2015,'SEPub',410,'','Available','Roger','Pressman');

-- CHECKOUTS
INSERT INTO Checkout (UserID, BookID) VALUES
(1,1),(1,2),(1,3),
(2,4),(2,5),(2,6),
(3,7),(3,8),(3,9),
(4,10),(4,11),(4,12),
(5,13),(5,14),(5,15);

-- CHECKOUT STATUS (30-day due date)
INSERT INTO CheckoutStatus (CheckoutID, Status, DueDate, ReturnDate) VALUES
(1,'Returned', DATE_ADD(CURRENT_DATE, INTERVAL 30 DAY), CURRENT_DATE),
(2,'Active', DATE_ADD(CURRENT_DATE, INTERVAL 30 DAY), NULL),
(3,'Overdue', DATE_ADD(CURRENT_DATE, INTERVAL 30 DAY), NULL),

(4,'Returned', DATE_ADD(CURRENT_DATE, INTERVAL 30 DAY), CURRENT_DATE),
(5,'Active', DATE_ADD(CURRENT_DATE, INTERVAL 30 DAY), NULL),
(6,'Overdue', DATE_ADD(CURRENT_DATE, INTERVAL 30 DAY), NULL),

(7,'Returned', DATE_ADD(CURRENT_DATE, INTERVAL 30 DAY), CURRENT_DATE),
(8,'Active', DATE_ADD(CURRENT_DATE, INTERVAL 30 DAY), NULL),
(9,'Overdue', DATE_ADD(CURRENT_DATE, INTERVAL 30 DAY), NULL),

(10,'Returned', DATE_ADD(CURRENT_DATE, INTERVAL 30 DAY), CURRENT_DATE),
(11,'Active', DATE_ADD(CURRENT_DATE, INTERVAL 30 DAY), NULL),
(12,'Overdue', DATE_ADD(CURRENT_DATE, INTERVAL 30 DAY), NULL),

(13,'Returned', DATE_ADD(CURRENT_DATE, INTERVAL 30 DAY), CURRENT_DATE),
(14,'Active', DATE_ADD(CURRENT_DATE, INTERVAL 30 DAY), NULL),
(15,'Overdue', DATE_ADD(CURRENT_DATE, INTERVAL 30 DAY), NULL);
