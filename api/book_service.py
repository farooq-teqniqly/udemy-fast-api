"""
book_service.py

This module provides various services related to book management. It includes functions
for filtering, adding, deleting, and querying books, as well as handling book ratings
and reviews.

Functions:
    _filter_books(books: list, query_params: BookQueryParameters) -> list:
        Filters books based on given query parameters like author, category, and ISBN.

    _limit_books(books: list, limit: int) -> list:
        Limits the number of books returned to a specified top N value.

    _exclude_deleted_books(books: list, include_deleted: bool) -> list:
        Excludes books marked as soft-deleted from the list of books unless
        include_deleted is set to True.

    _get_author_last_name(author_name: str) -> str:
        Extracts the last name from the full author name for sorting purposes.

    query_book(query_params: BookQueryParameters) -> list:
        Returns a list of books based on the provided query parameters. It applies
        filters, limits the results, and sorts the list based on the author's last name.

    create_book(book_data: CreateBookRequest) -> dict:
        Adds a new book to the list using the provided book details and returns
        the created book.

    delete_book(book_id: int) -> None:
        Marks a book as soft-deleted based on the provided book ID.

    add_rating(book_id: int, rating_data: AddRatingRequest) -> None:
        Adds a rating to the specified book and updates its average rating and
        total number of ratings.

    create_review(book_id: int, review_data: CreateReviewRequest) -> None:
        Adds a review to the specified book based on the provided review content.

    get_reviews(book_id: int) -> list:
        Retrieves all reviews for the specified book.

Example usage:
    Querying books with specific parameters:

    ```python
    query_params = BookQueryParameters(
        author="J.K. Rowling",
        category="Fantasy",
        top=10)
    books = query_book(query_params)
    print(books)
    ```

    Adding a new book:

    ```python
    new_book = CreateBookRequest(
        author="J.K. Rowling",
        title="New Book",
        category="Fantasy",
        isbn="1234567890123")
    created_book = create_book(new_book)
    print(created_book)
    ```

    Deleting a book:

    ```python
    delete_book(book_id=1)
    ```

    Adding a rating to a book:

    ```python
    rating = AddRatingRequest(rating=4.5)
    add_rating(book_id=1, rating_data=rating)
    ```

    Adding a review to a book:

    ```python
    review = CreateReviewRequest(review="Great book!")
    create_review(book_id=1, review_data=review)
    ```

    Getting reviews for a book:

    ```python
    reviews = get_reviews(book_id=1)
    print(reviews)
    ```
"""

from typing import Dict, List, Optional

from api.data import BOOK_REVIEWS, BOOKS
from api.models import (
    AddRatingRequest,
    BookQueryParameters,
    CreateBookRequest,
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


async def create_book(params: CreateBookRequest) -> None:
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
            soft_deleted=False,
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


async def add_rating(isbn: str, params: AddRatingRequest):
    books = [b for b in BOOKS if b["isbn"] == isbn]

    if len(books) == 0:
        return

    book = books[0]
    book["num_ratings"] += 1
    book["sum_ratings"] += params.rating
    book["avg_rating"] = book["sum_ratings"] / book["num_ratings"]


async def create_review(isbn: str, request: CreateReviewRequest):
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
