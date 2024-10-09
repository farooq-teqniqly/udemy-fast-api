"""
Book Query Parameters Module

This module provides the definition of the `BookQueryParameters` class, which is used
to represent the query parameters for filtering and paginating book search results.

Classes:
    BookQueryParameters: A Pydantic model that includes optional attributes such as
    author, category, top, and ISBN to filter book search results.

Example usage:
    query_params = BookQueryParameters(author="J.K. Rowling", category="Fantasy",
    top=10)
    print(query_params.dict())
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
