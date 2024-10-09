from typing import Dict, List, Optional

from api.data import BOOKS


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


async def query_book(
    author: Optional[str] = None,
    category: Optional[str] = None,
    top: Optional[int] = None,
    isbn: Optional[str] = None,
) -> List[Dict[str, Optional[str]]]:
    filtered_books = _filter_books(BOOKS, "author", author)
    filtered_books = _filter_books(filtered_books, "category", category)
    filtered_books = _filter_books(filtered_books, "isbn", isbn)
    return _limit_books(filtered_books, top)
