from test import client

import pytest
import test_data

import api.http_status_codes as status_code


def test_get_reviews_when_book_has_no_reviews_returns_empty_list(mocker):
    mock_books = test_data.setup_mock_books(mocker)
    response = client.get(f"/books/{mock_books[0]['isbn']}/reviews")
    assert response.status_code == status_code.OK
    assert response.json() == []


def test_get_reviews_returns_correct_reviews(mocker):
    mock_reviews = test_data.setup_mock_reviews(mocker)

    response = client.get(f"/books/{test_data.VALID_ISBN}/reviews")
    assert response.status_code == status_code.OK
    assert response.json() == mock_reviews


def test_get_reviews_when_book_does_not_exist_returns_empty_list(mocker):
    test_data.setup_mock_reviews(mocker)
    response = client.get("/books/0000000000000/reviews")
    assert response.status_code == status_code.OK
    assert response.json() == []


@pytest.mark.parametrize("isbn", test_data.INVALID_ISBNS)
def test_get_reviews_fails_when_isbn_invalid(isbn):
    response = client.get(f"/books/{isbn}/reviews")
    assert response.status_code == status_code.UNPROCESSABLE_ENTITY
