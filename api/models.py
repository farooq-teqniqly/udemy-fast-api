"""
Models for the book management API.

This module defines the data models used by the book management API. It includes the
following classes and attributes:

Attributes:
    VALID_ISBN_REGEX (str): A regular expression pattern for validating ISBN numbers.

Classes:
    BookQueryParameters: Parameters for querying books.
        - author (str): The author of the book.
        - category (str): The category of the book.
        - top (int): The number of top books to return.
        - isbn (str): The ISBN of the book.
        - return_deleted_books (bool): A flag to include deleted books in the results.

    CreateBookRequest: Parameters for creating a new book.
        - author (str): The author of the book.
        - title (str): The title of the book.
        - category (str): The category of the book.
        - isbn (str): The ISBN of the book.

    AddRatingParameters: Parameters for adding a rating to a book.
        - rating (int): The rating value.

    CreateReviewRequest: Parameters for creating a review for a book.
        - review (str): The content of the review.
"""

from typing import Optional

from pydantic import BaseModel, Field, confloat

VALID_ISBN_REGEX = r"\d{13}"


class BookQueryParameters(BaseModel):
    """
    BookQueryParameters is a model used to encapsulate the query parameters for
    searching books in a library system.

    Attributes:
        author: The author of the book. Optional.
        category: The category of the book. Optional.
        top: The maximum number of top results to return. Optional.
        isbn: The ISBN of the book. This field must match the provided ISBN pattern.
        Optional.
        return_deleted_books: A flag indicating whether to return deleted books in the
        query results. Defaults to False.
    """

    author: Optional[str] = None
    category: Optional[str] = None
    top: Optional[int] = None
    isbn: Optional[str] = Field(None, pattern=VALID_ISBN_REGEX)
    return_deleted_books: bool = False


class CreateBookRequest(BaseModel):
    """
    Class for creating a book request.

    Attributes:
        author: The author of the book.
        title: The title of the book.
        category: The category or genre of the book.
        isbn: The International Standard Book Number (ISBN) of the book, which must
        match the VALID_ISBN_REGEX pattern.
    """

    author: str
    title: str
    category: str
    isbn: str = Field(pattern=VALID_ISBN_REGEX)


class AddRatingParameters(BaseModel):
    """
    Represents the parameters required to add a rating.
    This class is responsible for validating that the
    rating value is within the specified range of 1.0 to 5.0.

    Attributes:
        rating: A floating-point number for the rating, constrained
                to be between 1.0 and 5.0 inclusive.
    """

    rating: confloat(ge=1.0, le=5.0) = Field(
        description="Rating must be between 1 and 5."
    )


class CreateReviewRequest(BaseModel):
    """
    CreateReviewRequest is a data model representing the request to add a review.

    Attributes:
        review (str): The content of the review.
    """

    review: str
