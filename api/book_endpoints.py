"""
Endpoints for book management API.

This module defines the endpoints for the book management API. It includes the following
attributes and functions:

Attributes:
    bs (BookService): The service instance used for book operations.
    app (FastAPI): The FastAPI instance used for defining the endpoints.

Functions:
    query_book: Endpoint to query books based on various parameters.
    create_book: Endpoint to create a new book in the system.
    delete_book: Endpoint to delete a book by its ISBN.
    add_rating: Endpoint to add a rating to a book.
    create_review: Endpoint to create a review for a book.
    get_reviews: Endpoint to get reviews for a specific book.
"""

import uvicorn
from fastapi import Body, Depends, FastAPI, Path, Request
from starlette import status

import api.book_service as bs
from api.models import (
    VALID_ISBN_REGEX,
    AddRatingRequest,
    BookQueryParameters,
    CreateBookRequest,
    CreateReviewRequest,
)

app = FastAPI(title="My Books API")


def _add_links(d: dict, self_link: str) -> dict:
    d["links"] = dict(self=self_link)
    return d


@app.get("/books/q", status_code=status.HTTP_200_OK)
async def query_book(params: BookQueryParameters = Depends()):
    """
    API endpoint to query books based on specified parameters.

    Args:
        params (BookQueryParameters): The parameters used to query books.

    Returns:
        The result of the book query.
    """
    return await bs.query_book(params)


@app.post("/books", status_code=status.HTTP_201_CREATED, response_model=dict)
async def create_book(request: Request, params: CreateBookRequest):
    """
    Args:
        request: HTTP request object that provides request data and context.
        params: CreateBookRequest object that contains the book details to create.
    """
    book = await bs.create_book(params)
    self = f"{request.url_for("query_book")}?isbn={params.isbn}"

    _add_links(book, self)
    return book


@app.delete("/books/{isbn}")
async def delete_book(isbn: str = Path(pattern=VALID_ISBN_REGEX)):
    """
    Args:
        isbn (str): The International Standard Book Number (ISBN) of the book to be
        deleted. It must match the VALID_ISBN_REGEX pattern.

    Returns:
        Response: An HTTP response indicating the outcome of the delete operation.
    """
    return await bs.delete_book(isbn)


@app.post("/books/{isbn}/ratings")
async def add_rating(
    isbn: str = Path(pattern=VALID_ISBN_REGEX),
    params: AddRatingRequest = Body(),
):
    """
    Args:
        isbn: The ISBN of the book for which the rating is being added. Must match the
        VALID_ISBN_REGEX pattern.
        params: The parameters for adding the rating, encapsulated in an
        AddRatingRequest object.
    """
    return await bs.add_rating(isbn, params)


@app.post("/books/{isbn}/reviews")
async def create_review(
    isbn: str = Path(pattern=VALID_ISBN_REGEX), request: CreateReviewRequest = Body()
):
    """
    Args:
        isbn: A string representing the International Standard Book Number (ISBN) of the
        book for which the review is being created. This is validated against a
        predefined regex pattern.
        request: An instance of CreateReviewRequest containing the details of the review
        to be created.
    """
    return await bs.create_review(isbn, request)


@app.get("/books/{isbn}/reviews", status_code=status.HTTP_200_OK)
async def get_reviews(isbn: str = Path(pattern=VALID_ISBN_REGEX)):
    """
    Retrieve reviews for a book identified by its ISBN.

    Args:
        isbn (str): The ISBN number of the book. It should match the pattern specified
        by VALID_ISBN_REGEX.

    Returns:
        A list of reviews for the specified book.
    """
    return await bs.get_reviews(isbn)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
