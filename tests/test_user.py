import unittest
import re
from src.user import User, UserRole
from src.book import Book, BookGenre


class TestUser(unittest.TestCase):
    """Test cases for the User class."""

    def setUp(self):
        """Set up test fixtures."""
        self.valid_user = User(
            id="U123",
            name="John Doe",
            email="john@example.com",
            role=UserRole.STUDENT
        )

        self.test_book = Book(
            title="The Hobbit",
            author="J.R.R. Tolkien",
            isbn="9780261103344",
            publication_year=1937,
            genre=BookGenre.FANTASY
        )

    def test_user_initialization(self):
        """Test that a user can be created with valid attributes."""
        self.assertEqual(self.valid_user.id, "U123")
        self.assertEqual(self.valid_user.name, "John Doe")
        self.assertEqual(self.valid_user.email, "john@example.com")
        self.assertEqual(self.valid_user.role, UserRole.STUDENT)
        self.assertTrue(self.valid_user.active)
        self.assertEqual(len(self.valid_user.borrowed_books), 0)

    def test_invalid_email_raises_error(self):
        """Test that creating a user with invalid email raises ValueError."""
        with self.assertRaises(ValueError):
            User(
                id="U123",
                name="John Doe",
                email="invalid-email",  # Invalid email format
                role=UserRole.STUDENT
            )

    def test_email_validation_regex(self):
        """Test the email validation regex pattern."""
        valid_emails = [
            "user@example.com",
            "user.name@example.com",
            "user+tag@example.com",
            "user@sub.example.com"
        ]

        invalid_emails = [
            "user@",
            "@example.com",
            "user@.com",
            "user@example.",
            "user@exam@ple.com"
        ]

        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        for email in valid_emails:
            self.assertTrue(bool(re.match(email_pattern, email)))

        for email in invalid_emails:
            self.assertFalse(bool(re.match(email_pattern, email)))

    def test_borrow_book(self):
        """Test that a user can borrow a book."""
        self.assertTrue(self.valid_user.borrow_book(self.test_book))
        self.assertEqual(len(self.valid_user.borrowed_books), 1)
        self.assertEqual(self.valid_user.borrowed_books[0], self.test_book)
        self.assertFalse(self.test_book.available)
        self.assertEqual(self.test_book.borrowed_by, self.valid_user)

    def test_borrow_already_borrowed_book_raises_error(self):
        """Test that borrowing an already borrowed book raises ValueError."""
        self.valid_user.borrow_book(self.test_book)

        with self.assertRaises(ValueError):
            self.valid_user.borrow_book(self.test_book)

    def test_return_book(self):
        """Test that a user can return a borrowed book."""
        self.valid_user.borrow_book(self.test_book)
        self.assertTrue(self.valid_user.return_book(self.test_book))
        self.assertEqual(len(self.valid_user.borrowed_books), 0)
        self.assertTrue(self.test_book.available)

    def test_return_not_borrowed_book_raises_error(self):
        """Test that returning a not borrowed book raises ValueError."""
        with self.assertRaises(ValueError):
            self.valid_user.return_book(self.test_book)

    def test_deactivate_user(self):
        """Test that a user can be deactivated."""
        self.assertTrue(self.valid_user.deactivate())
        self.assertFalse(self.valid_user.active)

    def test_deactivate_user_with_borrowed_books_raises_error(self):
        """Test that deactivating a user with borrowed books raises ValueError."""
        self.valid_user.borrow_book(self.test_book)

        with self.assertRaises(ValueError):
            self.valid_user.deactivate()

    def test_activate_user(self):
        """Test that a user can be activated."""
        self.valid_user.deactivate()
        self.assertTrue(self.valid_user.activate())
        self.assertTrue(self.valid_user.active)

    def test_to_json(self):
        """Test that a user can be converted to JSON."""
        json_str = self.valid_user.to_json()
        import json
        data = json.loads(json_str)

        self.assertEqual(data["id"], "U123")
        self.assertEqual(data["name"], "John Doe")
        self.assertEqual(data["email"], "john@example.com")
        self.assertEqual(data["role"], "STUDENT")
        self.assertTrue(data["active"])
        self.assertEqual(data["borrowed_books_count"], 0)

    def test_from_json(self):
        """Test that a user can be created from JSON."""
        json_str = self.valid_user.to_json()
        new_user = User.from_json(json_str)

        self.assertEqual(new_user.id, "U123")
        self.assertEqual(new_user.name, "John Doe")
        self.assertEqual(new_user.email, "john@example.com")
        self.assertEqual(new_user.role, UserRole.STUDENT)
        self.assertTrue(new_user.active)