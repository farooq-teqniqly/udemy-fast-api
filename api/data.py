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
        - avg_rating (float): The average rating of the book.
        - num_ratings (int): The total number of ratings the book has received.
"""

BOOKS = [
    dict(
        title="A Brief History of Time",
        author="Stephen Hawking",
        category="Science",
        isbn="9780553380163",
        avg_rating=None,
        num_ratings=None,
    ),
    dict(
        title="The Great Gatsby",
        author="F. Scott Fitzgerald",
        category="Classic",
        isbn="9780743273565",
        avg_rating=None,
        num_ratings=None,
    ),
    dict(
        title="1984",
        author="George Orwell",
        category="Dystopian",
        isbn="9780451524935",
        avg_rating=None,
        num_ratings=None,
    ),
    dict(
        title="Animal Farm",
        author="George Orwell",
        category="Satire",
        isbn="9780451526342",
        avg_rating=None,
        num_ratings=None,
    ),
    dict(
        title="To Kill a Mockingbird",
        author="Harper Lee",
        category="Classic",
        isbn="9780061120084",
        avg_rating=None,
        num_ratings=None,
    ),
    dict(
        title="The Catcher in the Rye",
        author="J.D. Salinger",
        category="Fiction",
        isbn="9780316769488",
        avg_rating=None,
        num_ratings=None,
    ),
    dict(
        title="Go Set a Watchman",
        author="Harper Lee",
        category="Classic",
        isbn="9780062409850",
        avg_rating=None,
        num_ratings=None,
    ),
]
