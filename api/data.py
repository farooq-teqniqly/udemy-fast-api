"""
data.py

This module defines a catalog of books and manages a dictionary for storing book
reviews. Each book is represented as a dictionary with various attributes such as title,
author, category, ISBN, and ratings information. The module also provides a structure
to hold book reviews.

Attributes:
    BOOKS (list):
        A list of dictionaries, where each dictionary represents a book with the
        following keys:
            - title (str): The title of the book.
            - author (str): The author of the book.
            - category (str): The category or genre of the book.
            - isbn (str): The ISBN number of the book.
            - avg_rating (Optional[float]): The average rating of the book.
            - num_ratings (int): The total number of ratings the book has received.
            - sum_ratings (float): The sum of all ratings the book has received.
            - soft_deleted (bool): True if the book is soft-deleted, otherwise False.

    BOOK_REVIEWS (dict):
        A dictionary where the keys are ISBN numbers (str) of books and the values are
        lists of reviews (Optional[List[str]]) for the corresponding books. If a book
        has no reviews, the value is None.

Example:
    Adding a book to the BOOKS list:
    ```python
    BOOKS.append(
        dict(
            title="New Book",
            author="New Author",
            category="New Category",
            isbn="1234567890123",
            avg_rating=None,
            num_ratings=0,
            sum_ratings=0,
            soft_deleted=False,
        )
    )
    ```

    Adding a review for a book:
    ```python
    isbn = "9780553380163"
    if isbn in BOOK_REVIEWS:
        if BOOK_REVIEWS[isbn] is None:
            BOOK_REVIEWS[isbn] = []
        BOOK_REVIEWS[isbn].append("This is a review.")
    else:
        BOOK_REVIEWS[isbn] = ["This is a review."]
    ```
"""

from typing import Dict, List

BOOKS = [
    dict(
        title="A Brief History of Time",
        author="Stephen Hawking",
        category="Science",
        isbn="9780553380163",
        avg_rating=None,
        num_ratings=0,
        sum_ratings=0,
        soft_deleted=False,
    ),
    dict(
        title="The Great Gatsby",
        author="F. Scott Fitzgerald",
        category="Classic",
        isbn="9780743273565",
        avg_rating=None,
        num_ratings=0,
        sum_ratings=0,
        soft_deleted=False,
    ),
    dict(
        title="1984",
        author="George Orwell",
        category="Dystopian",
        isbn="9780451524935",
        avg_rating=None,
        num_ratings=0,
        sum_ratings=0,
        soft_deleted=False,
    ),
    dict(
        title="Animal Farm",
        author="George Orwell",
        category="Satire",
        isbn="9780451526342",
        avg_rating=None,
        num_ratings=0,
        sum_ratings=0,
        soft_deleted=False,
    ),
    dict(
        title="To Kill a Mockingbird",
        author="Harper Lee",
        category="Classic",
        isbn="9780061120084",
        avg_rating=None,
        num_ratings=0,
        sum_ratings=0,
        soft_deleted=False,
    ),
    dict(
        title="The Catcher in the Rye",
        author="J.D. Salinger",
        category="Fiction",
        isbn="9780316769488",
        avg_rating=None,
        num_ratings=0,
        sum_ratings=0,
        soft_deleted=False,
    ),
    dict(
        title="Go Set a Watchman",
        author="Harper Lee",
        category="Classic",
        isbn="9780062409850",
        avg_rating=None,
        num_ratings=0,
        sum_ratings=0,
        soft_deleted=False,
    ),
]

BOOK_REVIEWS: List[Dict[str, List[str]]] = []
