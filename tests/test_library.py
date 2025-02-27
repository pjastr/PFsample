import unittest
import os
import tempfile
from src.library import Library
from src.book import Book, BookGenre
from src.user import User, UserRole


class TestLibrary(unittest.TestCase):
    """Test cases for the Library class."""

    def setUp(self):
        """Set up test fixtures."""
        self.library = Library(
            name="Central Library",
            location="City Center"
        )

        # Create test books
        self.book1 = Book(
            title="The Hobbit",
            author="J.R.R. Tolkien",
            isbn="9780261103344",
            publication_year=1937,
            genre=BookGenre.FANTASY
        )

        self.book2 = Book(
            title="Pride and Prejudice",
            author="Jane Austen",
            isbn="9780141439518",
            publication_year=1813,
            genre=BookGenre.ROMANCE
        )

        # Create test users
        self.user1 = User(
            id="U123",
            name="John Doe",
            email="john@example.com",
            role=UserRole.STUDENT
        )

        self.user2 = User(
            id="U456",
            name="Jane Smith",
            email="jane@example.com",
            role=UserRole.TEACHER
        )

    def test_library_initialization(self):
        """Test that a library can be created with valid attributes."""
        self.assertEqual(self.library.name, "Central Library")
        self.assertEqual(self.library.location, "City Center")
        self.assertEqual(len(self.library.books), 0)
        self.assertEqual(len(self.library.users), 0)

    def test_add_book(self):
        """Test that a book can be added to the library."""
        self.assertTrue(self.library.add_book(self.book1))
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[self.book1.isbn], self.book1)

    def test_add_duplicate_book_raises_error(self):
        """Test that adding a book with duplicate ISBN raises ValueError."""
        self.library.add_book(self.book1)

        with self.assertRaises(ValueError):
            self.library.add_book(self.book1)

    def test_remove_book(self):
        """Test that a book can be removed from the library."""
        self.library.add_book(self.book1)
        removed_book = self.library.remove_book(self.book1.isbn)

        self.assertEqual(removed_book, self.book1)
        self.assertEqual(len(self.library.books), 0)

    def test_remove_nonexistent_book_raises_error(self):
        """Test that removing a nonexistent book raises ValueError."""
        with self.assertRaises(ValueError):
            self.library.remove_book("nonexistent-isbn")

    def test_remove_borrowed_book_raises_error(self):
        """Test that removing a borrowed book raises ValueError."""
        self.library.add_book(self.book1)
        self.library.register_user(self.user1)

        self.user1.borrow_book(self.book1)

        with self.assertRaises(ValueError):
            self.library.remove_book(self.book1.isbn)

    def test_find_book_by_isbn(self):
        """Test that a book can be found by ISBN."""
        self.library.add_book(self.book1)
        self.library.add_book(self.book2)

        found_book = self.library.find_book_by_isbn(self.book1.isbn)
        self.assertEqual(found_book, self.book1)

        nonexistent_book = self.library.find_book_by_isbn("nonexistent-isbn")
        self.assertIsNone(nonexistent_book)

    def test_find_books_by_author(self):
        """Test that books can be found by author."""
        self.library.add_book(self.book1)
        self.library.add_book(self.book2)

        tolkien_books = self.library.find_books_by_author("Tolkien")
        self.assertEqual(len(tolkien_books), 1)
        self.assertEqual(tolkien_books[0], self.book1)

        # Case insensitive search
        tolkien_books_lower = self.library.find_books_by_author("tolkien")
        self.assertEqual(len(tolkien_books_lower), 1)

        # Nonexistent author
        nonexistent_books = self.library.find_books_by_author("nonexistent")
        self.assertEqual(len(nonexistent_books), 0)

    def test_find_books_by_title(self):
        """Test that books can be found by title."""
        self.library.add_book(self.book1)
        self.library.add_book(self.book2)

        hobbit_books = self.library.find_books_by_title("Hobbit")
        self.assertEqual(len(hobbit_books), 1)
        self.assertEqual(hobbit_books[0], self.book1)

        # Case insensitive search
        hobbit_books_lower = self.library.find_books_by_title("hobbit")
        self.assertEqual(len(hobbit_books_lower), 1)

        # Partial match
        pride_books = self.library.find_books_by_title("Pride")
        self.assertEqual(len(pride_books), 1)
        self.assertEqual(pride_books[0], self.book2)

        # Nonexistent title
        nonexistent_books = self.library.find_books_by_title("nonexistent")
        self.assertEqual(len(nonexistent_books), 0)

    def test_register_user(self):
        """Test that a user can be registered in the library."""
        self.assertTrue(self.library.register_user(self.user1))
        self.assertEqual(len(self.library.users), 1)
        self.assertEqual(self.library.users[self.user1.id], self.user1)

    def test_register_duplicate_user_raises_error(self):
        """Test that registering a user with duplicate ID raises ValueError."""
        self.library.register_user(self.user1)

        with self.assertRaises(ValueError):
            self.library.register_user(self.user1)

    def test_find_user(self):
        """Test that a user can be found by ID."""
        self.library.register_user(self.user1)
        self.library.register_user(self.user2)

        found_user = self.library.find_user(self.user1.id)
        self.assertEqual(found_user, self.user1)

        nonexistent_user = self.library.find_user("nonexistent-id")
        self.assertIsNone(nonexistent_user)

    def test_save_and_load_from_file(self):
        """Test that library data can be saved to a file and loaded back."""
        # Add books and users
        self.library.add_book(self.book1)
        self.library.add_book(self.book2)
        self.library.register_user(self.user1)
        self.library.register_user(self.user2)

        # Save to a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_filename = temp_file.name

        try:
            self.library.save_to_file(temp_filename)

            import json
            with open(temp_filename, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.assertEqual(data["name"], "Central Library")
            self.assertEqual(data["location"], "City Center")
            self.assertEqual(len(data["books"]), 2)
            self.assertEqual(len(data["users"]), 2)

        finally:
            # Clean up temporary file
            if os.path.exists(temp_filename):
                os.remove(temp_filename)

    def test_load_from_nonexistent_file_raises_error(self):
        """Test that loading from a nonexistent file raises FileNotFoundError."""
        with self.assertRaises(FileNotFoundError):
            Library.load_from_file("nonexistent-file.json")