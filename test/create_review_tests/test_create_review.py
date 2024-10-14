from test import client

import pytest
import test_data
from starlette import status


def test_can_add_review_to_book(mocker):
    test_data.setup_mock_books(mocker)
    mock_reviews = test_data.setup_mock_reviews(mocker)
    review_text = "This is a great book!"
    request = dict(review=review_text)
    response = client.post(f"/books/{test_data.VALID_ISBN}/reviews", json=request)
    assert response.status_code == status.HTTP_200_OK
    assert any(review_text in review_data["reviews"] for review_data in mock_reviews)


@pytest.mark.parametrize("isbn", test_data.INVALID_ISBNS)
def test_create_reviews_fails_when_isbn_invalid(isbn):
    request = dict(review="Yay!")
    response = client.post(f"/books/{isbn}/reviews", json=request)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
