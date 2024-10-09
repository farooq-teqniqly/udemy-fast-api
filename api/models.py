"""
Book Query Parameters Module

This module provides the definition of the `BookQueryParameters` and
`AddBookQueryParameters` classes, which are used to represent the query parameters for
filtering, paginating, and adding book search results.

Classes:
    BookQueryParameters: A Pydantic model that includes optional attributes such as
    author, category, top, and ISBN to filter book search results.
    AddBookQueryParameters: A Pydantic model that includes mandatory attributes such as
    author, title, category, and ISBN to add a new book.

Example usage:
    Creating a query parameter instance for book search:

    query_params = BookQueryParameters(
        author="J.K. Rowling",
        category="Fantasy",
        top=10)
    print(query_params.dict())

    Creating a parameter instance for adding a new book:

    add_params = AddBookQueryParameters(
        author="J.K. Rowling",
        title="New Book",
        category="Fantasy",
        isbn="1234567890")
    print(add_params.dict())
"""

from typing import Optional

from pydantic import BaseModel


class BookQueryParameters(BaseModel):
    """
    BookQueryParameters is a model for specifying query parameters related to books.

    Attributes:
        author (Optional[str]): The name of the author to query.
        category (Optional[str]): The category or genre of the book to query.
        top (Optional[int]): The number of top records to retrieve.
        isbn (Optional[str]): The ISBN number of the book to query.
    """

    author: Optional[str] = None
    category: Optional[str] = None
    top: Optional[int] = None
    isbn: Optional[str] = None


class AddBookQueryParameters(BaseModel):
    author: str
    title: str
    category: str
    isbn: str
