"""
book_endpoints.py

This module defines the endpoints for managing book-related operations
within the application. It leverages FastAPI to register routes for CRUD
operations related to books, handling ratings, and managing reviews.

Attributes:
    bs: An instance of book services used to handle various book-related operations.
    validators: A module containing validators for input data.
    app: The FastAPI application instance to which all the endpoints are registered.

Functions:
    query_book(request):
        Handles GET requests to fetch details of a specific book or a list of books
        based on provided query parameters.

    add_book(request):
        Handles POST requests to add a new book to the collection. Takes in various
        book details as input.

    delete_book(request):
        Handles DELETE requests to remove a book from the collection based on the
        book ID provided.

    add_rating(request):
        Handles POST requests to add a rating to a specific book. The rating details
        are provided in the request.

    add_review(request):
        Handles POST requests to add a review for a specific book. Review details
        are provided in the request.

    get_reviews(request):
        Handles GET requests to fetch reviews of a specific book. The book ID is
        provided in the query parameters.
"""

import uvicorn
from fastapi import Body, Depends, FastAPI

import api.book_service as bs
import api.validators as validators
from api.models import (
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
async def add_book(params: CreateBookRequest = Body()):
    """
    Args:
        params: Query parameters for adding a book. Expected to be an instance of
        CreateBookRequest.

    Returns:
        JSON response indicating the success or failure of the add book operation.
    """
    return await bs.add_book(params)


@app.delete("/books/{isbn}")
async def delete_book(isbn: str = Depends(validators.validate_isbn)):
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
    isbn: str = Depends(validators.validate_isbn),
    params: AddRatingParameters = Depends(),
):
    """
    Args:
        isbn: The ISBN of the book to which the rating should be added. This parameter
        is validated using the _validate_isbn dependency.
        params: A set of parameters required to add the rating. This is provided by the
        AddRatingParameters dependency.
    """
    return await bs.add_rating(isbn, params)


@app.post("/books/{isbn}/reviews")
async def add_review(
    isbn: str = Depends(validators.validate_isbn), request: CreateReviewRequest = Body()
):
    """
    Adds a review for a book with the given ISBN.

    Args:
        isbn: The International Standard Book Number of the book.
        request: An instance of CreateReviewRequest containing the review details.

    Returns:
        The result of adding the review to the book.
    """
    return await bs.add_review(isbn, request)


@app.get("/books/{isbn}/reviews")
async def get_reviews(isbn: str = Depends(validators.validate_isbn)):
    """
    Args:
        isbn: A string representing the International Standard Book Number (ISBN).

    Returns:
        Reviews of the book identified by the given ISBN.
    """
    return await bs.get_reviews(isbn)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
