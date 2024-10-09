"""
This module provides functionality for querying books from a predefined list of books.
It includes helper functions to filter and limit the books based on various criteria
such as author, category, and ISBN.

Functions:
    _filter_books(books, key, value): Filters the list of books based on a given key
    and value.
    _limit_books(books, limit): Limits the number of books returned.
    query_book(params): Asynchronously queries books based on given query parameters.

The `query_book` function can be used to perform complex queries on the list of books by
combining multiple filter criteria and limiting the results.

Dependencies:
    - api.data.BOOKS: A predefined list of books.
    - api.models.BookQueryParameters: A dataclass defining the parameters for querying
    books.
"""

from typing import Dict, List, Optional

from api.data import BOOKS
from api.models import BookQueryParameters


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
    return _limit_books(filtered_books, params.top)
