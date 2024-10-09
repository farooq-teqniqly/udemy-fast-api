"""
This module defines a FastAPI application for querying, adding, and deleting books.

It includes the following components:
- FastAPI application setup with a specified title.
- API endpoints to query, add, and delete books using specified parameters.
- Dependency injection to handle book query, addition, and deletion parameters.

Main Components:
- FastAPI: The web framework used to create the API application.
- uvicorn: ASGI server used to run the application.
- api.book_service: Module containing the business logic for querying, adding, and
    deleting books.
- api.models: Module defining the data models used in the API.

Endpoints:
- GET /books/q:
    - Description: API endpoint to query books based on specified parameters.
    - Parameters: BookQueryParameters (Injected via Depends).
    - Returns: The result of the book query.
- POST /books:
    - Description: API endpoint to add a new book based on specified parameters.
    - Parameters: AddBookQueryParameters (Injected via Depends).
    - Returns: JSON response indicating the success or failure of the add book
        operation.
- DELETE /books/{isbn}:
    - Description: API endpoint to delete a book identified by its ISBN.
    - Parameters: ISBN of the book to be deleted.
    - Returns: JSON response indicating the success or failure of the delete book
        operation.

Usage:
To run the application, execute this module directly. The application will be available
at host 127.0.0.1 on port 8000.

Example:
    $ python <module_name.py>
"""

from typing import Dict, List, Optional

from api.data import BOOKS
from api.models import AddBookQueryParameters, BookQueryParameters


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
