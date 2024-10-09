"""
Books Catalog Module

This module defines a list of books, each represented as a dictionary containing the
book's title, author, category, and ISBN.
It then sorts this list of books by the last name of the author.

Attributes:
    BOOKS (list): A list of dictionaries, where each dictionary represents a book with
    keys:
        - title (str): The title of the book.
        - author (str): The author of the book.
        - category (str): The category or genre of the book.
        - isbn (str): The ISBN number of the book.

Functions:
    _get_author_last_name(name: str) -> str: Returns the last name of the author from a
    full name string.

Usage:
    The BOOKS list gets automatically sorted by the author's last name upon module
    import.
"""

BOOKS = [
    dict(
        title="A Brief History of Time",
        author="Stephen Hawking",
        category="Science",
        isbn="9780553380163",
    ),
    dict(
        title="The Great Gatsby",
        author="F. Scott Fitzgerald",
        category="Classic",
        isbn="9780743273565",
    ),
    dict(
        title="1984", author="George Orwell", category="Dystopian", isbn="9780451524935"
    ),
    dict(
        title="Animal Farm",
        author="George Orwell",
        category="Satire",
        isbn="9780451526342",
    ),
    dict(
        title="To Kill a Mockingbird",
        author="Harper Lee",
        category="Classic",
        isbn="9780061120084",
    ),
    dict(
        title="The Catcher in the Rye",
        author="J.D. Salinger",
        category="Fiction",
        isbn="9780316769488",
    ),
    dict(
        title="Go Set a Watchman",
        author="Harper Lee",
        category="Classic",
        isbn="9780062409850",
    ),
]


def _get_author_last_name(name: str) -> str:
    return name.split()[-1]


BOOKS.sort(key=lambda b: _get_author_last_name(b["author"]))
