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
    filtered_books = _filter_books(BOOKS, "author", params.author)
    filtered_books = _filter_books(filtered_books, "category", params.category)
    filtered_books = _filter_books(filtered_books, "isbn", params.isbn)
    return _limit_books(filtered_books, params.top)
