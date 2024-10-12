"""
This module contains test cases for the DELETE /books/{isbn} endpoint of the API.
"""

from test import client

VALID_ISBN = "4444444444444"
INVALID_ISBN = "foobar1234"
NON_EXISTENT_ISBN = "0000000000000"


def _setup_mock_books(mocker, books):
    mocker.patch("api.book_service.BOOKS", books)


def test_delete_book_fails_with_invalid_isbn_in_url():
    response = client.delete(f"/books/{INVALID_ISBN}")
    assert response.status_code == 422


def test_delete_book_when_successful_sets_soft_deleted_to_true(mocker):
    mock_books = [
        dict(
            isbn=VALID_ISBN,
            title="A Brief History of Time",
            author="Stephen Hawking",
            category="Science",
            avg_rating=None,
            num_ratings=0,
            sum_ratings=0,
            soft_deleted=False,
        )
    ]

    _setup_mock_books(mocker, mock_books)
    response = client.delete(f"/books/{VALID_ISBN}")
    assert response.status_code == 200
    assert mock_books[0]["soft_deleted"]


def test_delete_book_succeeds_even_when_book_does_not_exist(mocker):
    mock_books = [
        dict(
            isbn=VALID_ISBN,
            title="A Brief History of Time",
            author="Stephen Hawking",
            category="Science",
            avg_rating=None,
            num_ratings=0,
            sum_ratings=0,
            soft_deleted=False,
        )
    ]

    _setup_mock_books(mocker, mock_books)
    mocker.patch("api.book_service.BOOKS", mock_books)
    response = client.delete(f"/books/{NON_EXISTENT_ISBN}")
    assert response.status_code == 200
