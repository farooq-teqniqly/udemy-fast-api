"""
This module contains test cases for the DELETE /books/{isbn} endpoint of the API.
"""

from test import client


def test_delete_book_fails_with_invalid_isbn_in_url():
    response = client.delete("/books/foobar1234")
    assert response.status_code == 422


def test_delete_book_succeeds_with_valid_isbn_in_url():
    response = client.delete("/books/4444444444444")
    assert response.status_code == 200
