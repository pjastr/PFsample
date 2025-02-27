import json
import re
import datetime
from enum import Enum, auto


class UserRole(Enum):
    """Enum representing user roles in the library system."""
    STUDENT = auto()
    TEACHER = auto()
    LIBRARIAN = auto()
    ADMIN = auto()
    GUEST = auto()


class User:
    """Class representing a user in the library system."""

    def __init__(self, id, name, email, role=UserRole.GUEST):
        """Initialize a new user.

        Args:
            id (str): User ID
            name (str): User name
            email (str): User email
            role (UserRole, optional): User role. Default is UserRole.GUEST

        Raises:
            ValueError: If email format is invalid
        """
        self.id = id
        self.name = name
        self.role = role

        # Email validation
        if not self._validate_email(email):
            raise ValueError(f"Invalid email format: {email}")
        self.email = email

        # Additional attributes
        self.registration_date = datetime.datetime.now()
        self.borrowed_books = []
        self.active = True

    def _validate_email(self, email):
        """Validate email format.

        Args:
            email (str): Email to validate

        Returns:
            bool: True if email format is valid, False otherwise
        """
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_pattern, email))

    def borrow_book(self, book):
        """Adds a book to user's borrowed books.

        Args:
            book: Book object to borrow

        Returns:
            bool: True if operation was successful
        """
        if not self.active:
            raise ValueError("Inactive user cannot borrow books")

        if book in self.borrowed_books:
            raise ValueError(f"Book '{book.title}' is already borrowed by this user")

        # Execute the book's borrow operation
        book.borrow(self)
        self.borrowed_books.append(book)
        return True

    def return_book(self, book):
        """Returns a book from user's borrowed books.

        Args:
            book: Book object to return

        Returns:
            bool: True if operation was successful

        Raises:
            ValueError: If the book was not borrowed by this user
        """
        if book not in self.borrowed_books:
            raise ValueError(f"Book '{book.title}' was not borrowed by this user")

        book.return_book()
        self.borrowed_books.remove(book)
        return True

    def deactivate(self):
        """Deactivates the user account.

        Returns:
            bool: True if operation was successful
        """
        if self.borrowed_books:
            raise ValueError("Cannot deactivate user with borrowed books")

        self.active = False
        return True

    def activate(self):
        """Activates the user account.

        Returns:
            bool: True if operation was successful
        """
        self.active = True
        return True

    def to_json(self):
        """Converts the user to JSON format.

        Returns:
            str: JSON representation of the user
        """
        data = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role.name,
            "registration_date": self.registration_date.isoformat(),
            "active": self.active,
            "borrowed_books_count": len(self.borrowed_books)
        }

        return json.dumps(data, ensure_ascii=False)

    @classmethod
    def from_json(cls, json_str):
        """Creates a user instance from JSON data.

        Args:
            json_str (str): User data in JSON format

        Returns:
            User: New User instance
        """
        data = json.loads(json_str)
        role = UserRole[data["role"]]

        user = cls(
            data["id"],
            data["name"],
            data["email"],
            role
        )

        user.active = data["active"]
        return user