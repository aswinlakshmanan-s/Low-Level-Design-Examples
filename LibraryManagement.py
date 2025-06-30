from threading import Lock
from typing import Dict, List
import uuid
from datetime import datetime, timedelta

MAX_BORROW_LIMIT = 3
LOAN_DURATION_DAYS = 14

class Book:
    def __init__(self, title: str, author: str, isbn: str, pub_year: int):
        self.book_id = str(uuid.uuid4())
        self.title = title
        self.author = author
        self.isbn = isbn
        self.pub_year = pub_year
        self.is_available = True

    def __str__(self):
        return f"{self.title} by {self.author} ({self.pub_year}) - {'Available' if self.is_available else 'Borrowed'}"

class Member:
    def __init__(self, name: str, contact: str):
        self.member_id = str(uuid.uuid4())
        self.name = name
        self.contact = contact
        self.borrowed_books: Dict[str, datetime] = {}  # book_id -> due_date

    def __str__(self):
        return f"{self.name} ({self.member_id})"

class LibrarySystem:
    def __init__(self):
        self.books: Dict[str, Book] = {}          # book_id -> Book
        self.members: Dict[str, Member] = {}      # member_id -> Member
        self.lock = Lock()

    # Book Management
    def add_book(self, title: str, author: str, isbn: str, pub_year: int):
        with self.lock:
            book = Book(title, author, isbn, pub_year)
            self.books[book.book_id] = book
            print(f"Added: {book}")

    def remove_book(self, book_id: str):
        with self.lock:
            if book_id in self.books:
                del self.books[book_id]
                print(f"Removed book ID: {book_id}")

    def update_book_status(self, book_id: str, is_available: bool):
        with self.lock:
            if book_id in self.books:
                self.books[book_id].is_available = is_available

    # Member Management
    def register_member(self, name: str, contact: str) -> str:
        with self.lock:
            member = Member(name, contact)
            self.members[member.member_id] = member
            print(f"Registered member: {member}")
            return member.member_id

    # Borrowing Logic
    def borrow_book(self, member_id: str, book_id: str):
        with self.lock:
            if member_id not in self.members or book_id not in self.books:
                print("Invalid member or book.")
                return False

            member = self.members[member_id]
            book = self.books[book_id]

            if not book.is_available:
                print("Book already borrowed.")
                return False

            if len(member.borrowed_books) >= MAX_BORROW_LIMIT:
                print("Borrowing limit reached.")
                return False

            due_date = datetime.now() + timedelta(days=LOAN_DURATION_DAYS)
            member.borrowed_books[book_id] = due_date
            book.is_available = False
            print(f"{member.name} borrowed '{book.title}'. Due on {due_date.date()}.")
            return True

    # Returning Logic
    def return_book(self, member_id: str, book_id: str):
        with self.lock:
            if member_id not in self.members or book_id not in self.books:
                print("Invalid member or book.")
                return False

            member = self.members[member_id]
            if book_id not in member.borrowed_books:
                print("Book was not borrowed by this member.")
                return False

            del member.borrowed_books[book_id]
            self.books[book_id].is_available = True
            print(f"{member.name} returned '{self.books[book_id].title}'.")
            return True

    # Debug Print
    def print_books(self):
        print("\nAll Books in Library:")
        for book in self.books.values():
            print(book)

    def print_member_info(self, member_id: str):
        if member_id in self.members:
            member = self.members[member_id]
            print(f"\n{member.name}'s borrowed books:")
            for book_id, due in member.borrowed_books.items():
                book = self.books[book_id]
                print(f"- {book.title} (Due: {due.date()})")

# -------------------------------
# Sample Usage
if __name__ == "__main__":
    system = LibrarySystem()

    # Add books
    system.add_book("1984", "George Orwell", "123456", 1949)
    system.add_book("Brave New World", "Aldous Huxley", "234567", 1932)

    # Register a member
    member_id = system.register_member("Alice", "alice@example.com")

    # Borrow books
    book_ids = list(system.books.keys())
    system.borrow_book(member_id, book_ids[0])
    system.borrow_book(member_id, book_ids[1])

    # View status
    system.print_books()
    system.print_member_info(member_id)

    # Return a book
    system.return_book(member_id, book_ids[0])
    system.print_books()
