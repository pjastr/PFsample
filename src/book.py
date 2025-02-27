import datetime
import json
from enum import Enum, auto


class BookGenre(Enum):
    """Enum representing book genres."""
    FANTASY = auto()
    MYSTERY = auto()
    ROMANCE = auto()
    BIOGRAPHY = auto()
    SCIENCE = auto()
    OTHER = auto()


class Book:
    """Class representing a book in the library system."""

    def __init__(self, title, author, isbn, publication_year, genre=BookGenre.OTHER):
        """Initialize a new book.

        Args:
            title (str): Book title
            author (str): Book author
            isbn (str): ISBN number (13 digits)
            publication_year (int): Year of publication
            genre (BookGenre, optional): Book genre. Default is BookGenre.OTHER

        Raises:
            ValueError: If data is invalid
        """
        self.title = title
        self.author = author
        self.genre = genre

        # ISBN validation
        if not self._validate_isbn(isbn):
            raise ValueError(f"Invalid ISBN number: {isbn}")
        self.isbn = isbn

        # Publication year validation
        current_year = datetime.datetime.now().year
        if not isinstance(publication_year, int) or publication_year < 1450 or publication_year > current_year:
            raise ValueError(f"Invalid publication year: {publication_year}")
        self.publication_year = publication_year

        # Additional attributes
        self.available = True
        self.borrow_date = None
        self.borrowed_by = None

    def _validate_isbn(self, isbn):
        """Validates ISBN number format.

        Args:
            isbn (str): ISBN number to validate

        Returns:
            bool: True if the ISBN is valid, False otherwise
        """
        # Simplified validation - check length and if contains only digits
        if len(isbn) != 13:
            return False
        return isbn.isdigit()

    def borrow(self, user):
        """Borrows the book to the specified user.

        Args:
            user: User object borrowing the book

        Raises:
            ValueError: If the book is already borrowed

        Returns:
            bool: True if operation was successful
        """
        if not self.available:
            raise ValueError(f"Book '{self.title}' is already borrowed.")

        self.available = False
        self.borrow_date = datetime.datetime.now()
        self.borrowed_by = user
        return True

    def return_book(self):
        """Returns the borrowed book to the library.

        Returns:
            bool: True if operation was successful
        """
        self.available = True
        self.borrow_date = None
        self.borrowed_by = None
        return True

    def to_json(self):
        """Converts the book to JSON format.

        Returns:
            str: JSON representation of the book
        """
        data = {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "publication_year": self.publication_year,
            "genre": self.genre.name,
            "available": self.available
        }

        # Additional data if the book is borrowed
        if not self.available and self.borrowed_by:
            data["borrowed_by"] = self.borrowed_by.id
            data["borrow_date"] = self.borrow_date.isoformat()

        return json.dumps(data, ensure_ascii=False)

    @classmethod
    def from_json(cls, json_str):
        """Creates a book instance from JSON data.

        Args:
            json_str (str): Book data in JSON format

        Returns:
            Book: New Book instance
        """
        data = json.loads(json_str)
        genre = BookGenre[data["genre"]]

        book = cls(
            data["title"],
            data["author"],
            data["isbn"],
            data["publication_year"],
            genre
        )

        book.available = data["available"]
        return book