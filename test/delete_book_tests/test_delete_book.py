"""
This module contains test cases for the DELETE /books/{isbn} endpoint of the API.
"""

from test import client

import pytest
import test_data
from starlette import status


@pytest.mark.parametrize("isbn", test_data.INVALID_ISBNS)
def test_delete_book_fails_when_isbn_invalid(isbn):
    response = client.delete(f"/books/{isbn}")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_book_when_successful_sets_soft_deleted_to_true(mocker):
    books = [
        dict(
            isbn=test_data.VALID_ISBN,
            title="A Brief History of Time",
            author="Stephen Hawking",
            category="Science",
            avg_rating=None,
            num_ratings=0,
            sum_ratings=0,
            soft_deleted=False,
        )
    ]

    test_data.setup_mock_books(mocker, books)
    response = client.delete(f"/books/{test_data.VALID_ISBN}")
    assert response.status_code == status.HTTP_200_OK
    assert books[0]["soft_deleted"]


def test_delete_book_succeeds_even_when_book_does_not_exist(mocker):
    mock_books = test_data.setup_mock_books(mocker)
    mocker.patch("api.book_service.BOOKS", mock_books)
    response = client.delete("/books/0000000000000")
    assert response.status_code == status.HTTP_200_OK
