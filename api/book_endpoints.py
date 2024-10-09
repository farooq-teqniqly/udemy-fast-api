"""
This module defines a FastAPI application for querying and adding books.

It includes the following components:
- FastAPI application setup with a specified title.
- API endpoints to query and add books using specified parameters.
- Dependency injection to handle book query and addition parameters.

Main Components:
- FastAPI: The web framework used to create the API application.
- uvicorn: ASGI server used to run the application.
- api.book_service: Module containing the business logic for querying and adding books.
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

Usage:
To run the application, execute this module directly. The application will be available
at host 127.0.0.1 on port 8000.

Example:
    $ python <module_name.py>
"""

import uvicorn
from fastapi import Depends, FastAPI

import api.book_service as bs
from api.models import AddBookQueryParameters, BookQueryParameters

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
async def add_book(params: AddBookQueryParameters = Depends()):
    """
    Args:
        params: Query parameters for adding a book. Expected to be an instance of
        AddBookQueryParameters.

    Returns:
        JSON response indicating the success or failure of the add book operation.
    """
    return await bs.add_book(params)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
