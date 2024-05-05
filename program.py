import pymongo
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from prettytable import PrettyTable

# MongoDB connection parameters
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
DATABASE_NAME = 'Library'
STAFF_DATABASE_NAME = 'staff'

# Connect to MongoDB
client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
db = client[DATABASE_NAME]
staff_db = client[STAFF_DATABASE_NAME]

# Collection names
BOOKS_COLLECTION = 'books'
MEMBERS_COLLECTION = 'members'
TRANSACTIONS_COLLECTION = 'transactions'

# Function to authenticate staff login
def login(username, password):
    staff = staff_db['users'].find_one({"username": username, "password": password})
    if staff:
        return staff
    else:
        return None

# Function to edit a book's details (admin only)
def edit_book(book_id):
    book = db[BOOKS_COLLECTION].find_one({"_id": ObjectId(book_id)})
    if book:
        print("Current book details:")
        display_books([book])  # Display current book details
        print("Enter new details (leave blank to keep current):")
        new_title = input(f"Title ({book['title']}): ") or book['title']
        new_author = input(f"Author ({book['author']}): ") or book['author']
        new_genre = input(f"Genre ({book['genre']}): ") or book['genre']
        new_ISBN = input(f"ISBN ({book['ISBN']}): ") or book['ISBN']
        new_publication_year = input(f"Publication Year ({book['publication_year']}): ") or book['publication_year']
        new_quantity = input(f"Quantity ({book['quantity']}): ") or book['quantity']
        
        # Update book details
        db[BOOKS_COLLECTION].update_one(
            {"_id": ObjectId(book_id)},
            {"$set": {
                "title": new_title,
                "author": new_author,
                "genre": new_genre,
                "ISBN": new_ISBN,
                "publication_year": new_publication_year,
                "quantity": new_quantity
            }}
        )
        print("Book details updated successfully.")
    else:
        print("Invalid book ID.")


# Function to get books based on staff permissions
def get_books(staff_permission):
    books = []
    if staff_permission == 1:  # Admin
        books = db[BOOKS_COLLECTION].find()
    elif staff_permission == 0:  # Teller
        books = db[BOOKS_COLLECTION].find({"quantity": {"$gt": 0}})
    return books

# Function to display available commands
def display_commands():
    print("Available commands:")
    print("0: Add a book")
    print("1: Add a member")
    print("2: Create a transaction")
    print("3: View books")
    print("4: View transactions")
    print("5: View transaction history")
    print("6: View members")
    print("7: Edit a book's details")
    print("8: Sign out")


# Function to view books with subcommands
def view_books():
    subcommand = input("Enter the subcommand number (0: All books, 1: Books owned, 2: Books in stock, 3: Books taken out, 4: Overdue books): ")
    if subcommand == '0':  # All books
        books = db[BOOKS_COLLECTION].find()
    elif subcommand == '1':  # Books owned
        books = db[BOOKS_COLLECTION].find()
        # Implement logic to filter books owned by the library
    elif subcommand == '2':  # Books in stock
        books = db[BOOKS_COLLECTION].find({"quantity": {"$gt": 0}})
    elif subcommand == '3':  # Books taken out
        # Get books that are currently taken out
        transactions = db[TRANSACTIONS_COLLECTION].find({"actual_return_date": None})
        book_ids = [transaction["book_id"] for transaction in transactions]
        books = db[BOOKS_COLLECTION].find({"_id": {"$in": book_ids}})
    elif subcommand == '4':  # Overdue books
        today = datetime.now()
        # Get transactions with return dates before today and actual return date is None (overdue)
        overdue_transactions = db[TRANSACTIONS_COLLECTION].find({
            "actual_return_date": None,
            "return_date": {"$lt": today}
        })
        book_ids = [transaction["book_id"] for transaction in overdue_transactions]
        books = db[BOOKS_COLLECTION].find({"_id": {"$in": book_ids}})
    else:
        print("Invalid subcommand. Please try again.")
        return

    if books:
        display_books(books)
    else:
        print("No books found.")

# Function to display books in table format
def display_books(books):
    table = PrettyTable(["Title", "Author", "Genre", "ISBN", "Publication Year", "Quantity"])
    for book in books:
        table.add_row([book.get("ID", ""), book.get("title", ""), book.get("author", ""), book.get("genre", ""), book.get("ISBN", ""), book.get("publication_year", ""), book.get("quantity", "")])
    print(table)

# Function to view transactions with subcommands
def view_transactions():
    subcommand = input("Enter the subcommand number (0: All transactions, 1: Borrowed transactions, 2: Returned transactions, 3: Overdue transactions): ")
    if subcommand == '0':  # All transactions
        transactions = db[TRANSACTIONS_COLLECTION].find()
    elif subcommand == '1':  # Borrowed transactions
        transactions = db[TRANSACTIONS_COLLECTION].find({"actual_return_date": None})
    elif subcommand == '2':  # Returned transactions
        transactions = db[TRANSACTIONS_COLLECTION].find({"actual_return_date": {"$ne": None}})
    elif subcommand == '3':  # Overdue transactions
        today = datetime.now()
        transactions = db[TRANSACTIONS_COLLECTION].find({
            "actual_return_date": None,
            "return_date": {"$lt": today}
        })
    else:
        print("Invalid subcommand. Please try again.")
        return

    if transactions:
        display_transactions(transactions)
    else:
        print("No transactions found.")

