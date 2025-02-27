import unittest
import datetime
import json
from src.book import Book, BookGenre
from src.user import User, UserRole


class TestBook(unittest.TestCase):
    """Test cases for the Book class."""

    def setUp(self):
        """Set up test fixtures."""
        self.valid_book = Book(
            title="The Hobbit",
            author="J.R.R. Tolkien",
            isbn="9780261103344",
            publication_year=1937,
            genre=BookGenre.FANTASY
        )

        self.test_user = User(
            id="U123",
            name="John Doe",
            email="john@example.com",
            role=UserRole.STUDENT
        )

    def test_book_initialization(self):
        """Test that a book can be created with valid attributes."""
        self.assertEqual(self.valid_book.title, "The Hobbit")
        self.assertEqual(self.valid_book.author, "J.R.R. Tolkien")
        self.assertEqual(self.valid_book.isbn, "9780261103344")
        self.assertEqual(self.valid_book.publication_year, 1937)
        self.assertEqual(self.valid_book.genre, BookGenre.FANTASY)
        self.assertTrue(self.valid_book.available)
        self.assertIsNone(self.valid_book.borrow_date)
        self.assertIsNone(self.valid_book.borrowed_by)

    def test_invalid_isbn_raises_error(self):
        """Test that creating a book with invalid ISBN raises ValueError."""
        with self.assertRaises(ValueError):
            Book(
                title="Invalid Book",
                author="Author",
                isbn="123",  # Too short
                publication_year=2020
            )

        with self.assertRaises(ValueError):
            Book(
                title="Invalid Book",
                author="Author",
                isbn="123abc4567890",  # Contains non-digits
                publication_year=2020
            )

    def test_invalid_publication_year_raises_error(self):
        """Test that creating a book with invalid publication year raises ValueError."""
        current_year = datetime.datetime.now().year

        with self.assertRaises(ValueError):
            Book(
                title="Future Book",
                author="Author",
                isbn="9780261103344",
                publication_year=current_year + 1  # Future year
            )

        with self.assertRaises(ValueError):
            Book(
                title="Ancient Book",
                author="Author",
                isbn="9780261103344",
                publication_year=1000  # Too old
            )

    def test_book_borrow(self):
        """Test that a book can be borrowed."""
        self.assertTrue(self.valid_book.borrow(self.test_user))
        self.assertFalse(self.valid_book.available)
        self.assertEqual(self.valid_book.borrowed_by, self.test_user)
        self.assertIsNotNone(self.valid_book.borrow_date)

    def test_borrow_already_borrowed_raises_error(self):
        """Test that borrowing an already borrowed book raises ValueError."""
        self.valid_book.borrow(self.test_user)

        with self.assertRaises(ValueError):
            self.valid_book.borrow(self.test_user)

    def test_book_return(self):
        """Test that a borrowed book can be returned."""
        self.valid_book.borrow(self.test_user)
        self.assertTrue(self.valid_book.return_book())
        self.assertTrue(self.valid_book.available)
        self.assertIsNone(self.valid_book.borrowed_by)
        self.assertIsNone(self.valid_book.borrow_date)

    def test_to_json(self):
        """Test that a book can be converted to JSON."""
        json_str = self.valid_book.to_json()
        data = json.loads(json_str)

        self.assertEqual(data["title"], "The Hobbit")
        self.assertEqual(data["author"], "J.R.R. Tolkien")
        self.assertEqual(data["isbn"], "9780261103344")
        self.assertEqual(data["publication_year"], 1937)
        self.assertEqual(data["genre"], "FANTASY")
        self.assertTrue(data["available"])

    def test_from_json(self):
        """Test that a book can be created from JSON."""
        json_str = self.valid_book.to_json()
        new_book = Book.from_json(json_str)

        self.assertEqual(new_book.title, "The Hobbit")
        self.assertEqual(new_book.author, "J.R.R. Tolkien")
        self.assertEqual(new_book.isbn, "9780261103344")
        self.assertEqual(new_book.publication_year, 1937)
        self.assertEqual(new_book.genre, BookGenre.FANTASY)
        self.assertTrue(new_book.available)