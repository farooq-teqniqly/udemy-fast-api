"""
models.py

This module defines several Pydantic models used for handling query parameters and
request bodies in the book-related endpoints of the application. These models ensure
data validation and structured representation of request parameters related to books,
their ratings, and reviews.

Attributes:
    validators (module): A module containing validators for input data.

Classes:
    BookQueryParameters:
        A Pydantic model representing query parameters for filtering and paginating
        book search results. Includes attributes such as author, category, top,
        ISBN, and a flag to include deleted books.

        Class Attributes:
            - author (Optional[str]): The author of the book.
            - category (Optional[str]): The category or genre of the book.
            - top (Optional[int]): The top N records to return.
            - isbn (Optional[str]): The ISBN number of the book.
            - return_deleted_books (bool): Flag to include deleted books in the query.

        Methods:
            - isbn_must_be_13_digits(cls, value): Validates that the ISBN is exactly 13
            digits long if provided.

    CreateBookRequest:
        A Pydantic model representing the mandatory parameters required for adding
        a new book. Includes attributes such as author, title, category, and ISBN.

        Class Attributes:
            - author (str): The author of the book.
            - title (str): The title of the book.
            - category (str): The category or genre of the book.
            - isbn (str): The ISBN number of the book, must be exactly 13 numeric
                digits.

    AddRatingParameters:
        A Pydantic model representing the parameters required for adding a rating
        to a book. Ensures that the rating value is within the specified range of
        1.0 to 5.0.

        Class Attributes:
            - rating (confloat): A floating-point number for the rating, constrained
              to be between 1.0 and 5.0 inclusive.

    CreateReviewRequest:
        A Pydantic model representing the request to add a review. Includes the
        review content.

        Class Attributes:
            - review (str): The content of the review.

Example usage:
    Creating a query parameter instance for book search:

    ```python
    query_params = BookQueryParameters(
        author="J.K. Rowling",
        category="Fantasy",
        top=10)
    print(query_params.dict())
    ```

    Creating a parameter instance for adding a new book:

    ```python
    add_params = CreateBookRequest(
        author="J.K. Rowling",
        title="New Book",
        category="Fantasy",
        isbn="1234567890123")
    print(add_params.dict())
    ```

    Creating a parameter instance for adding a rating:

    ```python
    rating_params = AddRatingParameters(
        rating=4.5)
    print(rating_params.dict())
    ```

    Creating a parameter instance for adding a review:

    ```python
    review_params = CreateReviewRequest(
        review="Great book!")
    print(review_params.dict())
    ```
"""

from typing import Optional

from pydantic import BaseModel, Field, confloat

VALID_ISBN_REGEX = r"\d{13}"


class BookQueryParameters(BaseModel):
    """
    BookQueryParameters Model

    Represents query parameters for querying book records.

    Attributes:
        author (Optional[str]): The author of the book.
        category (Optional[str]): The category or genre of the book.
        top (Optional[int]): The top N records to return.
        isbn (Optional[str]): The ISBN number of the book.
        return_deleted_books (bool): Flag to include deleted books in the query.
        Defaults to False.

    Methods:
        isbn_must_be_13_digits(cls, value):
            Validates that the ISBN is exactly 13 digits long if provided.
    """

    author: Optional[str] = None
    category: Optional[str] = None
    top: Optional[int] = None
    isbn: Optional[str] = Field(None, pattern=VALID_ISBN_REGEX)
    return_deleted_books: bool = False


class CreateBookRequest(BaseModel):
    """
    Class representing a request to create a book.

    Attributes:
        author: The name of the book's author.
        title: The title of the book.
        category: The category or genre of the book.
        isbn: The ISBN of the book, which is validated by the `validate_isbn` function.
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
