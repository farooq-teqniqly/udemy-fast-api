from test import client

import pytest
import test_data
from starlette import status


def test_average_and_number_of_ratings_is_correctly_calculated(mocker):
    mock_books = test_data.setup_mock_books(mocker)
    mock_book = mock_books[0]

    request = dict(rating=2)
    response = client.post(f"/books/{mock_book["isbn"]}/ratings", json=request)
    assert response.status_code == status.HTTP_200_OK

    request = dict(rating=3)
    response = client.post(f"/books/{mock_book["isbn"]}/ratings", json=request)
    assert response.status_code == status.HTTP_200_OK

    request = dict(rating=4.5)
    response = client.post(f"/books/{mock_book["isbn"]}/ratings", json=request)
    assert response.status_code == status.HTTP_200_OK

    assert mock_book["num_ratings"] == 3
    assert mock_book["avg_rating"] == pytest.approx(3.2, abs=1e-1)


@pytest.mark.parametrize("rating", [-1, -0.5, 0, 0.5, 5.5, 6])
def test_cannot_add_invalid_ratings(mocker, rating):
    mock_books = test_data.setup_mock_books(mocker)
    request = dict(rating=rating)
    response = client.post(f"/books/{mock_books[0]["isbn"]}/ratings", json=request)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize("rating", [x * 0.5 for x in range(2, 11)])
def test_when_ratings_are_valid_request_is_successful(mocker, rating):
    mock_books = test_data.setup_mock_books(mocker)
    request = dict(rating=rating)
    response = client.post(f"/books/{mock_books[0]["isbn"]}/ratings", json=request)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize("isbn", test_data.INVALID_ISBNS)
def test_add_rating_fails_wth_invalid_isbn(isbn):
    request = dict(rating=2.5)
    response = client.post(f"/books/{isbn}/ratings", json=request)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
