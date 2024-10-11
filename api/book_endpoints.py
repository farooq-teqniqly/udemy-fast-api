"""
book_endpoints.py

This module defines the endpoints for managing book-related operations within
the application. It leverages FastAPI to register routes for CRUD operations
related to books, handling ratings, and managing reviews.

Attributes:
    bs (BookService): An instance of the book services used to handle various
    book-related operations.
    validators (module): A module containing validators for input data.
    app (FastAPI): The FastAPI application instance to which all the endpoints are
    registered.

Functions:
    query_book(request: QueryBookRequest) -> List[Book]:
        Handles GET requests to fetch details of a specific book or a list of books
        based on provided query parameters. Uses book service for querying.

    create_book(request: CreateBookRequest) -> Book:
        Handles POST requests to add a new book to the collection. Takes in various
        book details as input and uses the book service to create the book.

    delete_book(book_id: int) -> None:
        Handles DELETE requests to remove a book from the collection based on the
        book ID provided. Uses the book service to perform the deletion.

    add_rating(book_id: int, request: AddRatingRequest) -> None:
        Handles POST requests to add a rating to a specific book. The rating details
        are provided in the request, and it uses the book service to add the rating.

    create_review(book_id: int, request: CreateReview) -> None:
        Handles POST requests to add a review for a specific book. Review details
        are provided in the request, and it uses the book service to add the review.

    get_reviews(book_id: int) -> List[Review]:
        Handles GET requests to fetch reviews of a specific book. The book ID is
        provided in the query parameters, and it uses the book service to retrieve the
        reviews.
"""

import uvicorn
from fastapi import Body, Depends, FastAPI, Path

import api.book_service as bs
from api.models import (
    VALID_ISBN_REGEX,
    AddRatingParameters,
    BookQueryParameters,
    CreateBookRequest,
    CreateReviewRequest,
)

app = FastAPI(title="My Books API")


@app.get("/books/q")
async def query_book(params: BookQueryParameters = Depends()):
    """
    API endpoint to query books based on specified parameters.

    Args:
        params (BookQueryParameters): The parameters used to query books.

    Returns:
        The result of the book query.
    """
    return await bs.query_book(params)


@app.post("/books")
async def create_book(params: CreateBookRequest):
    """
    Args:
        params (CreateBookRequest): The parameters for creating a new book, coming from
        the request body.

    Returns:
        The newly created book after being added to the system.
    """
    return await bs.create_book(params)


@app.delete("/books/{isbn}")
async def delete_book(isbn: str = Path(pattern=VALID_ISBN_REGEX)):
    """
    Args:
        isbn: The International Standard Book Number (ISBN) of the book to be deleted.
        It is validated using the `validate_isbn` function.

    Returns:
        The result of the book deletion operation, which could include confirmation of
        deletion or an error message if the book could not be deleted.
    """
    return await bs.delete_book(isbn)


@app.post("/books/{isbn}/ratings")
async def add_rating(
    isbn: str = Path(pattern=VALID_ISBN_REGEX),
    params: AddRatingParameters = Body(),
):
    """
    Args:
        isbn: The ISBN of the book for which the rating is being added. Validated by
        `validators.validate_isbn`.
        params: The parameters for the rating being added, encapsulated in
        `AddRatingParameters` and passed in the request body.
    """
    return await bs.add_rating(isbn, params)


@app.post("/books/{isbn}/reviews")
async def create_review(
    isbn: str = Path(pattern=VALID_ISBN_REGEX), request: CreateReviewRequest = Body()
):
    """
    Args:
        isbn: The ISBN of the book for which the review is to be created. This parameter
        is validated using the `validators.validate_isbn` function.
        request: A request body containing the details of the review to be created. This
        parameter is expected to be an instance of `CreateReviewRequest`.
    """
    return await bs.create_review(isbn, request)


@app.get("/books/{isbn}/reviews")
async def get_reviews(isbn: str = Path(pattern=VALID_ISBN_REGEX)):
    """
    Args:
        isbn: A string representing the International Standard Book Number (ISBN).

    Returns:
        Reviews of the book identified by the given ISBN.
    """
    return await bs.get_reviews(isbn)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
