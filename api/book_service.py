"""
book_service.py

This module provides the core services for managing book-related operations.
It includes functions for querying, adding, deleting books, and managing
book ratings and reviews. Additionally, it contains utility functions for
filtering and managing book data.

Functions:
    _filter_books(books, filter_params):
        Applies various filtering criteria to a list of books based on
        provided parameters.

    _limit_books(books, limit):
        Limits the number of books returned based on the specified limit.

    _exclude_deleted_books(books):
        Excludes books marked as deleted from the provided list.

    _get_author_last_name(author):
        Retrieves the last name of an author from the author metadata.

    query_book(query_params):
        Queries books based on given parameters. Supports searching and
        filtering of book data.

    add_book(book_data):
        Adds a new book to the collection. Requires book details such as title,
        author, published date, etc.

    delete_book(book_id):
        Marks a book as deleted based on the provided book ID.

    add_rating(book_id, rating_data):
        Adds a rating to a specific book. Requires book ID and rating details.

    add_review(book_id, review_data):
        Adds a review to a specific book. Requires book ID and review details.

    get_reviews(book_id):
        Retrieves reviews for a specific book based on the book ID.
"""

from typing import Dict, List, Optional

from api.data import BOOK_REVIEWS, BOOKS
from api.models import (
    AddBookQueryParameters,
    AddRatingParameters,
    BookQueryParameters,
    CreateReviewRequest,
)


def _filter_books(
    books: List[Dict[str, Optional[str]]], key: str, value: Optional[str]
) -> List[Dict[str, Optional[str]]]:
    if value:
        return [
            book for book in books if book.get(key, "").casefold() == value.casefold()
        ]
    return books


def _limit_books(
    books: List[Dict[str, Optional[str]]], limit: Optional[int]
) -> List[Dict[str, Optional[str]]]:
    return books[:limit] if limit else books


def _exclude_deleted_books(books: List[Dict[str, Optional[str]]]):
    return [book for book in books if not book.get("soft_deleted", False)]


def _get_author_last_name(name: str) -> str:
    return name.split()[-1]


async def query_book(params: BookQueryParameters) -> List[Dict[str, Optional[str]]]:
    """
    Args:
        params: The parameters for querying books, including author, category, isbn,
        and top limit.

    Returns:
        A list of dictionaries, where each dictionary represents a book with optional
        string fields.
    """
    filtered_books = _filter_books(BOOKS, "author", params.author)
    filtered_books = _filter_books(filtered_books, "category", params.category)
    filtered_books = _filter_books(filtered_books, "isbn", params.isbn)

    if not params.return_deleted_books:
        filtered_books = _exclude_deleted_books(filtered_books)

    filtered_books = _limit_books(filtered_books, params.top)
    filtered_books.sort(key=lambda b: _get_author_last_name(b["author"]))
    return filtered_books


async def add_book(params: AddBookQueryParameters) -> None:
    """
    Adds a book to the BOOKS list.

    Args:
        params: Contains the attributes of the book to add including title, author,
        category, and ISBN.
    """
    BOOKS.append(
        dict(
            title=params.title,
            author=params.author,
            category=params.category,
            isbn=params.isbn,
            avg_rating=None,
            num_ratings=None,
        )
    )


async def delete_book(isbn: str) -> None:
    """
    Args:
        isbn: The ISBN of the book to be deleted.

    Marks the book identified by the provided ISBN as 'soft deleted' in the BOOKS
    collection.
    """
    books = [b for b in BOOKS if b["isbn"] == isbn]

    if books:
        books[0]["soft_deleted"] = True


async def add_rating(isbn: str, params: AddRatingParameters):
    books = [b for b in BOOKS if b["isbn"] == isbn]

    if len(books) == 0:
        return

    book = books[0]
    book["num_ratings"] += 1
    book["sum_ratings"] += params.rating
    book["avg_rating"] = book["sum_ratings"] / book["num_ratings"]


async def add_review(isbn: str, request: CreateReviewRequest):
    """
    Args:
        isbn: The International Standard Book Number of the book.
        request: An instance of CreateReviewRequest containing the review to be added.
    """
    book_reviews = BOOK_REVIEWS.setdefault(isbn, [])

    if not any(book for book in BOOKS if book["isbn"] == isbn):
        return

    book_reviews.append(request.review)


async def get_reviews(isbn: str):
    """
    Args:
        isbn (str): The ISBN number of the book for which reviews are to be fetched.

    Returns:
        list: A list containing reviews for the book. If no reviews are found, an empty
        list is returned.
    """
    return BOOK_REVIEWS.get(isbn, [])