# Function to display transactions in table format
def display_transactions(transactions):
    table = PrettyTable(["Member ID", "Book ID", "Transaction Type", "Borrow Date", "Return Date", "Actual Return Date"])
    for transaction in transactions:
        table.add_row([
            transaction.get("member_id", ""),
            transaction.get("book_id", ""),
            transaction.get("transaction_type", ""),
            transaction.get("borrow_date", ""),
            transaction.get("return_date", ""),
            transaction.get("actual_return_date", "")
        ])
    print(table)

# Function to view members with subcommands
def view_members():
    subcommand = input("Enter the subcommand number (0: All members, 1: Active members, 2: Inactive members): ")
    if subcommand == '0':  # All members
        members = db[MEMBERS_COLLECTION].find()
    elif subcommand == '1':  # Active members
        members = db[MEMBERS_COLLECTION].find({"status": "Active"})
    elif subcommand == '2':  # Inactive members
        members = db[MEMBERS_COLLECTION].find({"status": "Inactive"})
    else:
        print("Invalid subcommand. Please try again.")
        return

    if members:
        display_members(members)
    else:
        print("No members found.")

# Function to display members in table format
def display_members(members):
    table = PrettyTable(["Name", "Email", "Phone", "Address", "Membership ID", "Status"])
    for member in members:
        table.add_row([
            member.get("name", ""),
            member.get("email", ""),
            member.get("phone", ""),
            member.get("address", ""),
            member.get("membership_id", ""),
            member.get("status", "")
        ])
    print(table)

# Function to add a new member (admin only)
def add_member(name, email, phone, address, membership_id):
    member = {
        "name": name,
        "email": email,
        "phone": phone,
        "address": address,
        "membership_id": membership_id,
        "status": "Active"
    }
    db[MEMBERS_COLLECTION].insert_one(member)
    print("New member added successfully.")

# Function to add a new book (admin only)
def add_book(title, author, genre, ISBN, publication_year, quantity):
    book = {
        "title": title,
        "author": author,
        "genre": genre,
        "ISBN": ISBN,
        "publication_year": publication_year,
        "quantity": quantity
    }
    db[BOOKS_COLLECTION].insert_one(book)
    print("New book added successfully.")

# Function to create a new transaction (teller only)
def create_transaction(member_id, book_id):
    member = db[MEMBERS_COLLECTION].find_one({"_id": ObjectId(member_id)})
    book = db[BOOKS_COLLECTION].find_one({"_id": ObjectId(book_id)})
    if member and book:
        today = datetime.now()
        return_date = today + timedelta(days=14)  # Return date is 14 days from today
        transaction = {
            "member_id": ObjectId(member_id),
            "book_id": ObjectId(book_id),
            "transaction_type": "Borrow",
            "borrow_date": today,
            "return_date": return_date,
            "actual_return_date": None
        }
        db[TRANSACTIONS_COLLECTION].insert_one(transaction)
        print("Transaction created successfully.")
    else:
        print("Invalid member ID or book ID.")

# Function to view transaction history
def view_transaction_history():
    transactions = db[TRANSACTIONS_COLLECTION].find().sort("borrow_date", pymongo.DESCENDING)
    if transactions:
        display_transactions(transactions)
    else:
        print("No transaction history found.")

# Main function
def main():
    print("Welcome to the Library Management System!")
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    # Authenticate staff login
    staff = login(username, password)
    if staff:
        print(f"Welcome, {staff['name']}!")
        staff_permission = staff['permission']  # Get staff permission level

        # Continue running commands until sign out
        while True:
            display_commands()
            command = input("Enter the command number: ")

            if command == '0':  # Add a book
                if staff_permission == 1:  # Admin only
                    title = input("Enter the title of the book: ")
                    author = input("Enter the author of the book: ")
                    genre = input("Enter the genre of the book: ")
                    ISBN = input("Enter the ISBN of the book: ")
                    publication_year = input("Enter the publication year of the book: ")
                    quantity = input("Enter the quantity of the book: ")
                    add_book(title, author, genre, ISBN, publication_year, quantity)
                else:
                    print("You don't have permission to add a book.")

            elif command == '1':  # Add a member
                if staff_permission == 1:  # Admin only
                    name = input("Enter the name of the member: ")
                    email = input("Enter the email of the member: ")
                    phone = input("Enter the phone number of the member: ")
                    address = input("Enter the address of the member: ")
                    membership_id = input("Enter the membership ID of the member: ")
                    add_member(name, email, phone, address, membership_id)
                else:
                    print("You don't have permission to add a member.")

            elif command == '2':  # Create a transaction
                if staff_permission == 0:  # Teller only
                    member_id = input("Enter the member ID: ")
                    book_id = input("Enter the book ID: ")
                    create_transaction(member_id, book_id)
                else:
                    print("You don't have permission to create a transaction.")

            elif command == '3':  # View books
                view_books()

            elif command == '4':  # View transactions
                view_transactions()

            elif command == '5':  # View transaction history
                view_transaction_history()

            elif command == '6':  # View members
                view_members()

            elif command == '7':  # Edit a book's details
                if staff_permission == 1:  # Admin only
                    book_id = input("Enter the book ID you want to edit: ")
                    edit_book(book_id)
                else:
                    print("You don't have permission to edit a book's details.")

            elif command == '8':  # Sign out
                print("Signing out...")
                break

            else:
                print("Invalid command. Please try again.")

    else:
        print("Invalid username or password. Please try again.")

if __name__ == "__main__":
    main()