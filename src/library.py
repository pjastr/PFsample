import json
import os
import datetime


class Library:
    """Class representing a library system."""

    def __init__(self, name, location):
        """Initialize a new library.

        Args:
            name (str): Library name
            location (str): Library location
        """
        self.name = name
        self.location = location
        self.books = {}  # Dict with ISBN as key
        self.users = {}  # Dict with user ID as key
        self.creation_date = datetime.datetime.now()

    def add_book(self, book):
        """Add a book to the library.

        Args:
            book: Book object to add

        Returns:
            bool: True if operation was successful

        Raises:
            ValueError: If book with same ISBN already exists
        """
        if book.isbn in self.books:
            raise ValueError(f"Book with ISBN {book.isbn} already exists in the library")

        self.books[book.isbn] = book
        return True

    def remove_book(self, isbn):
        """Remove a book from the library.

        Args:
            isbn (str): ISBN of the book to remove

        Returns:
            book: Removed book object

        Raises:
            ValueError: If book is not found or is borrowed
        """
        if isbn not in self.books:
            raise ValueError(f"Book with ISBN {isbn} not found in the library")

        book = self.books[isbn]
        if not book.available:
            raise ValueError(f"Cannot remove book '{book.title}' as it is currently borrowed")

        return self.books.pop(isbn)

    def find_book_by_isbn(self, isbn):
        """Find a book by ISBN.

        Args:
            isbn (str): ISBN to search for

        Returns:
            book: Found book object or None
        """
        return self.books.get(isbn)

    def find_books_by_author(self, author):
        """Find books by author.

        Args:
            author (str): Author name to search for

        Returns:
            list: List of books by the author
        """
        return [book for book in self.books.values() if author.lower() in book.author.lower()]

    def find_books_by_title(self, title):
        """Find books by title.

        Args:
            title (str): Title or part of title to search for

        Returns:
            list: List of books matching the title
        """
        return [book for book in self.books.values() if title.lower() in book.title.lower()]

    def register_user(self, user):
        """Register a new user in the library.

        Args:
            user: User object to register

        Returns:
            bool: True if operation was successful

        Raises:
            ValueError: If user with same ID already exists
        """
        if user.id in self.users:
            raise ValueError(f"User with ID {user.id} already exists in the library")

        self.users[user.id] = user
        return True

    def find_user(self, user_id):
        """Find a user by ID.

        Args:
            user_id (str): User ID to search for

        Returns:
            user: Found user object or None
        """
        return self.users.get(user_id)

    def save_to_file(self, filename):
        """Save library data to a file.

        Args:
            filename (str): File path to save to

        Returns:
            bool: True if operation was successful
        """
        data = {
            "name": self.name,
            "location": self.location,
            "creation_date": self.creation_date.isoformat(),
            "books": {isbn: json.loads(book.to_json()) for isbn, book in self.books.items()},
            "users": {user_id: json.loads(user.to_json()) for user_id, user in self.users.items()}
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return True

    @classmethod
    def load_from_file(cls, filename):
        """Load library data from a file.

        Args:
            filename (str): File path to load from

        Returns:
            Library: New Library instance

        Raises:
            FileNotFoundError: If file is not found
        """
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File {filename} not found")

        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        from book import Book, BookGenre
        from user import User, UserRole

        library = cls(data["name"], data["location"])

        # Load books
        for isbn, book_data in data["books"].items():
            book_data["genre"] = BookGenre[book_data["genre"]]
            book = Book(
                book_data["title"],
                book_data["author"],
                book_data["isbn"],
                book_data["publication_year"],
                book_data["genre"]
            )
            book.available = book_data["available"]
            library.books[isbn] = book

        # Load users
        for user_id, user_data in data["users"].items():
            user_data["role"] = UserRole[user_data["role"]]
            user = User(
                user_data["id"],
                user_data["name"],
                user_data["email"],
                user_data["role"]
            )
            user.active = user_data["active"]
            library.users[user_id] = user

        return library